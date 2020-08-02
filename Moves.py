import random


def distance_to_food(food_x, food_y, snake_x, snake_y, move_before):
    up = snake_y - food_y
    down = food_y - snake_y
    left = snake_x - food_x
    right = food_x - snake_x
    possible_moves = [up, down, left, right]

    move_before += 1 if move_before % 2 == 0 else -1
    possible_moves[move_before] == 0.0
    moves = [i for i, ni in enumerate(possible_moves) if ni > 0.0]

    return random.randint(0, 4) if len(moves) == 0 else random.choice(moves)


def check_blocks(snake_x, snake_y, body, move_before):

    right, left, down, up = check_surroundings(snake_x, snake_y, body)

    possible_moves = [up, down, left, right]
    moves = [i for i, move in enumerate(possible_moves) if move]

    return  random.randint(0, 4) if len(moves) == 0 else random.choice(moves)


def check_surroundings(snake_x, snake_y, body):
    right = True
    left = True
    up = True
    down = True

    for element in body:
        if element[0] - snake_x <= 20.0:
            right = False
        elif snake_x - element[0] <= 20.0:
            left = False

    if snake_x >= 380.0:
        right = False
    elif snake_x <= 10.0:
        left = False

    for element in body:
        if element[1] - snake_y <= 20.0:
            down = False
        elif snake_y - element[1] <= 20.0:
            up = False

    if snake_y >= 380.0:
        down = False
    elif snake_y <= 10.0:
        up = False

    return right, left, down, up
