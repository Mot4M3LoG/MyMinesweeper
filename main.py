"""
This program enables user to play a game of minesweeper.

Program contains welcome screen with options and play button, options allowing
to change the game's settings such as board size and bombs number,
with instructions on how to play.
Program continues until player either fails or reaches the goal - which the
program announces in a very simple way, then exits to main menu with
possibility of playing again.
"""
import random
import pygame
import sys
import time


def all_da_tables(columns, rows, bombs):
    """
    this function handles generating playable space on the backend -
    generates 2-dim list which the user later interacts with.

    Function takes columns, rows and bombs as parameters, result is a
    ready board of minesweeper.
    """
    bombs_table = [[0 for _ in range(columns)] for _ in range(rows)]

    while bombs > 0:
        for a in range(len(bombs_table)):
            for b in range(len(bombs_table[a])):
                if bombs > 0:
                    x = random.randint(0, 9)
                    if x % 10 == 0 and bombs_table[a][b] != 1:
                        bombs_table[a][b] = 1
                        bombs -= 1

    nums_table = bombs_table
    for a in range(len(bombs_table)):
        for b in range(len(bombs_table[a])):
            if bombs_table[a][b] == 0:
                nums_table[a][b] = 1
            else:
                nums_table[a][b] = 0

    for a in range(len(nums_table)):
        for b in range(len(nums_table[a])):
            if nums_table[a][b] == 0:
                if (b - 1) >= 0 and nums_table[a][b - 1] != 0:
                    nums_table[a][b - 1] += 1
                if (b + 1) < columns and nums_table[a][b + 1] != 0:
                    nums_table[a][b + 1] += 1
                if ((a + 1) < rows and b - 1 >= 0) and \
                        nums_table[a + 1][b - 1] != 0:
                    nums_table[a + 1][b - 1] += 1
                if a + 1 < rows and nums_table[a + 1][b] != 0:
                    nums_table[a + 1][b] += 1
                if (a + 1 < rows and b + 1 < columns) and \
                        nums_table[a + 1][b + 1] != 0:
                    nums_table[a + 1][b + 1] += 1
                if (a - 1 >= 0 and b - 1 >= 0) and \
                        nums_table[a - 1][b - 1] != 0:
                    nums_table[a - 1][b - 1] += 1
                if a - 1 >= 0 and nums_table[a - 1][b] != 0:
                    nums_table[a - 1][b] += 1
                if (a - 1 >= 0 and b + 1 < columns) and \
                        nums_table[a - 1][b + 1] != 0:
                    nums_table[a - 1][b + 1] += 1

    for a in range(len(nums_table)):
        for b in range(len(nums_table[a])):
            if nums_table[a][b] == 0:
                nums_table[a][b] = "X"
            else:
                nums_table[a][b] -= 1

    return nums_table


def reveal():
    """
    reveal handles changing of the state of certain tile - from covered
    to uncovered, and calls for failure() if it was a bomb or reveal_pro(x,
    y), to further reveal the board under good circumstances

    takes no parameters

    changes state of a tile in game_state table(which tiles are hidden or not)
    """
    cursor = pygame.mouse.get_pos()
    for v in range(columns_number):
        for v1, rect in enumerate(tiles_table[v]):
            if rect["rect"].collidepoint(cursor[0], cursor[1]) == 1:
                if game_state[v1][v] == 'Cov':
                    game_state[v1][v] = 'UnCov'
                    if numbers_table[v1][v] == 'X':
                        rect["file"] = "bomb.png"
                        rect["surf"] = pygame.image.load("bomb.png")
                        rect["surf"] = pygame.transform.scale(rect["surf"],
                                                              ((win[0] - 100) /
                                                               columns_number,
                                                               win[1] /
                                                               rows_number))
                        window.blit(rect["surf"], rect["rect"])
                        pygame.display.flip()
                        failure()
                    if numbers_table[v1][v] == 0:
                        reveal_pro(v1, v)


