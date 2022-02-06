import pygame, random, os, sys, time

# Define variables

WIDTH = 750
HEIGHT = 440
FPS = 40
VEL = 2

SPRITE_IMAGE = pygame.image.load(os.path.join('Assets', 'sprite.png'))

SPRITE = pygame.transform.scale(SPRITE_IMAGE, (15,15))

menu_background = pygame.image.load(os.path.join('Assets', 'menu_background.png'))

def get_font(size):
    return pygame.font.Font(os.path.join('Assets', 'font.ttf', 40))

# Define colours

BLACK = (0, 0, 0)
BLUE = (40, 40, 255)
LIGHTBLUE = (150, 255, 255)

# initalise pygame

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Maze Game")
clock = pygame.time.Clock()

#initalise fonts

pygame.font.init()
winner_font = pygame.font.SysFont('comicsans', 40)
timer_font = pygame.font.SysFont('comicsans', 30)

# setup variables for maze

x = 0                    # x axis
y = 0                    # y axis
w = 20                   # width of cell
grid = []
visited = []
stack = []
solution = {}

maze = pygame.Surface(screen.get_size())
maze.fill(LIGHTBLUE)

player = pygame.draw.rect(maze, BLACK, pygame.Rect(405, 405, 15, 15))


class Button():                                                                             #creating a class for buttons
    def __init__(self, image, pos, text_input, font, base_color, hovering_color):
            self.image = image
            self.x_pos = pos[0]
            self.y_pos = pos[1]
            self.font = font
            self.base_color, self.hovering_color = base_color, hovering_color
            self.text_input = text_input
            self.text = self.font.render(self.text_input, True, self.base_color)
            if self.image is None:
                    self.image = self.text
            self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
            self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))

    def update(self, screen):
            if self.image is not None:
                    screen.blit(self.image, self.rect)
            screen.blit(self.text, self.text_rect)

    def checkForInput(self, position):
            if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
                    return True
            return False

    def changeColor(self, position):            #changes colour of buttons if hovering with mouse
            if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
                    self.text = self.font.render(self.text_input, True, self.hovering_color)
            else:
                    self.text = self.font.render(self.text_input, True, self.base_color)


