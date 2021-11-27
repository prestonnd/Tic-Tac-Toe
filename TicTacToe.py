""""
A Simple Tic Tac Toe game by Preston D'Silva, 2020
"""

from random import choice
import pygame as p


p.init()
grid_width, grid_height, grid_score_board = 300, 300, 50
screen = p.display.set_mode((grid_width, grid_height + grid_score_board))
x_icon, o_icon = p.image.load('./x.png'), p.image.load('./o.png')
p.display.set_caption("Preston's Tic Tac Toe")

B = [[], [], []]
console_text_board = False
acceptable_keys = [p.K_0, p.K_1, p.K_2, p.K_KP0, p.K_KP1, p.K_KP2]
scores_list = []
computer_skill = 2


def switch_player(pl):
    list_of_players = ['player', 'computer']
    if pl == 'random_to_start':
        return choice(list_of_players)
    elif pl == 'computer':
        return 'player'
    elif pl == 'player':
        return 'computer'


def reset_board():
    for reset_loop in range(3):
        B[reset_loop] = [' ', ' ', ' ']


def draw_grid(ref):
    if ref == 'refresh_bg_true':
        screen.fill((255, 255, 255))
    else:
        x, y, side_length = 0, 0, 100
        for row_loop in range(3):
            for col_loop in range(3):
                p.draw.rect(screen, (0, 0, 255), (x, y, side_length, side_length), width=1)
                x += side_length
            x = 0
            y += side_length
    draw_score_board()


def hover_box(location):
    draw_grid('refresh_bg_false')
    x, y = int(location[0]/100) * 100, int(location[1]/100) * 100
    side_length = 100
    p.draw.rect(screen, (255, 43, 0), (x, y, side_length, side_length), width=1)


def draw_score_board():
    p.draw.rect(screen, (255, 255, 255), (0, 300, 300, 50), width=0)
    font = p.font.SysFont('None', 30)
    bottom_message_text = f'Player: {scores_list.count("player")} Computer: {scores_list.count("computer")} ' \
                          f'Tie: {scores_list.count("tie")}'
    message = font.render(bottom_message_text, True, (0, 0, 255))
    screen.blit(message, (0, 300))
    computer_skill_message = font.render(f'Computer skill level (0-2): {computer_skill}', True, (0, 0, 255))
    screen.blit(computer_skill_message, (0, 330))


def player_picks(location):
    """    converts player click to open spot on board    """
    if click_is_on_the_board:
        r, c = int(location[0]/100), int(location[1]/100)
        if B[c][r] == ' ':
            B[c][r] = 'X'
            return True


def computer_picks_random():  # random computer pick from open spots
    found_open_spot = False
    while not found_open_spot:
        coord = (0, 1, 2)
        grid_x, grid_y = choice(coord), choice(coord)
        if B[grid_x][grid_y] == ' ':
            B[grid_x][grid_y] = 'O'
            found_open_spot = True


def computer_skill_changer(key):
    """
    player can use 0, 1, 2 on the keyboard number row or keypad,
    returns 0,1 or 2.
    """
    if key == 48 or key == 1073741922:  # key 0 pressed
        return 0
    if key == 49 or key == 1073741913:  # key 1 pressed
        return 1
    if key == 50 or key == 1073741914:  # key 2 pressed
        return 2
    draw_score_board()


def computer_picks(x_or_o):
    """
    attribute is passed either 'X' or ' O'
    function will loop through the rows, then columns, then diagonals...
    ... looking for a set that has one blank spot
    depending on set computer skill level, function will either complete a set to win,
    or block a set, to stop the player.
    """
    for loop_row in range(3):
        if B[loop_row] == [x_or_o, x_or_o, ' ']:
            B[loop_row][2] = 'O'
            return True
        elif B[loop_row] == [' ', x_or_o, x_or_o]:
            B[loop_row][0] = 'O'
            return True
        elif B[loop_row] == [x_or_o, ' ', x_or_o]:
            B[loop_row][1] = 'O'
            return True
    for loop_col in range(3):  # check columns
        if B[0][loop_col] == x_or_o and B[1][loop_col] == x_or_o and B[2][loop_col] == ' ':
            B[2][loop_col] = 'O'
            return True
        elif B[0][loop_col] == x_or_o and B[2][loop_col] == x_or_o and B[1][loop_col] == ' ':
            B[1][loop_col] = 'O'
            return True
        elif B[1][loop_col] == x_or_o and B[2][loop_col] == x_or_o and B[0][loop_col] == ' ':
            B[0][loop_col] = 'O'
            return True
    # check diagonals
    if B[0][0] == x_or_o and B[1][1] == x_or_o and B[2][2] == ' ':
        B[2][2] = 'O'
        return True
    elif B[0][0] == x_or_o and B[2][2] == x_or_o and B[1][1] == ' ':
        B[1][1] = 'O'
        return True
    elif B[1][1] == x_or_o and B[2][2] == x_or_o and B[0][0] == ' ':
        B[0][0] = 'O'
        return True
    elif B[0][2] == x_or_o and B[1][1] == x_or_o and B[2][0] == ' ':
        B[2][0] = 'O'
        return True
    elif B[1][1] == x_or_o and B[2][0] == x_or_o and B[0][2] == ' ':
        B[0][2] = 'O'
        return True
    elif B[0][2] == x_or_o and B[2][0] == x_or_o and B[1][1] == ' ':
        B[1][1] = 'O'
        return True
    return False