def reveal_pro(cor1, cor2):
    """
    reveal_pro is called when reveal() uncovers a tile which is empty - to
    further reveal the board.

    It takes coordinates of that tile as parameters

    outputs are more changed states of the tiles in game_state
    """
    if cor2 - 1 >= 0:
        if numbers_table[cor1][cor2 - 1] == 0 and \
                game_state[cor1][cor2 - 1] != 'UnCov':
            game_state[cor1][cor2 - 1] = 'UnCov'
            reveal_pro(cor1, cor2 - 1)
        else:
            game_state[cor1][cor2 - 1] = 'UnCov'

    if cor2 - 1 >= 0 and cor1 + 1 < columns_number:
        if numbers_table[cor1 + 1][cor2 - 1] == 0 and \
                game_state[cor1 + 1][cor2 - 1] != 'UnCov':
            game_state[cor1 + 1][cor2 - 1] = 'UnCov'
            reveal_pro(cor1 + 1, cor2 - 1)
        else:
            game_state[cor1 + 1][cor2 - 1] = 'UnCov'

    if cor1 + 1 < columns_number:
        if numbers_table[cor1 + 1][cor2] == 0 and \
                game_state[cor1 + 1][cor2] != 'UnCov':
            game_state[cor1 + 1][cor2] = 'UnCov'
            reveal_pro(cor1 + 1, cor2)
        else:
            game_state[cor1 + 1][cor2] = 'UnCov'

    if cor1 + 1 < columns_number and cor2 + 1 < columns_number:
        if numbers_table[cor1 + 1][cor2 + 1] == 0 and \
                game_state[cor1 + 1][cor2 + 1] != 'UnCov':
            game_state[cor1 + 1][cor2 + 1] = 'UnCov'
            reveal_pro(cor1 + 1, cor2 + 1)
        else:
            game_state[cor1 + 1][cor2 + 1] = 'UnCov'

    if cor2 + 1 < columns_number:
        if numbers_table[cor1][cor2 + 1] == 0 and \
                game_state[cor1][cor2 + 1] != 'UnCov':
            game_state[cor1][cor2 + 1] = 'UnCov'
            reveal_pro(cor1, cor2 + 1)
        else:
            game_state[cor1][cor2 + 1] = 'UnCov'

    if cor1 - 1 >= 0 and cor2 + 1 < columns_number:
        if numbers_table[cor1 - 1][cor2 + 1] == 0 and \
                game_state[cor1 - 1][cor2 + 1] != 'UnCov':
            game_state[cor1 - 1][cor2 + 1] = 'UnCov'
            reveal_pro(cor1 - 1, cor2 + 1)
        else:
            game_state[cor1 - 1][cor2 + 1] = 'UnCov'

    if cor1 - 1 >= 0:
        if numbers_table[cor1 - 1][cor2] == 0 and \
                game_state[cor1 - 1][cor2] != 'UnCov':
            game_state[cor1 - 1][cor2] = 'UnCov'
            reveal_pro(cor1 - 1, cor2)
        else:
            game_state[cor1 - 1][cor2] = 'UnCov'

    if cor1 - 1 >= 0 and cor2 - 1 >= 0:
        if numbers_table[cor1 - 1][cor2 - 1] == 0 and \
                game_state[cor1 - 1][cor2 - 1] != 'UnCov':
            game_state[cor1 - 1][cor2 - 1] = 'UnCov'
            reveal_pro((cor1 - 1), (cor2 - 1))
        else:
            game_state[cor1 - 1][cor2 - 1] = 'UnCov'


def flag():
    """
    this function is responsible for changing the state of tile to flagged
    and vice versa

    takes no parameters

    result is changed state of the tile
    """
    cursor = pygame.mouse.get_pos()
    for v in range(columns_number):
        for v1, rect in enumerate(tiles_table[v]):
            if rect["rect"].collidepoint(cursor[0], cursor[1]) == 1:
                if game_state[v1][v] == 'Cov':
                    game_state[v1][v] = 'Flg'
                elif game_state[v1][v] == 'Flg':
                    game_state[v1][v] = 'Cov'


