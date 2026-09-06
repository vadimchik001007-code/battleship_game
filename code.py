import pygame
import random

# ---------------------------------------------------------------------------
# Ниже - запуск PyGame и основные параметры окна игры.
pygame.init()
width, height = 1040, 700
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Морской бой")
clock = pygame.time.Clock()

# ---------------------------------------------------------------------------
# Ниже - цвета, размеры игрового поля и параметры двух сеток 10*10.
background_color = (13, 73, 112)
field_color = (182, 229, 242)
grid_color = (30, 85, 120)
ship_color = (80, 80, 90)
hit_color = (225, 65, 50)
miss_color = (245, 245, 245)
text_color = (255, 255, 255)
button_color = (35, 133, 184)
button_hover_color = (54, 164, 220)
cell_size = 42
grid_size = 10
pix_grid_size = cell_size * grid_size
tabX1 = 70
tabX2 = 550
tabY = 180

# ---------------------------------------------------------------------------
# Ниже - шрифты, используемые для заголовков, текста и кнопок.
font_small = pygame.font.SysFont("arial", 20)
font_normal = pygame.font.SysFont("arial", 27)
font_big = pygame.font.SysFont("arial", 45, bold=True)


# ---------------------------------------------------------------------------
# Функция ниже создаёт матрицу состояний игровой сетки.
# 0 - вода, 1 - корабль, 2 - попадание, 3 - промах.
def create_grid_matrix(grid_size):
    grid = []
    for i in range(grid_size):
        row_list = []
        for j in range(grid_size):
            row_list.append(0)
        grid.append(row_list)
    return grid


# ---------------------------------------------------------------------------
# Функция ниже проверяет, можно ли поставить корабль заданной длины.
def can_place_ship(grid, row, col, direction, length):
    for i in range(length):
        new_row = row
        new_col = col
        if direction == "right":
            new_col = col + i
        else:
            new_row = row + i

        if new_row >= grid_size or new_col >= grid_size:
            return False

        # Проверяем клетку корабля и все соседние клетки вокруг неё.
        for check_row in range(new_row - 1, new_row + 2):
            for check_col in range(new_col - 1, new_col + 2):
                if 0 <= check_row < grid_size and 0 <= check_col < grid_size:
                    if grid[check_row][check_col] == 1:
                        return False
    return True


# ---------------------------------------------------------------------------
# Функция ниже ставит корабль в матрицу после успешной проверки.
def place_ship(grid, row, col, direction, length):
    for i in range(length):
        if direction == "right":
            grid[row][col + i] = 1
        else:
            grid[row + i][col] = 1


# ---------------------------------------------------------------------------
# Функция ниже автоматически расставляет стандартный набор кораблей.
def place_all_ships(grid):
    ships = [4, 3, 3, 2, 2, 2, 1, 1, 1, 1]
    for length in ships:
        ship_placed = False
        while ship_placed == False:
            row = random.randint(0, grid_size - 1)
            col = random.randint(0, grid_size - 1)
            direction = random.choice(["right", "down"])
            if can_place_ship(grid, row, col, direction, length):
                place_ship(grid, row, col, direction, length)
                ship_placed = True


# ---------------------------------------------------------------------------
# Функция ниже рисует буквы и цифры вокруг сетки.
def draw_grid_marks(tabX, tabY):
    letters = "АБВГДЕЖЗИК"
    for i in range(grid_size):
        letter = font_small.render(letters[i], True, text_color)
        number = font_small.render(str(i + 1), True, text_color)
        screen.blit(letter, (tabX + i * cell_size + 14, tabY - 27))
        screen.blit(number, (tabX - 25, tabY + i * cell_size + 10))


