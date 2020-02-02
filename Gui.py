import pygame
import time

class Gui:
    screen_width = 400
    screen_height = 400
    info_screen_height = 50  # for little section under the board

    blocks = []             # holds the current value for each block
    solution_board = []     # holds solution which is obtained from the backtracking algorithm
    game_board = []         # holds the current board

    # initialize colors
    white = (255, 255, 255)
    black = (0, 0, 0)
    blue = (0, 0, 255)
    red = (255, 0, 0)
    green = (0, 255, 0)

    show_text_x = True  # use this variable to determine whether to display text under board or solution msg
    x_array = [0, 10]   # number of errors, position for x to display
    space_bar_text = "press space bar to solve"

    pygame.init()

    gameDisplay = pygame.display.set_mode((screen_width, screen_height + info_screen_height))
    pygame.display.set_caption('Sudoku')
    number_font = pygame.font.SysFont("Calibri", 50)
    x_font = pygame.font.SysFont("Arial", 40)
    msg_font = pygame.font.SysFont("Arial", 20)
    end_game_font = pygame.font.SysFont("Arial", 40)

    # ******************************************************************
    # pass in the solution board that the backtracking algorithm solved
    # also pass in the starting game board
    # ******************************************************************
    def __init__(self, solution, game):
        self.solution_board = solution
        self.game_board = game

    # draw grid on board
    def draw_lines(self):
        next_line = 0
        for i in range(10):
            # vertical
            pygame.draw.line(self.gameDisplay, self.black, [next_line, 0], [next_line, self.screen_height])
            # thick lines
            if i % 3 == 0 and i <= 9 and i != 0:
                pygame.draw.line(self.gameDisplay, self.black, [next_line, 0], [next_line, self.screen_height], 3)

            # horizontal
            pygame.draw.line(self.gameDisplay, self.black, [0, next_line], [self.screen_width, next_line])
            # thick lines
            if i % 3 == 0 and i <= 9 and i != 0:
                pygame.draw.line(self.gameDisplay, self.black, [0, next_line], [self.screen_width, next_line], 3)

            next_line += self.screen_width / 9

    # initialize the blocks array that stores the dimensions for the individual blocks on the Sudoku board
    def make_blocks(self):
        top = 0
        bottom = self.screen_height / 9
        left = 0
        right = self.screen_width / 9

        # 1 - 81
        cube_num = 0

        # math
        for row in range(9):
            for col in range(9):
                value = self.game_board[row][col]
                cube_num += 1
                self.blocks.append([cube_num, left, right, top, bottom, value])

                left = right
                right += self.screen_width / 9

            top = bottom
            bottom += self.screen_height / 9
            left = 0
            right = self.screen_height / 9

    # return the cube number that was selected by the courser
    def get_cube_number(self, mx, my):

        for cell in self.blocks:
            top = cell[3]
            bottom = cell[4]
            left = cell[1]
            right = cell[2]

            if (my > top) and (my < bottom):
                if (mx > left) and (mx < right):
                    return cell
        print("error: no cube found")

    # highlight selected cube based off of cubeNumber
    def select_cube(self, cube_number):  # color determines what color to highlight cube in

        # the prevents highlighting of multiple cubes at the same time
        self.gameDisplay.fill(self.white)
        self.draw_lines()

        for i in self.blocks:
            if i[0] == cube_number:
                left = i[1]
                right = i[2]
                top = i[3]
                bottom = i[4]

                pygame.draw.line(self.gameDisplay, self.blue, [left, top], [right, top], 2)
                pygame.draw.line(self.gameDisplay, self.blue, [left, bottom], [right, bottom], 2)
                pygame.draw.line(self.gameDisplay, self.blue, [left, top], [left, bottom], 2)
                pygame.draw.line(self.gameDisplay, self.blue, [right, top], [right, bottom], 2)

                return i[0]  # return selected cube number
        return -1

    # if the cube is correct then highlight green. else use red
    def highlight_color(self, cube_number, is_correct):
        for i in self.blocks:
            if i[0] == cube_number:
                left = i[1]
                right = i[2]
                top = i[3]
                bottom = i[4]
                if is_correct:
                    pygame.draw.line(self.gameDisplay, self.green, [left, top], [right, top], 2)
                    pygame.draw.line(self.gameDisplay, self.green, [left, bottom], [right, bottom], 2)
                    pygame.draw.line(self.gameDisplay, self.green, [left, top], [left, bottom], 2)
                    pygame.draw.line(self.gameDisplay, self.green, [right, top], [right, bottom], 2)
                else:
                    pygame.draw.line(self.gameDisplay, self.red, [left, top], [right, top], 2)
                    pygame.draw.line(self.gameDisplay, self.red, [left, bottom], [right, bottom], 2)
                    pygame.draw.line(self.gameDisplay, self.red, [left, top], [left, bottom], 2)
                    pygame.draw.line(self.gameDisplay, self.red, [right, top], [right, bottom], 2)

    # render sudoku board on gui
    def render_text(self):

        text = self.msg_font.render(self.space_bar_text, True, self.black)
        self.gameDisplay.blit(text, (self.screen_width - 180, self.screen_height + 10))

        # add one x for every answer you got wrong
        self.x_array[1] = 10
        height_of_x = self.screen_height
        for x in range(self.x_array[0]):
            # go to new line
            if self.x_array[1] > 200:
                self.x_array[1] = 10
                height_of_x += 20

            text = self.msg_font.render("X", True, self.red)
            self.gameDisplay.blit(text, (self.x_array[1], height_of_x))
            self.x_array[1] += 25

        next_x = -self.screen_width / 9 / 2
        next_y = -self.screen_height / 9

        for i in self.blocks:
            if i[5] != 0:
                text = self.number_font.render(str(i[5]), True, self.black)
            else:
                text = self.number_font.render(" ", True, self.black)

            self.gameDisplay.blit(text, (self.screen_width / 9 + next_x - text.get_rect().width / 2, self.screen_height / 9 + next_y))
            next_x += self.screen_width / 9

            if i[0] % 9 == 0:
                next_x = -self.screen_width / 9 / 2
                next_y += self.screen_height / 9

    # checks if user input is correct
    def test_input(self, block_num, user_input):

        # check if the current block already has a value
        for i in self.blocks:
            if i[0] == block_num:
                if i[5] != 0:  # has to be 0 to enter a number
                    return False

        count = 1
        for row in range(9):
            for col in range(9):
                if count == block_num:  # if you are on the right cube
                    return self.solution_board[row][col] == user_input
                count += 1
        return False

    # adds user input to board
    def add_solution(self, cube_num, solution):
        for i in self.blocks:
            if int(i[0]) == cube_num:
                # add solution to array for solutions
                i[5] = solution

    def process_input(self, current_block, number):
        print("pressed ", number)
        if self.test_input(current_block, number):
            print("is solution")
            self.highlight_color(current_block, True)
            self.add_solution(current_block, number)
        else:
            self.x_array[0] += 1
            self.highlight_color(current_block, False)


    def start_gui(self):

        current_block = -1  # -1 means there is no cube selected

        # initialize board
        self.gameDisplay.fill(self.white)
        self.draw_lines()

        # initialize boxes
        self.make_blocks()

        exit_game = False

        while not exit_game:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()


                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mx, my = pygame.mouse.get_pos()
                    cube = self.get_cube_number(mx, my)
                    current_block = self.select_cube(cube[0])

                    print("current cube is ", current_block)

                elif event.type == pygame.KEYDOWN and current_block != -1:
                    if event.key == pygame.K_1:
                        self.process_input(current_block, 1)
                    elif event.key == pygame.K_2:
                        self.process_input(current_block, 2)
                    elif event.key == pygame.K_3:
                        self.process_input(current_block, 3)
                    if event.key == pygame.K_4:
                        self.process_input(current_block, 4)
                    elif event.key == pygame.K_5:
                        self.process_input(current_block, 5)
                    elif event.key == pygame.K_6:
                        self.process_input(current_block, 6)
                    elif event.key == pygame.K_7:
                        self.process_input(current_block, 7)
                    elif event.key == pygame.K_8:
                        self.process_input(current_block, 8)
                    elif event.key == pygame.K_9:
                        self.process_input(current_block, 9)


                    elif event.key == pygame.K_SPACE:
                        count = 0
                        for row in range(9):
                            for col in range(9):
                                self.blocks[count][5] = self.solution_board[row][col]
                                count += 1

                    solved = True
                    for num in self.blocks:
                        if num[5] == 0:
                            solved = False

                    if solved:
                        pygame.draw.rect(self.gameDisplay, self.white, [0, 400, 400, 500])

                        text = self.end_game_font.render("Solved ", True, self.green, "white")
                        self.gameDisplay.blit(text, (self.screen_width / 2 - text.get_rect().width / 2, self.screen_height))

                        # take away x's at bottom
                        self.x_array[0] = 0

                        # take away of space bar text
                        self.space_bar_text = ""

            self.render_text()
            pygame.display.update()