def failure():
    """
    handles player's failure - revealing the board and resetting game to main
    menu.

    no parameters

    result is being transported to main menu
    """
    myfont = pygame.font.Font('freesansbold.ttf', 100)
    fail_sign = myfont.render("You Exploded!", True, "Yellow")
    fail_sign_box = fail_sign.get_rect()
    fail_sign_box.center = arena.center
    for v in range(columns_number):
        for v1 in range(len(game_state[v])):
            game_state[v1][v] = 'UnCov'

    display_tiles(columns_number, rows_number, win, tiles_table, game_state, numbers_table, window)

    window.blit(fail_sign, fail_sign_box)
    pygame.display.flip()
    pygame.time.wait(4000)
    main_menu_and_game(ask)


def success_question_mark():
    """
    this function handles situation in which player wins - announcing it and
    returning to main menu.

    no parameters

    result is being transported to main menu
    """
    counter = 0
    for r in range(len(game_state)):
        for t in range(len(game_state[r])):
            if game_state[t][r] == "Cov" or game_state[t][r] == "Flg":
                counter += 1
    if counter == bombs_number:
        myfont = pygame.font.Font('freesansbold.ttf', 100)
        succ_sign = myfont.render("You Win!", True, "purple")
        succ_sign_box = succ_sign.get_rect()
        succ_sign_box.center = arena.center
        window.blit(succ_sign, succ_sign_box)
        pygame.display.flip()
        pygame.time.wait(4000)
        main_menu_and_game(ask)


def main_menu_and_game(asker):
    """
    the function is game's main loop - handles main menu and the game itself
    displaying tiles depending on variables and views time.

    takes 1 parameter as a "question" if he should continue onto the game

    each iteration manages blitting, revealing, counting time.
    """
    global columns_number
    global rows_number
    global bombs_number
    global numbers_table
    global coordinates_table
    global tiles_table
    global game_state

    timer = 0
    m_timer = 0
    current_time = time.time()
    prev_increase = current_time
    mainfont = pygame.font.Font('freesansbold.ttf', 60)
    secfont = pygame.font.Font('freesansbold.ttf', 40)
    thirdfont = pygame.font.Font('freesansbold.ttf', 20)
    while asker != 1:
        m_position = pygame.mouse.get_pos()
        window.fill("black")
        welcome_sign = mainfont.render("Welcome to minesweeper!", True, "red")
        welcome_sign_box = welcome_sign.get_rect()
        welcome_sign_box.center = (arena.center[0], arena.center[1] / 2)
        option_1 = secfont.render("Play!", True, "white")
        option_1_box = option_1.get_rect()
        option_1_box.center = arena.center
        option_2 = secfont.render("Options", True, "white")
        option_2_box = option_2.get_rect()
        option_2_box.center = (arena.centery + 50, arena.centerx + 100)
        window.blit(welcome_sign, welcome_sign_box)
        window.blit(option_1, option_1_box)
        window.blit(option_2, option_2_box)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse = pygame.mouse.get_pressed()
                if mouse[0]:
                    if mouse_on_menu(option_2_box, m_position):
                        pygame.display.flip()
                        options()
                    if mouse_on_menu(option_1_box, m_position):
                        asker = 1
                        numbers_table = all_da_tables(columns_number,
                                                      rows_number, bombs_number)

                        coordinates_table = [
                            [(0, 0) for _ in range(columns_number)] for _ in
                            range(rows_number)]

                        for c_ in range(columns_number):
                            for d_ in range(rows_number):
                                coordinates_table[c_][d_] = \
                                    ((((win[0] - 100) / columns_number) * c_) +
                                     (win[0] - 100) / (columns_number * 2),
                                     (win[1] / (columns_number * 2) +
                                      (win[1] / rows_number) * d_))

                        print(coordinates_table)
                        for a in range(len(numbers_table)):
                            print(numbers_table[a])

                        tile_ = {"file": "undiscovered.png"}

                        tiles_table = [[tile_ for _ in range(columns_number)] for
                                       _ in range(rows_number)]

                        for i_ in range(len(tiles_table)):
                            for g_, field_ in enumerate(tiles_table[i_]):
                                field_["surf"] = pygame.image.load(tile_["file"])
                                field_["surf"] = pygame.transform.scale(
                                    field_["surf"], ((win[0] - 100) /
                                                     columns_number,
                                                     win[1] / rows_number))
                                field_["rect"] = field_["surf"].get_rect()
                                field_["rect"].center = coordinates_table[i_][g_]
                                tiles_table[i_][g_] = tile_.copy()

                        game_state = [['Cov' for _ in range(columns_number)] for
                                      _ in range(rows_number)]
        pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_press = pygame.mouse.get_pressed()
                if mouse_press[0]:
                    reveal()
                if mouse_press[2]:
                    flag()

        current_time = time.time()
        if (current_time - prev_increase) >= 1:
            timer += 1
            prev_increase = current_time
            if timer == 60:
                timer = 0
                m_timer += 1

        window.fill("black")
        time_display = thirdfont.render("time:", True, "white")
        time_display_box = time_display.get_rect()
        time_display_box.center = (850, 25)
        seconds = thirdfont.render(str(timer) + " sec", True, "blue")
        seconds_box = seconds.get_rect()
        seconds_box.center = (time_display_box.centerx, time_display_box[1] +
                              30)
        minutes = thirdfont.render(str(m_timer) + " min", True, "blue")
        minutes_box = minutes.get_rect()
        minutes_box.center = (time_display_box.centerx, time_display_box[1] +
                              60)
        bomb_display = thirdfont.render("bombs", True, "white")
        bomb_display_box = bomb_display.get_rect()
        bomb_display_box.center = (win[0] - 50, win[1] - 100)
        bomb_display1 = thirdfont.render("hidden:", True, "white")
        bomb_display1_box = bomb_display1.get_rect()
        bomb_display1_box.center = (win[0] - 50, win[1] - 75)
        bomb_display_num = thirdfont.render(str(bombs_number), True, "blue")
        bomb_display_num_box = bomb_display_num.get_rect()
        bomb_display_num_box.center = (win[0] - 50, win[1] - 50)

        display_tiles(columns_number, rows_number, win, tiles_table, game_state, numbers_table, window)

        window.blit(time_display, time_display_box)
        window.blit(seconds, seconds_box)
        window.blit(minutes, minutes_box)
        window.blit(bomb_display, bomb_display_box)
        window.blit(bomb_display1, bomb_display1_box)
        window.blit(bomb_display_num, bomb_display_num_box)

        success_question_mark()
        pygame.display.flip()