# ---------------------------------------------------------------------------
# Функция ниже отрисовывает сетку, корабли, попадания и промахи.
def draw_grid(grid, tabX, tabY, show_ships):
    # Сначала рисуем клетки и их внутреннее содержимое.
    for row in range(grid_size):
        for col in range(grid_size):
            cell_rect = pygame.Rect(tabX + col * cell_size, tabY + row * cell_size, cell_size, cell_size)
            pygame.draw.rect(screen, field_color, cell_rect)

            if grid[row][col] == 1 and show_ships:
                ship_rect = pygame.Rect(cell_rect.x + 4, cell_rect.y + 4, cell_size - 8, cell_size - 8)
                pygame.draw.rect(screen, ship_color, ship_rect, border_radius=5)
            elif grid[row][col] == 2:
                pygame.draw.circle(screen, hit_color, cell_rect.center, 12)
                pygame.draw.line(screen, text_color, (cell_rect.x + 10, cell_rect.y + 10),
                                 (cell_rect.x + cell_size - 10, cell_rect.y + cell_size - 10), 3)
                pygame.draw.line(screen, text_color, (cell_rect.x + cell_size - 10, cell_rect.y + 10),
                                 (cell_rect.x + 10, cell_rect.y + cell_size - 10), 3)
            elif grid[row][col] == 3:
                pygame.draw.circle(screen, miss_color, cell_rect.center, 6)

    # Затем рисуем линии сетки поверх клеток.
    for line_number in range(grid_size + 1):
        start_y = tabY + cell_size * line_number
        start_x = tabX + cell_size * line_number
        pygame.draw.line(screen, grid_color, (tabX, start_y), (tabX + pix_grid_size, start_y), 2)
        pygame.draw.line(screen, grid_color, (start_x, tabY), (start_x, tabY + pix_grid_size), 2)
    draw_grid_marks(tabX, tabY)


# ---------------------------------------------------------------------------
# Функция ниже проверяет, есть ли на поле хотя бы одна непоражённая часть корабля.
def has_alive_ships(grid):
    for row in range(grid_size):
        for col in range(grid_size):
            if grid[row][col] == 1:
                return True
    return False


# ---------------------------------------------------------------------------
# Функция ниже переводит координаты мыши в номер клетки или возвращает None.
def get_cell_from_mouse(mouse_pos, tabX, tabY):
    mouse_x, mouse_y = mouse_pos
    if tabX <= mouse_x < tabX + pix_grid_size and tabY <= mouse_y < tabY + pix_grid_size:
        col = (mouse_x - tabX) // cell_size
        row = (mouse_y - tabY) // cell_size
        return row, col
    return None


# ---------------------------------------------------------------------------
# Функция ниже делает выстрел и возвращает результат: hit, miss или repeat.
def make_shot(grid, row, col):
    if grid[row][col] == 1:
        grid[row][col] = 2
        return "hit"
    elif grid[row][col] == 0:
        grid[row][col] = 3
        return "miss"
    return "repeat"


# ---------------------------------------------------------------------------
# Функция ниже выбирает случайную ещё не открытую клетку.
def get_random_free_cell(grid, checkerboard):
    free_cells = []
    for row in range(grid_size):
        for col in range(grid_size):
            if grid[row][col] == 0 or grid[row][col] == 1:
                if checkerboard == False or (row + col) % 2 == 0:
                    free_cells.append((row, col))
    if len(free_cells) == 0 and checkerboard:
        return get_random_free_cell(grid, False)
    return random.choice(free_cells)


# ---------------------------------------------------------------------------
# Функция ниже выбирает соседнюю клетку около известного попадания для сложного ИИ.
def get_neighbour_cell(grid, computer_hits):
    for hit_row, hit_col in computer_hits:
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        random.shuffle(directions)
        for row_change, col_change in directions:
            row = hit_row + row_change
            col = hit_col + col_change
            if 0 <= row < grid_size and 0 <= col < grid_size:
                if grid[row][col] == 0 or grid[row][col] == 1:
                    return row, col
    return None


