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

import enum
from sys import argv, exit


class InfoType(enum.IntEnum):
    Name = 0
    Hmm = 1
    Rgb = 2
    Hex = 3
    Cmyk = 4
    Hsl = 5
    Hsv = 6
    Hmm2 = 7
    Ascii = 8
    Esc = 9

class Colin:
    color = '\033[48;2;'
    fg_color = '\033[38;2;'
    reset = '\033[0m'
    hex = ''
    color_data = color

    table_item = '░░'
    line = 0

    infos = [
        'name: ',
        '-----',
        '\033[0;31mr\033[0;32mg\033[0;34mb\033[0m  : ',
        'hex  : ',
        'cmyk : ',
        'hsl  : ',
        'hsv  : ',
        '-----',
        'ascii: ',
        'esc  : '
    ]

    def __init__(self):
        self.light_gray = self.SetColor(171, 171, 171)
        self.white = self.SetColor(255, 255, 255)

        
        # Rainbow colors
        self.red        = self.SetFgColor(255, 0  , 0)
        self.orange     = self.SetFgColor(255, 165, 0)
        self.yellow     = self.SetFgColor(255, 255, 0)
        self.green      = self.SetFgColor(0  , 128, 0)
        self.blue       = self.SetFgColor(0  , 0, 255)
        self.purple     = self.SetFgColor(75 , 0, 130)
        self.pink       = self.SetFgColor(238,130,238)

    def name_function(self):
        pass

    def hmm_function(self):
        pass

    def rgb_function(self):
        pass

    def hex_function(self):
        pass

    def cmyk_function(self):
        pass

    def hsl_function(self):
        pass

    def hsv_function(self):
        pass

    def hmm2_function(self):
        pass

    def ascii_function(self):
        pass

    def esc_function(self):
        pass

    def switch(self, arg: InfoType):
        {
            InfoType.Name: self.name_function(),

            InfoType.Hmm: self.hmm_function(),

            InfoType.Rgb: self.rgb_function(),
            InfoType.Hex: self.hex_function(),
            InfoType.Cmyk: self.cmyk_function(),
            InfoType.Hsl: self.hsl_function(),
            InfoType.Hsv: self.hsv_function(),

            InfoType.Hmm2: self.hmm2_function(),

            InfoType.Ascii: self.ascii_function(),
            InfoType.Esc: self.esc_function()
        }[arg]

    def SetColor(self, r: int, g: int, b: int) -> str:
        return self.color + str(r) + ';' + str(g) + ';' + str(b) + 'm'

    def SetFgColor(self, r: int, g: int, b: int) -> str:
        return self.fg_color + str(r) + ';' + str(g) + ';' + str(b) + 'm'

    def Newline(self):
        if self.line < len(self.infos):
            print(' ', self.infos[self.line])

            self.switch(InfoType(self.line))
        else:
            print(end='\n')

        self.line += 1

    def TABLE_LIGHT_GRAY(self):
        print(self.light_gray, self.table_item, self.white, self.table_item, self.reset, sep='', end='')


    def TABLE_WHITE(self):
        print(self.white, self.table_item, self.light_gray, self.table_item, self.reset, sep='', end='')


    def TABLE_COLOR(self):
        print(self.color_data, self.table_item, self.reset, sep='', end='')


    def NEWLINE(self):
        print()


    def Init(self, r: int, g: int, b: int):
        self.color_data = self.SetColor(r, g, b)

        self.infos[InfoType.Hex] = (self.red + 'hex  : ' + self.orange + self.hex)
        self.infos[InfoType.Cmyk] = (self.orange + 'cmyk : ' + self.yellow + 'work-in-progress')
        self.infos[InfoType.Hsl] = (self.yellow + 'hsl  : ' + self.green + 'work-in-progress')
        self.infos[InfoType.Hsv] = (self.green + 'hsv  : ' + self.blue + 'work-in-progress')
        self.infos[InfoType.Ascii] = (self.blue + 'ascii: ' + self.purple + 'work-in-progress')
        self.infos[InfoType.Esc] = (self.purple + 'esc  : ' + self.pink + 'work-in-progress')

    def PrintColorBox(self, split: bool):
        if split:
            self.TABLE_LIGHT_GRAY()
        else:
            self.TABLE_WHITE()

        for i in range(6):
            self.TABLE_COLOR()

        if not self.split:
            self.TABLE_LIGHT_GRAY()
        else:
            self.TABLE_WHITE()

        self.Newline()


    def PrintBox(self):
        i = 0
        self.split = False

        for i in range(5):
            self.TABLE_LIGHT_GRAY()

        self.Newline()

        for i in range(5):
            self.TABLE_WHITE()

        self.Newline()

        for i in range(5):
            self.PrintColorBox(self.split)
            self.split = not self.split

        for i in range(5):
            self.TABLE_LIGHT_GRAY()

        self.Newline()

        for i in range(5):
            self.TABLE_WHITE()

        self.Newline()


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

init = Colin()
init.Init(r, g, b)
init.PrintBox()