def display_tiles(columns_number_, rows_number_, win_, tiles_table_, game_state_, numbers_table_, window_):
    """
    Display tiles on the game window based on game state and numbers table.

    Args:
    - columns_number: Number of columns in the game.
    - rows_number: Number of rows in the game.
    - win: Tuple containing the width and height of the game window.
    - tiles_table: List of dictionaries containing information about tiles.
    - game_state: List representing the current state of the game.
    - numbers_table: List representing the numbers on the tiles.
    - window: Pygame window surface.

    Returns:
    - None
    """
    image_mapping = {
        'Cov': "undiscovered.png",
        'Flg': "flag.png",
        'UnCov': {
            0: "empty.png",
            1: "one.png",
            2: "two.png",
            3: "three.png",
            4: "four.png",
            5: "five.png",
            6: "six.png",
            7: "seven.png",
            8: "eight.png",
            'X': "bomb.png"
        }
    }

    for i_ in range(columns_number_):
        for k, rect in enumerate(tiles_table_[i_]):
            if game_state_[k][i_] in image_mapping:
                if game_state_[k][i_] == 'UnCov':
                    image_filename = image_mapping[game_state_[k][i_]].get(numbers_table_[k][i_], None)
                else:
                    image_filename = image_mapping[game_state_[k][i_]]

                if image_filename:
                    rect["surf"] = pygame.image.load(image_filename)
                    rect["surf"] = pygame.transform.scale(rect["surf"],
                                                          ((win_[0] - 100) / columns_number_,
                                                           win_[1] / rows_number_))
                    window_.blit(rect["surf"], rect["rect"])