def play(x, y, w):

    # build the grid

    for i in range(1,21):
        x = 20                                                            # set x coordinate to start position
        y = y + 20                                                        # start a new row
        for j in range(1, 21):
            maze_top = pygame.draw.rect(maze, BLACK, pygame.Rect(x, y, 20, 1))           # top of cell
            maze_right = pygame.draw.rect(maze, BLACK, pygame.Rect(x + w, y, 1, 20))       # right of cell
            maze_bottom = pygame.draw.rect(maze, BLACK, pygame.Rect(x + w, y + w, 20, 1))   # bottom of cell
            maze_left = pygame.draw.rect(maze, BLACK, pygame.Rect(x, y + w, 1, 20))       # left of cell
            grid.append((x,y))                                            # add cell to grid list
            x = x + 20                                                    # move cell to new position


    square1 = pygame.draw.rect(maze, BLUE, (x + 1, y - w + 1, 19, 39), 0)         # draw a rectangle twice the width of the cell
    pygame.display.update()                                                         # to animate the wall being removed


    square2 = pygame.draw.rect(maze, BLUE, (x +  1, y + 1, 19, 39), 0)
    pygame.display.update()


    square3 = pygame.draw.rect(maze, BLUE, (x - w +1, y +1, 39, 19), 0)
    pygame.display.update()


    square4 = pygame.draw.rect(maze, BLUE, (x +1, y +1, 39, 19), 0)
    pygame.display.update()


    stack.append((x,y))                                            # place starting cell into stack
    visited.append((x,y))                                          # add starting cell to visited list
    while len(stack) > 0:                                          # loop until stack is empty
        cell = []                                                  # define cell list
        if (x + w, y) not in visited and (x + w, y) in grid:       # right cell available?
            cell.append("right")                                   # if yes add to cell list

        if (x - w, y) not in visited and (x - w, y) in grid:       # left cell available?
            cell.append("left")

        if (x , y + w) not in visited and (x , y + w) in grid:     # down cell available?
            cell.append("down")

        if (x, y - w) not in visited and (x , y - w) in grid:      # up cell available?
            cell.append("up")

        if len(cell) > 0:                                          # check to see if cell list is empty
            cell_chosen = (random.choice(cell))                    # select one of the cell randomly

            if cell_chosen == "right":                             # if this cell has been chosen
                square4 = pygame.draw.rect(maze, BLUE, (x +1, y +1, 39, 19), 0)
                pygame.display.update()
                solution[(x + w, y)] = x, y                        # solution = dictionary key = new cell, other = current cell
                x = x + w                                          # make this cell the current cell
                visited.append((x, y))                             # add to visited list
                stack.append((x, y))                               # place current cell on to stack

            elif cell_chosen == "left":
                square3 = pygame.draw.rect(maze, BLUE, (x - w +1, y +1, 39, 19), 0)
                pygame.display.update()
                solution[(x - w, y)] = x, y
                x = x - w
                visited.append((x, y))
                stack.append((x, y))

            elif cell_chosen == "down":
                square2 = pygame.draw.rect(maze, BLUE, (x +  1, y + 1, 19, 39), 0)
                pygame.display.update()
                solution[(x , y + w)] = x, y
                y = y + w
                visited.append((x, y))
                stack.append((x, y))

            elif cell_chosen == "up":
                square1 = pygame.draw.rect(maze, BLUE, (x + 1, y - w + 1, 19, 39), 0)         # draw a rectangle twice the width of the cell
                pygame.display.update()
                solution[(x , y - w)] = x, y
                y = y - w
                visited.append((x, y))
                stack.append((x, y))
        else:
            x, y = stack.pop()                                    # if no cells are available pop one from the stack




    # patch maze walls
    pygame.draw.rect(maze, LIGHTBLUE, pygame.Rect(421, 21, 20, 400))
    pygame.draw.rect(maze, LIGHTBLUE, pygame.Rect(20, 421, 400, 20))
    pygame.draw.rect(maze, BLACK, pygame.Rect(20, 420, 20, 1))
    pygame.draw.rect(maze, LIGHTBLUE, pygame.Rect(421, 400, 40, 40))


    #draw_text = winner_font.render(text, 1, BLACK)
    #maze.blit(draw_text, [500, 40])
    #pygame.display.update()


    #draw_timer = timer_font.render(text, 1, BLACK)
    #maze.blit(draw_timer, [500, 55])

    
    running = True
    while running:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()

        keys_pressed = pygame.key.get_pressed()
        if keys_pressed[pygame.K_a] and player.x - VEL > 18: #left
            player.x = player.x - VEL
        if keys_pressed[pygame.K_d] and player.x + VEL < 405: #right
            player.x = player.x + VEL
        if keys_pressed[pygame.K_w] and player.y - VEL > 18: #up
            player.y = player.y - VEL
        if keys_pressed[pygame.K_s] and player.y + VEL < 405: #down
            player.y = player.y + VEL

        if keys_pressed[pygame.K_r]: #restart
            player.x = 405
            player.y = 405

        if keys_pressed[pygame.K_q] and keys_pressed[pygame.K_e]: #hax
            player.x = 20
            player.y = 20

        #winner_text = ""
        #if player.x < 21 and player.y < 21:
            #winner_text = "You Win!"

        #if winner_text != "":
            #draw_winner(winner_text)

        #add timer thing here
        
        screen.blit(maze,(0, 0))
        screen.blit(SPRITE, (player.x, player.y))
        pygame.display.update()

def main_menu():

    pygame.display.set_caption("Main Menu")
    
    while True:

        menu_mouse_pos = pygame.mouse.get_pos()

        menu_text = get_font(100).render("Main Menu", True, (182,143,64))
        menu_rect = menu_text.get_rect(center=(640,100))

        play_button = Button(image = pygame.image.load(os.path.join('Assets', 'play_rect.png')), pos = (640,250),
                             text_input = "Play", font=get_font(75), base_color = "(215,252,212)", hovering_color = "White")
        options_button = Button(image = pygame.image.load('Assets', 'options_rect.png'), pos = (640,400),
                             text_input = "Options", font=get_font(75), base_color = "(215,252,212)", hovering_color = "White")
        quit_button = Button(image = pygame.image.load('Assets', 'quit_rect.png'), pos = (640,550),
                             text_input = "Quit", font=get_font(75), base_color = "(215,252,212)", hovering_color = "White")

        screen.blit(menu_text, menu_rect)

        for button in [play_button, options_button, quit_button]:
            button.changeColor(menu_mouse_pos)
            button.update(screen)


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_button.checkForInput(menu_mouse_pos):
                    play()
                if options_button.checkForInput(menu_mouse_pos):
                    options()
                if play_button.checkForInput(menu_mouse_pos):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()

main_menu()