def board_is_full():
    """    Checking the board(3 rows), for an empty spot    """
    return True if ' ' not in B[0] and ' ' not in B[1] and ' ' not in B[2] else False


def check_for_3(cell1, cell2, cell3):
    """    Checking if 3 cells are the same    """
    return True if cell1 == cell2 and cell1 == cell3 and cell1 != ' ' else False


def draw_line(orientation, pos):
    """Draw a line to show a completed set"""
    if orientation == 'row':
        p.draw.line(screen, (0, 0, 255), (0, pos * 100 + 50), (300, pos * 100 + 50), width=5)
    if orientation == 'col':
        p.draw.line(screen, (0, 0, 255), (pos * 100 + 50, 0), (pos * 100 + 50, 300), width=5)
    if orientation == 'diagonal_right':
        p.draw.line(screen, (0, 0, 255), (0, 0), (300, 300), width=5)
    if orientation == 'diagonal_left':
        p.draw.line(screen, (0, 0, 255), (0, 300), (300, 0), width=5)


def there_is_winner():
    for loop_row in range(3):  # check rows
        if check_for_3(B[loop_row][0], B[loop_row][1], B[loop_row][2]):
            draw_line('row', loop_row)
            return True
    for loop_col in range(3):  # check columns
        if check_for_3(B[0][loop_col], B[1][loop_col], B[2][loop_col]):
            draw_line('col', loop_col)
            return True
    if check_for_3(B[0][0], B[1][1], B[2][2]):
        draw_line('diagonal_right', 0)
        return True
    elif check_for_3(B[0][2], B[1][1], B[2][0]):
        draw_line('diagonal_left', 0)
        return True
    else:
        return False


def there_is_a_tie():
    if board_is_full():  # check for a draw / draw a big x
        draw_line('diagonal_right', 0)
        draw_line('diagonal_left', 0)
        draw_score_board()
        return True


def add_to_scores_list(passed_player):
    scores_list.append(passed_player)


def display_plays():
    for loop_row in range(3):
        for loop_col in range(3):
            if B[loop_col][loop_row] == 'X':
                screen.blit(x_icon, (loop_row * 100, loop_col * 100))
            if B[loop_col][loop_row] == 'O':
                screen.blit(o_icon, (loop_row * 100, loop_col * 100))


def text_board():
    if console_text_board:
        print(f'Player: {scores_list.count("player")} Computer: {scores_list.count("computer")} '
              f'Tie: {scores_list.count("tie")}')
        print(f'Computer skill level (0-2): {computer_skill}')
        print(f'Current player: {current_player}')
        for loop in B:
            print(loop)
        print('\n')


def play(pl, location):
    if pl == 'computer':
        if computer_skill == 2:
            if not computer_picks('O'):
                if not computer_picks('X'):
                    computer_picks_random()
        elif computer_skill == 1:
            if not computer_picks('X'):
                computer_picks_random()
        else:
            computer_picks_random()
        text_board()
        display_plays()
        return True
    if pl == 'player' and player_picks(location):
        text_board()
        display_plays()
        return True
    return False


def do_all_the_resets():
    global current_player
    current_player = switch_player('random_to_start')
    reset_board()
    draw_grid('refresh_bg_true')


current_player = switch_player('random_to_start')
click_is_on_the_board = False
click_location = (0, 301)
game_over = False
do_all_the_resets()


running = True
while running:
    if not game_over:
        for event in p.event.get():
            if event.type == p.QUIT:
                quit()
            if event.type == p.KEYDOWN:
                if event.key == p.K_t:
                    console_text_board = not console_text_board
                if event.key in acceptable_keys:
                    computer_skill = computer_skill_changer(event.key)
            if event.type == p.MOUSEBUTTONDOWN:
                click_location = p.mouse.get_pos()
                click_is_on_the_board = True if click_location[1] < grid_height else False
            hover_box(p.mouse.get_pos())
        if play(current_player, click_location):
            if there_is_winner():
                add_to_scores_list(current_player)
                game_over = True
            elif there_is_a_tie() and not there_is_winner():
                add_to_scores_list('tie')
                game_over = True
            else:
                current_player = switch_player(current_player)
    elif game_over:
        for wait in p.event.get():
            if wait.type == p.QUIT:
                quit()
            if wait.type == p.MOUSEBUTTONDOWN:
                do_all_the_resets()
                game_over = False
                click_is_on_the_board = False
    draw_score_board()
    p.display.update()