def mouse_on_menu(rect, m_pos):
    """
    this function is responsible for detecting mouse's position, and if it
    collides with a rectangle - returns positive.

    takes a rectangles and mouse position as parameters

    result is true or false - if collision exists
    """
    pygame.event.get()
    if rect.collidepoint(m_pos[0], m_pos[1]):
        return True
    else:
        return False


def how_to_play():
    """
    this function is responsible only for displaying texts how to play

    no parameters

    result is just text
    """
    asker = 0
    global columns_number
    global rows_number
    global bombs_number
    while asker != 1:
        m_position = pygame.mouse.get_pos()
        window.fill("black")
        mainfont = pygame.font.Font('freesansbold.ttf', 25)
        back_button = mainfont.render("Return", True, "red")
        back_button_box = back_button.get_rect()
        back_button_box.topleft = (25, 25)
        left_click = mainfont.render("Left click to reveal a tile:", True,
                                     "white")
        left_click_box = left_click.get_rect()
        left_click_box.center = (arena.centerx, 100)
        left_click_con = mainfont.render("empty or a number - "
                                         "informs you how many bombs are "
                                         "around the tile", True, "red")
        left_click_con_box = left_click_con.get_rect()
        left_click_con_box.center = (arena.centerx, 150)
        left_click_con1 = mainfont.render("bomb - you lose!", True, "red")
        left_click_con1_box = left_click_con1.get_rect()
        left_click_con1_box.center = (arena.centerx, 200)
        right_click = mainfont.render("Right click to mark a tile with a flag "
                                      "- potential bomb", True, "white")
        right_click_box = right_click.get_rect()
        right_click_box.center = (arena.centerx, 250)
        win_con = mainfont.render("uncover all tiles without exploding to "
                                  "win!", True, "white")
        win_con_box = win_con.get_rect()
        win_con_box.center = (arena.centerx, 500)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse = pygame.mouse.get_pressed()
                if mouse[0]:
                    if mouse_on_menu(back_button_box, m_position):
                        asker = 1
        window.blit(back_button, back_button_box)
        window.blit(left_click, left_click_box)
        window.blit(left_click_con, left_click_con_box)
        window.blit(left_click_con1, left_click_con1_box)
        window.blit(right_click, right_click_box)
        window.blit(win_con, win_con_box)
        pygame.display.flip()

    options()


def adjust_game_settings(m_position, bombs_increaser_box, bombs_decreaser_box, board_increaser_box, board_decreaser_box,
                         how_to_box, back_button_box):
    global bombs_number
    global columns_number
    global rows_number

    if mouse_on_menu(bombs_increaser_box, m_position) and bombs_number < (pow(columns_number, 2) - 1):
        bombs_number += 1
    if mouse_on_menu(bombs_decreaser_box, m_position) and bombs_number > 1:
        bombs_number -= 1
    if mouse_on_menu(board_increaser_box, m_position) and columns_number < 20:
        columns_number += 1
        rows_number += 1
    if mouse_on_menu(board_decreaser_box, m_position) and columns_number > 2:
        columns_number -= 1
        rows_number -= 1
        if bombs_number > pow(columns_number, 2):
            bombs_number = pow(columns_number, 2) - 1
    if mouse_on_menu(how_to_box, m_position):
        how_to_play()
    if mouse_on_menu(back_button_box, m_position):
        return 1


