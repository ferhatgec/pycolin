#!/usr/bin/env python3

# MIT License
#
# Copyright (c) 2021 Ferhat Geçdoğan All Rights Reserved.
# Distributed under the terms of the MIT License.
#
#

# PyColin : Python implementation of Colin
#
# github.com/ferhatgec/colin
#
#

from sys import argv, exit

color = '\033[48;2;'
color_data = color
reset = '\033[0m'
table_item = '░░'

def SetColor(r: int, g: int, b: int) -> str:
    return color + str(r) + ';' + str(g) + ';' + str(b) + 'm'

light_gray = SetColor(171, 171, 171)
white      = SetColor(255, 255, 255)

def TABLE_LIGHT_GRAY():
    print(light_gray, table_item, white, table_item, reset, sep='', end='')

def TABLE_WHITE():
    print(white, table_item, light_gray, table_item, reset, sep='', end='')

def TABLE_COLOR():
    print(color_data, table_item, reset, sep='', end='')

def NEWLINE():
    print()

def Init(r: int, g: int, b: int) -> str:
    return SetColor(r, g, b)

def PrintColorBox(split: bool):
    if split:
        TABLE_LIGHT_GRAY()
    else:
        TABLE_WHITE()

    for i in range(6):
        TABLE_COLOR()

    if not split:
        TABLE_LIGHT_GRAY()
    else:
        TABLE_WHITE()

    NEWLINE()

def PrintBox():
    i = 0
    split = False

    for i in range(5):
        TABLE_LIGHT_GRAY()

    NEWLINE()

    for i in range(5):
        TABLE_WHITE()

    NEWLINE()

    for i in range(5):
        PrintColorBox(split)
        split = not split

    for i in range(5):
        TABLE_LIGHT_GRAY()

    NEWLINE()

    for i in range(5):
        TABLE_WHITE()

    NEWLINE()

if len(argv) < 4:
    print('Fegeya Colin : CLI color info tool',
          '--',
          argv[0] + ' {r} {g} {b}',
          '-------',
          argv[0] + ' 255 255 255',
          sep='\n')

    exit(1)

def insert(data: str) -> int:
    if data.isnumeric():
        return int(data)
    else:
        print('Use numeric value')
        exit(1)

r = insert(argv[1])
g = insert(argv[2])
b = insert(argv[3])

color_data = Init(r, g, b)
PrintBox()