# ---------------------------------------------------------------------------
# Функция ниже считает корабли, у которых все клетки уже поражены.
def count_destroyed_ships(grid):
    checked_cells = []
    destroyed_ships = 0
    for row in range(grid_size):
        for col in range(grid_size):
            if (grid[row][col] == 1 or grid[row][col] == 2) and (row, col) not in checked_cells:
                # Собираем все клетки одного корабля, соединённые сторонами.
                ship_cells = [(row, col)]
                checked_cells.append((row, col))
                cell_number = 0
                while cell_number < len(ship_cells):
                    ship_row, ship_col = ship_cells[cell_number]
                    for row_change, col_change in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                        new_row = ship_row + row_change
                        new_col = ship_col + col_change
                        if 0 <= new_row < grid_size and 0 <= new_col < grid_size:
                            if (grid[new_row][new_col] == 1 or grid[new_row][new_col] == 2):
                                if (new_row, new_col) not in checked_cells:
                                    checked_cells.append((new_row, new_col))
                                    ship_cells.append((new_row, new_col))
                    cell_number += 1
                # Если среди клеток корабля нет состояния 1, корабль уничтожен.
                ship_destroyed = True
                for ship_row, ship_col in ship_cells:
                    if grid[ship_row][ship_col] == 1:
                        ship_destroyed = False
                if ship_destroyed:
                    destroyed_ships += 1
    return destroyed_ships


# ---------------------------------------------------------------------------
# Функция ниже загружает сохранённую статистику из текстового файла.
def load_progress():
    try:
        progress_file = open("progress.txt", "r", encoding="utf-8")
        games = int(progress_file.readline())
        wins = int(progress_file.readline())
        progress_file.close()
        return games, wins
    except (FileNotFoundError, ValueError):
        return 0, 0


# ---------------------------------------------------------------------------
# Функция ниже сохраняет статистику в текстовый файл.
def save_progress(games, wins):
    progress_file = open("progress.txt", "w", encoding="utf-8")
    progress_file.write(str(games) + "\n")
    progress_file.write(str(wins) + "\n")
    progress_file.close()


# ---------------------------------------------------------------------------
# Функция ниже выполняет один выстрел компьютера.
def computer_one_shot(player_grid, difficulty, computer_hits):
    cell = None
    # На сложном уровне компьютер сначала ищет клетку рядом с попаданием.
    if difficulty == "Сложный":
        cell = get_neighbour_cell(player_grid, computer_hits)
    if cell == None:
        # На среднем уровне компьютер сначала стреляет по клеткам в шахматном порядке.
        if difficulty == "Средний":
            cell = get_random_free_cell(player_grid, True)
        else:
            cell = get_random_free_cell(player_grid, False)
    row, col = cell
    result = make_shot(player_grid, row, col)
    if result == "hit":
        computer_hits.append((row, col))
    return result


# ---------------------------------------------------------------------------
# Функция ниже рисует кнопку и возвращает True, если по ней нажали мышью.
def draw_button(text, rect, mouse_pos, mouse_click):
    color = button_color
    if rect.collidepoint(mouse_pos):
        color = button_hover_color
    pygame.draw.rect(screen, color, rect, border_radius=10)
    pygame.draw.rect(screen, text_color, rect, 2, border_radius=10)
    button_text = font_normal.render(text, True, text_color)
    text_rect = button_text.get_rect(center=rect.center)
    screen.blit(button_text, text_rect)
    return mouse_click and rect.collidepoint(mouse_pos)


# ---------------------------------------------------------------------------
# Ниже - создание кнопок меню и начальные значения переменных игры.
button_computer = pygame.Rect(350, 220, 340, 62)
button_two_players = pygame.Rect(350, 300, 340, 62)
button_easy = pygame.Rect(230, 420, 170, 55)
button_medium = pygame.Rect(435, 420, 170, 55)
button_hard = pygame.Rect(640, 420, 170, 55)
button_restart = pygame.Rect(370, 500, 300, 60)
game_state = "menu"
mode = ""
difficulty = "Средний"
current_player = 1
player1_grid = []
player2_grid = []
computer_hits = []
computer_waiting = False
computer_next_shot_time = 0
computer_games, computer_wins = load_progress()
message = "Выберите режим игры."
winner = ""
running = True


