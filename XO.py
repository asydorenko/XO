import pygame, random, copy, pickle, os

from pygame.locals import (
    RLEACCEL,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
    MOUSEBUTTONDOWN 
)

f = [True] * 9
cell_rec = [0] * 9
matrix = [[-1,-1,-1], [-1,-1,-1], [-1,-1,-1]]
X_PLAYER = 1
O_PLAYER = 0
node_list = []
computer_turn = False
WINS = LOSES = TIES = 0
move_was_made = False
game_over = False
grid = {0: (0,0), 1: (0,1), 2: (0,2), 3: (1,0), 4: (1,1), 5: (1,2), 6: (2,0), 7: (2,1), 8: (2,2)}
game_over_grid = { "h_line_0": False, "h_line_1": False, "h_line_2": False, "v_line_0": False, "v_line_1": False, "v_line_2": False, "l_line": False, "r_line": False }

class Node:
    def __init__(self, state, player, xy):

        self.children = []

        self.player = player

        self.state = copy.deepcopy(state)

        self.xy = xy


def is_win(m):
    global game_over_grid
    if (m[0][0] == m[0][1] == m[0][2] == "X"):
        game_over_grid["h_line_0"] = True
        return (True, 1)
    elif (m[1][0] == m[1][1] == m[1][2] == "X"):
        game_over_grid["h_line_1"] = True
        return (True, 1)
    elif (m[2][0] == m[2][1] == m[2][2] == "X"):
        game_over_grid["h_line_2"] = True
        return (True, 1)
    elif (m[0][0] == m[1][1] == m[2][2] == "X"):
        game_over_grid["l_line"] = True
        return (True, 1)
    elif (m[0][2] == m[1][1] == m[2][0] == "X"):
        game_over_grid["r_line"] = True
        return (True, 1)
    elif (m[0][0] == m[1][0] == m[2][0] == "X"):
        game_over_grid["v_line_0"] = True
        return (True, 1)
    elif (m[0][1] == m[1][1] == m[2][1] == "X"):
        game_over_grid["v_line_1"] = True
        return (True, 1)
    elif (m[0][2] == m[1][2] == m[2][2] == "X"):
        game_over_grid["v_line_2"] = True
        return (True, 1)
    elif (m[0][0] == m[0][1] == m[0][2] == 0):
        game_over_grid["h_line_0"] = True
        return (True, 0)
    elif (m[1][0] == m[1][1] == m[1][2] == 0):
        game_over_grid["h_line_1"] = True
        return (True, 0)
    elif (m[2][0] == m[2][1] == m[2][2] == 0):
        game_over_grid["h_line_2"] = True
        return (True, 0)
    elif (m[0][0] == m[1][1] == m[2][2] == 0):
        game_over_grid["l_line"] = True
        return (True, 0)
    elif (m[0][2] == m[1][1] == m[2][0] == 0):
        game_over_grid["r_line"] = True
        return (True, 0)
    elif (m[0][0] == m[1][0] == m[2][0] == 0):
        game_over_grid["v_line_0"] = True
        return (True, 0)
    elif (m[0][1] == m[1][1] == m[2][1] == 0):
        game_over_grid["v_line_1"] = True
        return (True, 0)
    elif (m[0][2] == m[1][2] == m[2][2] == 0):
        game_over_grid["v_line_2"] = True
        return (True, 0)
    else:
        return (False, -1)

def is_tie(m):
    if (len(get_empty_cells(m)) == 0) and (is_win(m) == (False, -1)):
        return True
    else:
        return False

def get_empty_cells(m):
    x = []
    for i in range(3):
        for j in range(3):
            if m[i][j] == -1:
                x.append((i,j))
    return x

def build_tree(node):
    if (is_win(node.state)[0] == True) or (is_tie(node.state)):
        return

    if node.player == X_PLAYER:
        open_cells = get_empty_cells(node.state)
        for i in open_cells:
            node.state[i[0]][i[1]] = "X"
            node.children.append(Node(copy.deepcopy(node.state), O_PLAYER, (i[0], i[1])))
            node.state[i[0]][i[1]] = -1

    if node.player == O_PLAYER:
        open_cells = get_empty_cells(node.state)
        for i in open_cells:
            node.state[i[0]][i[1]] = 0
            node.children.append(Node(copy.deepcopy(node.state), X_PLAYER, (i[0], i[1])))
            node.state[i[0]][i[1]] = -1

    node_list.append(node)

    for child in node.children:
        build_tree(child)

