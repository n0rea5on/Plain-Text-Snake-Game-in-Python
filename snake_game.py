#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 12 17:54:44 2024

@author: marshall
"""

import random

GRID_SIZE = 12

GRID_POINT = '.'
SNAKE_HEAD = '*'
SNAKE_BODY = '#'
FOOD = 'O'

class Grid(object):
    """ coordinate and type is all data att we need """
    def __init__(self, x, y, pt_type='grid_pt'):
        self.x = x
        self.y = y
        self.pt_type = pt_type
    def set_pt_type(self, pt_type):
        self.pt_type = pt_type
    def get_pt_type(self):
        return self.pt_type
    def get_pt_char(self):
        """ returns the actual character of pt
            for printing """
        if self.pt_type == 'grid_pt':
            return GRID_POINT
        elif self.pt_type == 'snake_head':
            return SNAKE_HEAD
        elif self.pt_type == 'snake_body':
            return SNAKE_BODY
        elif self.pt_type == 'food':
            return FOOD
        else:
            raise TypeError("invalid point type")

class Snake(object):
    def __init__(self, x, y, snk_type):
        """ snk_type: body/head """
        self.x = x
        self.y = y
        self.snk_type = snk_type
    def set_coordinate(self, x, y):
        self.x = x
        self.y = y
    def set_old_coordinate(self, x, y):
        self.old_x = x
        self.old_y = y
    def get_coordinate(self):
        return [self.x, self.y]
    def get_old_coordinate(self):
        return [self.old_x, self.old_y]
    def get_snk_type(self):
        return self.snk_type
    def get_identifier(self):
        return self.tag
    
def generate_grid(grid_size):
    """ returns a list of grid elements """
    FullGrid = []
    # [[x1, x2, x3...], [x1, x2, x3...]]
    for i in range(grid_size):
        FullGrid.append([])
        for j in range(grid_size):
            FullGrid[i].append(Grid(j, i))
    return FullGrid

def random_point(end, st=0):
    x = random.randrange(st, end)
    y = random.randrange(st, end)
    return [x, y]

def initialize_grid(grid_size, FullGrid, SnakePts):
    """ FullGrid, SnakePts list
        returns food_coor """
    # head shoudn't be too close to border
    head_coor = random_point(GRID_SIZE-2, st=2)
    SnakePts.append(Snake(head_coor[0], head_coor[1], 'head'))
    FullGrid[head_coor[1]][head_coor[0]].set_pt_type('snake_head')
    
    # food can be wherever else
    food_coor = random_point(GRID_SIZE)
    while food_coor == head_coor:
        food_coor = random_point(GRID_SIZE)
    FullGrid[food_coor[1]][food_coor[0]].set_pt_type('food')
    return food_coor

def print_grid(grid_list):
    for line in grid_list:
        for point in line:
            print(point.get_pt_char(), end=' ')
        print()

def update_point(x, y, direction):
    """ input coordinate, 
        returns new coordinate """
    # note the top left point is coordinate (0, 0)
    if direction == 'w':
        y -= 1
    elif direction == 's':
        y += 1
    elif direction == 'a':
        x -= 1
    elif direction == 'd':
        x += 1
    else:
        raise ValueError('Invalid direction value')
    return [x, y]

def update_snake(SnakePts, FullGrid, food_coor, direction):
    #import pdb; pdb.set_trace()
    # set head position
    head_coor = SnakePts[0].get_coordinate()
    new_coor = update_point(head_coor[0], head_coor[1], direction)
    # set new
    SnakePts[0].set_coordinate(new_coor[0], new_coor[1])
    # set old
    SnakePts[0].set_old_coordinate(head_coor[0], head_coor[1])
    
    if new_coor[0] < 0 or new_coor[0] > GRID_SIZE-1 or new_coor[1] < 0 or\
            new_coor[1] > GRID_SIZE-1:
                print('The snake hits the wall!')
                return 'over'
    if FullGrid[new_coor[1]][new_coor[0]].get_pt_type() == 'snake_body':
        print('The snake eats itself!')
        return 'over'

    meet_food = False
    if new_coor == food_coor:
        meet_food = True

    first_time_met_food = False
    if meet_food and len(SnakePts) == 1:
        SnakePts.append(Snake(head_coor[0], head_coor[1], 'body'))
        first_time_met_food = True

    # set body position
    if (not first_time_met_food) and (len(SnakePts) != 1):
        for i in range(1, len(SnakePts)):
            # the last snake point
            if i == len(SnakePts)-1:
                # if head meet food
                if meet_food:
                    tail_coor = SnakePts[i].get_coordinate()
                    SnakePts.append(Snake(tail_coor[0], tail_coor[1], 'body'))
                prev_point_coor = SnakePts[i-1].get_old_coordinate()
                current_coor = SnakePts[i].get_coordinate()
                # set new
                SnakePts[i].set_coordinate(prev_point_coor[0], prev_point_coor[1])
                # set old
                SnakePts[i].set_old_coordinate(current_coor[0],\
                        current_coor[1])
            # not the last, just update
            else:
                prev_point_coor = SnakePts[i-1].get_old_coordinate()
                current_coor = SnakePts[i].get_coordinate()
                SnakePts[i].set_coordinate(prev_point_coor[0], prev_point_coor[1])
                SnakePts[i].set_old_coordinate(current_coor[0],\
                        current_coor[1])
            

def update_grid(FullGrid, SnakePts, food_coor):
    """ update full grid,
        returns food_coor """
    # reset all points to grid point
    for line in FullGrid:
        for point in line:
            point.set_pt_type('grid_pt')
    # set snake points
    for point in SnakePts:
        coor = point.get_coordinate()
        if point.get_snk_type() == 'head':
            FullGrid[coor[1]][coor[0]].set_pt_type('snake_head')
        else:
            FullGrid[coor[1]][coor[0]].set_pt_type('snake_body')
    # regenerate food if eaten
    if SnakePts[0].get_coordinate() == food_coor:
        food_coor = random_point(GRID_SIZE)
        while FullGrid[food_coor[1]][food_coor[0]].get_pt_type() == 'snake_head' \
            or FullGrid[food_coor[1]][food_coor[0]].get_pt_type() == 'snake_body':
                food_coor = random_point(GRID_SIZE)
    FullGrid[food_coor[1]][food_coor[0]].set_pt_type('food')
    return food_coor
    

def main_game():
    FullGrid = generate_grid(GRID_SIZE)
    # SnakePts has an order, from head to the end of body
    SnakePts = []
    # get initial food coordinate
    food_coor = initialize_grid(GRID_SIZE, FullGrid, SnakePts)
    
    print_grid(FullGrid)
    
    usr_inpt = input('Enter direction in "w" "a" "s" "d", "end" to end: ')
    while usr_inpt != 'end':
        # input check
        while usr_inpt not in ['w', 'a', 's', 'd' ,'end']:
            usr_inpt = input('Enter direction in "w" "a" "s" "d", "end" to end: ')
        if usr_inpt == 'end':
            break

        if update_snake(SnakePts, FullGrid, food_coor, usr_inpt) != 'over':
            # update and set food_coor
            food_coor = update_grid(FullGrid, SnakePts, food_coor)
            print_grid(FullGrid)
            usr_inpt = input('Enter direction in "w" "a" "s" "d", "end" to end: ')
        else:
            break
    print('Your score is:', len(SnakePts))
    print('Game Over')
    
if __name__ == '__main__':
    main_game()
