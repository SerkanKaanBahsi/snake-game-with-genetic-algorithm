import pygame as pg
import random
from Moves import *

games_count = 0
clock = pg.time.Clock()
red = pg.Color(255, 0, 0)
green = pg.Color(0, 255, 0)
black = pg.Color(0, 0, 0)
white = pg.Color(255, 255, 255)
brown = pg.Color(165, 42, 42)

screen_width, screen_height = (400, 400)
score, high_score = (0, 0)

pg.init()

# Create game screen.
wn = pg.display.set_mode((screen_width, screen_height))
pg.display.set_caption('Snake')


# Play the game and call fitness function
def cal_fitness(population):
    fitness_val = []
    for i in range(len(population)):
        fd = Food()
        p = Player()
        fitness = play_game(fd, p, population[i])
        fitness_val.append(fitness)

    return fitness_val


# Fitness is calculated here.
# Values in here can be changed.
def fitness_calculate(collision_control, points, move_counter):
    how_fit = 0
    how_fit = (1000-move_counter)*2
    if collision_control is True:
        how_fit = 600
    else:
        how_fit = 200

    if points == 0:
        how_fit += 425
    else:
        how_fit += points * -30
    return how_fit


class Food():
    def __init__(self):
        self.x = screen_width/2
        self.y = screen_height/4
        self.color = red
        self.width = 10
        self.height = 10

    def draw_food(self, surface):
        self.food = pg.Rect(self.x, self.y, self.width, self.height)
        pg.draw.rect(surface, self.color, self.food)

    def is_eaten(self, head):
        return self.food.colliderect(head)

    def new_pos(self):
        self.x = random.randint(0, screen_width-self.width)
        self.y = random.randint(0, screen_height-self.height)

    def returns_pos(self):
        return self.x, self.y


class Player():
    def __init__(self):
        self.x = screen_width/2
        self.y = screen_height/2
        self.width = 10
        self.height = 10
        self.velocity = 10
        self.direction = 'stop'
        self.body = []
        self.head_color = green
        self.body_color = brown

    def draw_player(self, surface):
        self.seg = []
        self.head = pg.Rect(self.x, self.y, self.width, self.height)
        pg.draw.rect(surface, self.head_color, self.head)
        if len(self.body) > 0:
            for unit in self.body:
                segment = pg.Rect(unit[0], unit[1], self.width, self.height)
                pg.draw.rect(surface, self.body_color, segment)
                self.seg.append(segment)

    def add_unit(self):
        if len(self.body) != 0:
            index = len(self.body)-1
            x = self.body[index][0]
            y = self.body[index][1]
            self.body.append([x, y])
        else:
            self.body.append([1000, 1000])

    def is_collision(self):
        for segment in self.seg:
            if self.head.colliderect(segment):
                return True
        if self.y < 0 or self.y > screen_height - self.height or self.x < 0 or self.x > screen_width - self.width:
            return True

    def move(self):
        for index in range(len(self.body)-1, 0, -1):
            x = self.body[index-1][0]
            y = self.body[index-1][1]
            self.body[index] = [x, y]
        if len(self.body) > 0:
            self.body[0] = [self.x, self.y]
        if self.direction == 'up':
            self.y -= self.velocity
        if self.direction == 'down':
            self.y += self.velocity
        if self.direction == 'left':
            self.x -= self.velocity
        if self.direction == 'right':
            self.x += self.velocity

    def change_direction(self, direction):
        if self.direction != 'down' and direction == 0:
            self.direction = 'up'
        if self.direction != 'right' and direction == 2:
            self.direction = 'left'
        if self.direction != 'up' and direction == 1:
            self.direction = 'down'
        if self.direction != 'left' and direction == 3:
            self.direction = 'right'

    def returns_snake_pos(self):
        return self.x, self.y

    def returns_body(self):
        return self.body


def draw_score(surface):
    global high_score
    font_name = pg.font.match_font('arial')
    if score > high_score:
        high_score = score
    font = pg.font.Font(font_name, 18)
    text_surface = font.render('Score: {} High Score: {}'.format(score, high_score), True, white)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (200, 10)
    surface.blit(text_surface, text_rect)


def play_game(fd, p, real_moves):
    global score
    member = real_moves[:]
    run = True
    col_control = False
    score = 0
    i = 0
    while run:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
        clock.tick(120)
        wn.fill(black)
        fd.draw_food(wn)
        p.draw_player(wn)
        draw_score(wn)
        # Calculate steps to take according to food or obstacles
        if member[i] == 4:
            x1, y1 = fd.returns_pos()
            x2, y2 = p.returns_snake_pos()
            if i == 0:
                move_before = 0
            else:
                move_before = member[i-1]
            member[i] = distance_to_food(x1, y1, x2, y2, move_before)
        elif member[i] == 5:
            x2, y2 = p.returns_snake_pos()
            if i == 0:
                move_before = 0
            else:
                move_before = member[i-1]
            member[i] = check_blocks(x2, y2, p.returns_body(), move_before)
            
        # Move
        p.change_direction(member[i])
        p.move()

        if fd.is_eaten(p.head):
            fd.new_pos()
            p.add_unit()
            score += 10
            
        # The game ends here if collision happens 
        if p.is_collision():
            run = False
            col_control = True
        elif i >= len(member)-1:
            run = False
        else:
            i += 1
        
        pg.display.update()
    return fitness_calculate(col_control,score,i)