def next_move(node):
    global init_player
    if is_win(node.state) == (True, 1):
        return (node.xy, 1)
    elif is_win(node.state) == (True, 0):
        return (node.xy, -100)
    elif is_tie(node.state):
        return (node.xy, 0)

    if node.player == X_PLAYER: 
        value = -1
        best_move = (-1,-1)
        for n in node.children:
            x, y = next_move(n)
            if y > value:
                best_move = n.xy
                value = y
        return (best_move, value)

    elif node.player == O_PLAYER: 
        value = 100
        best_move = (-1,-1)
        moves = []
        for n in node.children:
            x, y = next_move(n)
            if y < value:
                best_move = n.xy
                value = y
        return (best_move, value)

def computer_move(xy):
    global f
    index = -1
    x, y = xy
    matrix[x][y] = "X"
    for key, value in grid.items():
        if xy == value:
            index = key
    cells[index].blit(X, ((150-X.get_width())/2, (150-X.get_height())/2))
    f[index] = False

def player_move(cell, index):
    global matrix
    cell.blit(O, ((150-O.get_width())/2, (150-O.get_height())/2))
    x, y = grid[index]
    matrix[x][y] = 0

def clear_game():
    global f, matrix, player, computer_turn
    f = [True] * 9
    computer_turn = False
    move_was_made = False
    player = random.randint(0, 1)
    matrix = [ [-1,-1,-1], [-1,-1,-1], [-1,-1,-1] ]
    print("Clearing")
    print(matrix)
    for cell in cells:
        cell.fill((135, 206, 250))
    score_board.fill((204, 255, 255))
    print("PLAYER = ", player)
    if player == 0:
        display_message("You go first", 60)
    else:
        display_message("Computer goes first", 40)
    if player == 1:
        #n_m = next_move(root)
        n_m = (random.randint(0,2), random.randint(0,2))
        computer_move(n_m)
        print("Comp next move from clear = ", n_m)
        computer_turn = False

def reverse_matrix():
    global matrix
    for i in range(3):
        for j in range(3):
            if matrix[i][j] == "X":
                matrix[i][j] = 0
            elif matrix[i][j] == 0:
                matrix[i][j] = "X"

def update_screen():
    board.fill((0,0,0))
    cell_rec[0] = board.blit(cells[0], (0,0))
    cell_rec[1] = board.blit(cells[1], (165, 0))
    cell_rec[2] = board.blit(cells[2], (330, 0))
    cell_rec[3] = board.blit(cells[3], (0, 165))
    cell_rec[4] = board.blit(cells[4], (165, 165))
    cell_rec[5] = board.blit(cells[5], (330, 165))
    cell_rec[6] = board.blit(cells[6], (0, 330))
    cell_rec[7] = board.blit(cells[7], (165, 330))
    cell_rec[8] = board.blit(cells[8], (330, 330))

    score_board.fill((204, 255, 255))
    text = "     Wins: " + str(WINS) + "          Loses: " + str(LOSES) + "          Ties: " + str(TIES)
    text_surface = font.render(text, True, (0,0,0))
    score_board.blit(text_surface, (0,0))

    screen.fill((135, 206, 250))
    screen.blit(score_board, (0,0))
    screen.blit(board, board_center)
    pygame.display.flip()

def display_message(text, size):
    message_board.fill((0,0,0))
    font = pygame.font.Font(pygame.font.match_font('kristen_itc'), size)
    text_surface = font.render(text, True, (255,255,255))
    message_board.blit(text_surface, (((message_board.get_width()-text_surface.get_width())/2, (message_board.get_height()-text_surface.get_height())/2)))
    screen.blit(message_board, ((SCREEN_WIDTH-message_board.get_width())/2, (SCREEN_HEIGHT-message_board.get_height())/2+30))
    pygame.display.flip()
    pygame.time.wait(2000)

def cross_win():
    global game_over_grid
    print(game_over_grid)
    win_cells = ""
    for key, value in game_over_grid.items():
        if value == True:
            win_cells = key
            game_over_grid[key] = False
            break

    x, y = board_center

    if win_cells == "h_line_0":
        board.blit(h_line, (x-50, y-15))
    if win_cells == "h_line_1":
        board.blit(h_line, (x-50, y+150))
    if win_cells == "h_line_2":
        board.blit(h_line, (x-50, y+315))
    if win_cells == "v_line_0":
        board.blit(v_line, (x+37,y-80))
    if win_cells == "v_line_1":
        board.blit(v_line, (x+202, y-80))
    if win_cells == "v_line_2":
        board.blit(v_line, (x+367, y-80))
    if win_cells == "l_line":
        board.blit(l_line, (x-30, y-80))
    if win_cells == "r_line":
        board.blit(r_line, (x-50, y-80))

    print("win cell: ", win_cells)
    screen.blit(board, board_center)
    pygame.display.flip()
    pygame.time.wait(1000)


SCREEN_WIDTH = 550
SCREEN_HEIGHT = 600

pygame.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