def options():
    """
    this function manages the whole options screen - increasing or ecreasing
    varibale depending on user's wish.

    no parameters

    result is whole options screen and eventual change of variables
    """
    asker = 0
    global columns_number
    global rows_number
    global bombs_number
    while asker != 1:
        m_position = pygame.mouse.get_pos()
        window.fill("black")
        mainfont = pygame.font.Font('freesansbold.ttf', 30)
        back_button = mainfont.render("Return", True, "red")
        back_button_box = back_button.get_rect()
        back_button_box.topleft = (25, 25)
        board_size_mess = mainfont.render("Board size:", True, "red")
        board_size_mess_box = board_size_mess.get_rect()
        board_size_mess_box.center = (arena.center[0] / 2, arena.center[1])
        bombs_mess = mainfont.render("Bombs number:", True, "red")
        bombs_mess_box = bombs_mess.get_rect()
        bombs_mess_box.center = ((arena.center[0] / 2) * 3, arena.center[1])

        bombs = mainfont.render(str(bombs_number), True, "white")
        bombs_box = bombs.get_rect()
        bombs_box.center = ((arena.center[0] / 2) * 3, arena.center[1] + 100)

        board = mainfont.render(str(columns_number) + "X" + str(
            columns_number), True, "white")
        board_box = board.get_rect()
        board_box.center = (arena.center[0] / 2, arena.center[1] + 100)

        board_decreaser = mainfont.render("-1", True, "white")
        board_decreaser_box = board_decreaser.get_rect()
        board_decreaser_box.midright = (board_box.left - 30,
                                        board_box.center[1])
        board_increaser = mainfont.render("+1", True, "white")
        board_increaser_box = board_increaser.get_rect()
        board_increaser_box.midleft = (board_box.right + 30,
                                       board_box.center[1])
        bombs_decreaser = mainfont.render("-1", True, "white")
        bombs_decreaser_box = bombs_decreaser.get_rect()
        bombs_decreaser_box.midright = (bombs_box.left - 30,
                                        bombs_box.center[1])
        bombs_increaser = mainfont.render("+1", True, "white")
        bombs_increaser_box = bombs_increaser.get_rect()
        bombs_increaser_box.midleft = (bombs_box.right + 30,
                                       board_box.center[1])
        how_to = mainfont.render("How to play?", True, "red")
        how_to_box = how_to.get_rect()
        how_to_box.center = (win[1], back_button_box.centery)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.MOUSEWHEEL:
                mouse = pygame.mouse.get_pressed()
                if mouse[0]:
                    asker = adjust_game_settings(m_position, bombs_increaser_box, bombs_decreaser_box,
                                                 board_increaser_box, board_decreaser_box, how_to_box, back_button_box)
            if event.type == pygame.MOUSEWHEEL:
                asker = adjust_game_settings(m_position, bombs_increaser_box, bombs_decreaser_box, board_increaser_box,
                                             board_decreaser_box, how_to_box, back_button_box)

        window.blit(board, board_box)
        window.blit(board_size_mess, board_size_mess_box)
        window.blit(board_increaser, board_increaser_box)
        window.blit(board_decreaser, board_decreaser_box)

        window.blit(bombs, bombs_box)
        window.blit(bombs_mess, bombs_mess_box)
        window.blit(bombs_increaser, bombs_increaser_box)
        window.blit(bombs_decreaser, bombs_decreaser_box)

        window.blit(back_button, back_button_box)
        window.blit(how_to, how_to_box)
        pygame.display.flip()


if __name__ == "__main__":
    pygame.init()
    win = (900, 800)
    window = pygame.display.set_mode(win)
    arena = window.get_rect()
    ask = 0
    columns_number = 8
    rows_number = 8
    bombs_number = 13

    numbers_table = all_da_tables(columns_number,
                                  rows_number, bombs_number)

    coordinates_table = [[(0, 0) for z in range(columns_number)] for
                         y in range(rows_number)]

    for c in range(columns_number):
        for d in range(rows_number):
            coordinates_table[c][d] = (
                ((win[0] / columns_number) * c) +
                win[0] / (columns_number * 2),
                ((win[1] / rows_number) * d) + win[1] / (
                        rows_number * 2))

    tile = {"file": "undiscovered.png"}

    tiles_table = [[tile for z in range(columns_number)] for
                   y in range(rows_number)]

    for i in range(len(tiles_table)):
        for g, field in enumerate(tiles_table[i]):
            field["surf"] = pygame.image.load(tile["file"])
            field["surf"] = pygame.transform.scale(
                field["surf"], (win[0] / columns_number,
                                win[1] / rows_number))
            field["rect"] = field["surf"].get_rect()
            field["rect"].center = coordinates_table[i][g]
            tiles_table[i][g] = tile.copy()

    game_state = [['Cov' for z in range(columns_number)] for y in range(
        rows_number)]

    main_menu_and_game(ask)