# ---------------------------------------------------------------------------
# Ниже - главный игровой цикл программы.
while running:
    mouse_click = False
    mouse_pos = pygame.mouse.get_pos()

    # 1. ОБРАБОТКА СОБЫТИЙ: закрытие окна и нажатия мыши.
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_click = True
            mouse_pos = event.pos

    # 2. ЛОГИКА ИГРЫ: обработка меню, выстрелов и смены игроков.
    if game_state == "menu":
        if draw_button("Игра против компьютера", button_computer, mouse_pos, mouse_click):
            mode = "computer"
            message = "Выберите сложность, затем начнётся расстановка кораблей."
        if draw_button("Игра для двух игроков", button_two_players, mouse_pos, mouse_click):
            mode = "two_players"
            player1_grid = create_grid_matrix(grid_size)
            player2_grid = create_grid_matrix(grid_size)
            # Для быстрой подготовки партии корабли обоих игроков ставятся автоматически.
            place_all_ships(player1_grid)
            place_all_ships(player2_grid)
            current_player = 1
            message = "Ход игрока 1. Кликайте по правому полю."
            game_state = "game"

        if draw_button("Лёгкий", button_easy, mouse_pos, mouse_click):
            difficulty = "Лёгкий"
        if draw_button("Средний", button_medium, mouse_pos, mouse_click):
            difficulty = "Средний"
        if draw_button("Сложный", button_hard, mouse_pos, mouse_click):
            difficulty = "Сложный"

        # После выбора сложности и режима против компьютера создаём игровое поле.
        if mode == "computer" and mouse_click:
            if button_easy.collidepoint(mouse_pos) or button_medium.collidepoint(mouse_pos) or button_hard.collidepoint(mouse_pos):
                player1_grid = create_grid_matrix(grid_size)
                player2_grid = create_grid_matrix(grid_size)
                # У игрока и компьютера корабли расставляются автоматически.
                place_all_ships(player1_grid)
                place_all_ships(player2_grid)
                computer_hits = []
                computer_waiting = False
                message = "Ваш ход. Кликайте по правому полю противника."
                game_state = "game"

    elif game_state == "game" and mouse_click and computer_waiting == False:
        # Правая сетка всегда является полем противника для текущего игрока.
        cell = get_cell_from_mouse(mouse_pos, tabX2, tabY)
        if cell != None:
            row, col = cell
            if current_player == 1:
                target_grid = player2_grid
            else:
                target_grid = player1_grid
            result = make_shot(target_grid, row, col)

            if result == "repeat":
                message = "Эта клетка уже открыта. Выберите другую."
            elif result == "hit":
                message = "Попадание! Можно стрелять ещё раз."
            else:
                message = "Промах. Ход переходит противнику."
                if mode == "two_players":
                    if current_player == 1:
                        current_player = 2
                    else:
                        current_player = 1
                else:
                    message = "Компьютер готовится сделать ход."
                    computer_waiting = True
                    computer_next_shot_time = pygame.time.get_ticks() + 1000

            # После каждого настоящего выстрела проверяем условие победы.
            if result != "repeat" and has_alive_ships(target_grid) == False:
                if current_player == 1:
                    winner = "Игрок 1"
                else:
                    winner = "Игрок 2"
                if mode == "computer" and current_player == 1:
                    winner = "Вы"
                    computer_games += 1
                    computer_wins += 1
                    save_progress(computer_games, computer_wins)
                game_state = "end"
            elif mode == "computer" and has_alive_ships(player1_grid) == False:
                winner = "Компьютер"
                computer_games += 1
                save_progress(computer_games, computer_wins)
                game_state = "end"

    # Компьютер делает один выстрел в секунду, чтобы игрок видел каждый его ход.
    if game_state == "game" and mode == "computer" and computer_waiting:
        if pygame.time.get_ticks() >= computer_next_shot_time:
            computer_result = computer_one_shot(player1_grid, difficulty, computer_hits)
            if has_alive_ships(player1_grid) == False:
                winner = "Компьютер"
                computer_games += 1
                save_progress(computer_games, computer_wins)
                game_state = "end"
                computer_waiting = False
            elif computer_result == "hit":
                message = "Компьютер попал и делает второй ход."
                computer_next_shot_time = pygame.time.get_ticks() + 1000
            else:
                message = "Теперь Ваша очередь делать ход."
                computer_waiting = False

    elif game_state == "end":
        if draw_button("Вернуться в меню", button_restart, mouse_pos, mouse_click):
            game_state = "menu"
            mode = ""
            message = "Выберите режим игры."

    # 3. ОТРИСОВКА: заливка фона и отображение нужного экрана.
    screen.fill(background_color)
    if game_state == "menu":
        title = font_big.render("МОРСКОЙ БОЙ", True, text_color)
        screen.blit(title, title.get_rect(center=(width // 2, 105)))
        menu_text = font_normal.render("Выберите режим и сложность компьютера", True, text_color)
        screen.blit(menu_text, menu_text.get_rect(center=(width // 2, 170)))
        draw_button("Игра против компьютера", button_computer, mouse_pos, False)
        draw_button("Игра для двух игроков", button_two_players, mouse_pos, False)
        draw_button("Лёгкий", button_easy, mouse_pos, False)
        draw_button("Средний", button_medium, mouse_pos, False)
        draw_button("Сложный", button_hard, mouse_pos, False)
        selected_text = font_normal.render("Выбрана сложность: " + difficulty, True, text_color)
        screen.blit(selected_text, selected_text.get_rect(center=(width // 2, 510)))
        # Ниже - раздел прогресса по играм против компьютера.
        progress_title = font_normal.render("Прогресс в игре против компьютера", True, text_color)
        screen.blit(progress_title, progress_title.get_rect(center=(width // 2, 555)))
        progress_text = font_small.render("Сыграно игр: " + str(computer_games) + "    Побед: " + str(computer_wins), True, text_color)
        screen.blit(progress_text, progress_text.get_rect(center=(width // 2, 585)))
        help_text = font_small.render("Корабли расставляются автоматически по классическим правилам.", True, text_color)
        screen.blit(help_text, help_text.get_rect(center=(width // 2, 625)))

    elif game_state == "game":
        # Определяем, какое поле показывать слева и какое справа.
        if current_player == 1:
            own_grid = player1_grid
            enemy_grid = player2_grid
            own_name = "Ваше поле" if mode == "computer" else "Поле игрока 1"
            enemy_name = "Поле компьютера" if mode == "computer" else "Поле игрока 2"
        else:
            own_grid = player2_grid
            enemy_grid = player1_grid
            own_name = "Поле игрока 2"
            enemy_name = "Поле игрока 1"
        left_title = font_normal.render(own_name, True, text_color)
        right_title = font_normal.render(enemy_name, True, text_color)
        screen.blit(left_title, left_title.get_rect(center=(tabX1 + pix_grid_size // 2, 135)))
        screen.blit(right_title, right_title.get_rect(center=(tabX2 + pix_grid_size // 2, 135)))
        draw_grid(own_grid, tabX1, tabY, True)
        draw_grid(enemy_grid, tabX2, tabY, False)
        # Ниже - счётчики полностью уничтоженных кораблей обеих сторон.
        destroyed_by_player = count_destroyed_ships(enemy_grid)
        destroyed_by_enemy = count_destroyed_ships(own_grid)
        if mode == "computer":
            score_text = "Уничтожено Вами: " + str(destroyed_by_player) + "/10    Компьютером: " + str(destroyed_by_enemy) + "/10"
        else:
            score_text = "Уничтожено игроком " + str(current_player) + ": " + str(destroyed_by_player) + "/10    Противником: " + str(destroyed_by_enemy) + "/10"
        score_surface = font_normal.render(score_text, True, text_color)
        screen.blit(score_surface, score_surface.get_rect(center=(width // 2, 610)))
        info_text = font_normal.render(message, True, text_color)
        screen.blit(info_text, info_text.get_rect(center=(width // 2, 650)))

    else:
        end_text = font_big.render(winner + " победил!", True, text_color)
        screen.blit(end_text, end_text.get_rect(center=(width // 2, 250)))
        result_text = font_normal.render("Все корабли противника уничтожены.", True, text_color)
        screen.blit(result_text, result_text.get_rect(center=(width // 2, 325)))
        draw_button("Вернуться в меню", button_restart, mouse_pos, False)

    # 4. ОБНОВЛЕНИЕ ЭКРАНА - один раз в конце кадра.
    pygame.display.flip()
    clock.tick(60)

# ---------------------------------------------------------------------------
# Ниже - корректное завершение работы PyGame после закрытия окна.
pygame.quit()