board = pygame.Surface((480, 480))
board_rect = board.get_rect()

score_board = pygame.Surface((550, 50))
score_board.fill((204, 255, 255))

message_board = pygame.Surface((550, 100))
message_board.fill((0,0,0))

font = pygame.font.Font(pygame.font.match_font('arial'), 36)
text = "Wins: " + str(WINS) + "          Loses: " + str(LOSES) + "          Ties: " + str(TIES)
text_surface = font.render(text, True, (0,0,0))
score_board.blit(text_surface, (0,0))

X = pygame.image.load(os.path.join(os.getcwd(), "x.jpg")).convert()
O = pygame.image.load(os.path.join(os.getcwd(), "o.jpg")).convert()
v_line = pygame.image.load(os.path.join(os.getcwd(), "vertical_line.png")).convert()
h_line = pygame.image.load(os.path.join(os.getcwd(), "horizontal_line.png")).convert()
l_line = pygame.image.load(os.path.join(os.getcwd(), "diagonal_line_left.png")).convert()
r_line = pygame.image.load(os.path.join(os.getcwd(), "diagonal_line_right.png")).convert()
v_line.set_colorkey((255, 255, 255), RLEACCEL)
h_line.set_colorkey((255, 255, 255), RLEACCEL)
l_line.set_colorkey((255, 255, 255), RLEACCEL)
r_line.set_colorkey((255, 255, 255), RLEACCEL)

cells = []

for i in range(9):
    cells.append(pygame.Surface((150, 150)))
    cells[i].fill((135, 206, 250))

screen.fill((135, 206, 250))
board.fill((0, 0, 0))
board_center = (
    (SCREEN_WIDTH-board.get_width())/2,
    (SCREEN_HEIGHT-board.get_height())/2+25
)

init_player = random.randint(0, 1)
player = init_player
print("PLAYER = ", init_player)
root = Node(matrix, init_player, None)
#node_list.append(root)
build_tree(root)
#file_x = open("xo_data", "wb")
#pickle.dump(node_list, file_x)
#file_x = open(os.path.join(os.getcwd(), "xo_data"), "rb")
#node_list = pickle.load(file_x)
#root = node_list[0]
print(len(root.children))
player_text = ""
if player == 0:
    display_message("You go first", 60)
else:
    display_message("Computer goes first", 40)

if init_player == 1:
    computer_move((random.randint(0,2), random.randint(0,2)))
    computer_turn = False

running = True

while running:
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
        elif event.type == QUIT:
            running = False
        elif event.type == MOUSEBUTTONDOWN and computer_turn == False:
            x,y = pygame.mouse.get_pos()
            for i in range(0, len(cells)):
                if cell_rec[i].collidepoint((x-35, y-85)) and f[i]:
                    print("collide with cell ", i)
                    f[i] = False
                    move_was_made = True
                    player_move(cells[i], i)
                    break
            game_over_grid = { "h_line_0": False, "h_line_1": False, "h_line_2": False, "v_line_0": False, "v_line_1": False, "v_line_2": False, "l_line": False, "r_line": False }
            if is_win(matrix) == (True, 0):
                WINS += 1
                update_screen()
                pygame.time.wait(1000)
                cross_win()
                display_message("Congratulations, you won!!", 50)
                print("Congratulations, you won!!")
                print(matrix)
                clear_game()
            elif is_tie(matrix):
                TIES += 1
                update_screen()
                pygame.time.wait(1000)
                display_message("It's a tie", 60)
                print("It's a tie")
                print(matrix)
                clear_game()
            else:
                if move_was_made:
                    update_screen()
                    computer_turn = True
                    pygame.time.wait(1000)
                    print ("computer's turn = ", computer_turn)
                    move_was_made = False
    
    if computer_turn:
        if player != init_player:
            reverse_matrix()
        for n in node_list:
            if n.state == matrix:
                if player != init_player:
                    reverse_matrix()
                print("match found")
                move = next_move(n)
                print(move)
                computer_move(move[0])
                computer_turn = False
                print(matrix)
                game_over_grid = { "h_line_0": False, "h_line_1": False, "h_line_2": False, "v_line_0": False, "v_line_1": False, "v_line_2": False, "l_line": False, "r_line": False }
                if is_win(matrix) == (True, 1):
                    LOSES += 1
                    update_screen()
                    pygame.time.wait(1000)
                    cross_win()
                    display_message("You lost!!", 60)
                    print("You lost!!")
                    print(matrix)
                    clear_game()
                if is_tie(matrix):
                    TIES += 1
                    update_screen()
                    pygame.time.wait(1000)
                    display_message("It's a tie", 60)
                    print("It's a tie")
                    print(matrix)
                    clear_game()
                break
            
    update_screen()