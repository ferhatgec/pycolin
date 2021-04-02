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

    def ToHex(self, r: int, g: int, b: int) -> str:
        if (r or g or b) < 0 and (r or g or b) > 255:
            return '#null'

        return '#%02x%02x%02x' % (r, g, b)

    def ToCMYK(self, r: int, g: int, b: int) -> tuple:
        _r, _g, _b = r, g, b

        w, c, m, y, k, max = 0, 0, 0, 0, 0, 0

        if _r == 0 and _g == 0 and _b == 0:
            c = m = y = 0
            k = 100
        else:
            _r = _r / 255
            _g = _g / 255
            _b = _b / 255

            max = _r

            # Get max value
            if _g > max:
                max = _g

            if _b > max:
                max = _b

            w = max

            c = ((w - _r) / w) * 100
            m = ((w - _g) / w) * 100
            y = ((w - _b) / w) * 100

            k = (1 - w) * 100

        return str(round(c, 2)), str(round(m, 2)), str(round(y, 2)), str(round(k, 2))


    def get_min(self, r: float, g: float, b: float):
        min = r

        if g < min:
            min = g

        if b < min:
            min = b

        return min

    def get_max(self, r: float, g: float, b: float):
        max = r

        if g > max:
            max = g

        if b > max:
            max = b

        return max

    def ToHSL(self, r: float, g: float, b: float):
        _r, _g, _b = r, g, b

        h, s, l, min, max = 0, 0, 0, 0, 0

        _r = _r / 255.0
        _g = _g / 255.0
        _b = _b / 255.0

        min = self.get_min(_r, _g, _b)
        max = self.get_max(_r, _g, _b)

        l = 50 * (min + max)

        if min == max:
            s = h = 0
        elif l < 50:
           s = 100 * (max - min) / (max + min)
        else:
           s = 100 * (max - min) / (2.0 - max - min)


        if _g - _b == 0:
            h = 0
        elif max == _r:
            h = 60 * (_g - _b) / (max - min)
        elif max == _g:
            h = 60 * (_b - _r) / (max - min) + 120
        elif max == _b:
            h = 60 * (_r - _g) / (max - min) + 240

        if h < 0:
            h = h + 360

        return str(round(h, 2)), str(round(s, 2)), str(round(l, 2))

    def ToHSV(self, r: float, g: float, b: float):
        _r, _g, _b, copy_r, copy_g, copy_b = r, g, b, 0, 0, 0

        h, s, v, min, max = 0.0, 0.0, 0.0, 0.0, 0.0

        _r = _r / 255
        _g = _g / 255
        _b = _b / 255

        max = self.get_max(_r, _g, _b)
        min = self.get_min(_r, _g, _b)

        v = max

        if min == max:
            h = s = 0

            return str(0), str(0), str(round(v * 100, 2))

        s = (max - min) / max

        copy_r = (max - _r) / (max - min)
        copy_g = (max - _g) / (max - min)
        copy_b = (max - _b) / (max - min)

        if _g - _b == 0:
            h = 0
        elif max == _r:
            h = 60 * (_g - b) / (max - min)
        elif max == _g:
            h = 60 * (_b - _r) / (max - min) + 120
        elif max == _b:
            h = 60 * (_r - _g) / (max - min) + 240

        if h < 0:
            h = h + 360

        return str(round(h, 2)), str(round(s * 100, 2)), str(round(v * 100, 2))

    def name_function(self):
        print(end=self.color_name)

    def hmm_function(self):
        pass

    def rgb_function(self):
        print(self.pink
              + 'rgb'
              + self.reset
              + '('
              + '\033[0;31m'
              + str(self.r)
              + ', \033[0;34m'
              + str(self.g)
              + ', \033[0;34m'
              + str(self.b)
              + self.reset
              + ')',
              end='')

    def hex_function(self):
        pass

    def cmyk_function(self):
        print(end='('
              + '\033[0;31m'
              + self.cmyk[0]
              + self.reset
              + ', \033[0;32m'
              + self.cmyk[1]
              + ', \033[0;34m'
              + self.cmyk[2]
              + ', '
              + self.pink
              + self.cmyk[3]
              + ')')

    def hsl_function(self):
        print(end='('
              + '\033[0;31m'
              + self.hsl[0]
              + self.reset
              + ', \033[0;32m'
              + self.hsl[1]
              + ', \033[0;34m'
              + self.hsl[2]
              + ')')

    def hsv_function(self):
        print(end='('
              + '\033[0;31m'
              + self.hsv[0]
              + self.reset
              + ', \033[0;32m'
              + self.hsv[1]
              + ', \033[0;34m'
              + self.hsv[2]
              + ')')

    def hmm2_function(self):
        pass

    def ascii_function(self):
        print(end='\\033' + self.color_data[1:])


    def esc_function(self):
        print(end='\\033')

    def switch(self, arg: InfoType):
        {
            InfoType.Name: self.name_function,

            InfoType.Hmm: self.hmm_function,

            InfoType.Rgb: self.rgb_function,
            InfoType.Hex: self.hex_function,
            InfoType.Cmyk: self.cmyk_function,
            InfoType.Hsl: self.hsl_function,
            InfoType.Hsv: self.hsv_function,

            InfoType.Hmm2: self.hmm2_function,

            InfoType.Ascii: self.ascii_function,
            InfoType.Esc: self.esc_function
        }[arg]()

    def SetColor(self, r: int, g: int, b: int) -> str:
        return self.color + str(r) + ';' + str(g) + ';' + str(b) + 'm'

    def SetFgColor(self, r: int, g: int, b: int) -> str:
        return self.fg_color + str(r) + ';' + str(g) + ';' + str(b) + 'm'

    def Newline(self):
        if self.line < len(self.infos):
            print('  ', self.infos[self.line], end='')

            self.switch(InfoType(self.line))

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

    def init_color_name(self):
        hmm = self.color_names.get(str(self.r) + ',' + str(self.g) + ',' + str(self.b))

        if hmm != None:
            self.color_name = hmm
        else:
            self.color_name = "hmmm?"

    def Init(self, r: int, g: int, b: int):
        self.r = r
        self.g = g
        self.b = b

        self.hex = self.ToHex(r, g, b)

        self.color_data = self.SetColor(r, g, b)

        self.cmyk = self.ToCMYK(r, g, b)
        self.hsl = self.ToHSL(r, g, b)
        self.hsv = self.ToHSV(r, g, b)

        self.init_color_name()

        self.infos[InfoType.Name] = (self.SetFgColor(r, g, b) + 'color' + self.reset + ': ')
        self.infos[InfoType.Hex] = (self.red + 'hex  : ' + self.orange + self.hex)
        self.infos[InfoType.Cmyk] = (self.orange + 'cmyk : ' + self.yellow)
        self.infos[InfoType.Hsl] = (self.yellow + 'hsl  : ' + self.green)
        self.infos[InfoType.Hsv] = (self.green + 'hsv  : ' + self.blue)
        self.infos[InfoType.Ascii] = (self.blue + 'ascii: ' + self.purple)
        self.infos[InfoType.Esc] = (self.purple + 'esc  : ' + self.pink)

    def PrintColorBox(self, split: bool):
        if split:
            self.TABLE_LIGHT_GRAY()
        else:
            self.TABLE_WHITE()

        for i in range(8):
            self.TABLE_COLOR()

        if not self.split:
            self.TABLE_LIGHT_GRAY()
        else:
            self.TABLE_WHITE()

        self.Newline()


    def PrintBox(self):
        i = 0
        self.split = False

        for i in range(6):
            self.TABLE_LIGHT_GRAY()

        self.Newline()

        for i in range(6):
            self.TABLE_WHITE()

        self.Newline()

        for i in range(6):
            self.PrintColorBox(self.split)
            self.split = not self.split

        for i in range(6):
            self.TABLE_LIGHT_GRAY()

        self.Newline()

        for i in range(6):
            self.TABLE_WHITE()

        self.Newline()

    def __init__(self):
        self.r = 0
        self.g = 0
        self.b = 0

        self.cmyk = ()
        self.hsl = ()
        self.hsv = ()

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

        self.color_name = ''

        # From Wikipedia: ^ )
        # Up to ~1045 for codes
        self.color_names = {
        '0,72,186': 'Absolute Zero',
        '176,191,26': 'Acid green',
        '124,185,232': 'Aero',
        '192,232,213': 'Aero blue',
        '178,132,190': 'African violet',
        '114,160,193': 'Air superiority blue',
        '237,234,224': 'Alabaster',
        '240,248,255': 'Alice blue',
        '196,98,16': 'Alloy orange',
        '239,222,205': 'Almond',
        '229,43,80': 'Amaranth',
        '159,43,104': 'Amaranth deep purple',
        '241,156,187': 'Amaranth pink',
        '171,39,79': 'Amaranth purple',
        '211,33,45': 'Amaranth red',
        '59,122,87': 'Amazon',
        '255,191,0': 'Amber',
        '255,126,0': 'Amber (SAE/ECE)',
        '153,102,204': 'Amethyst',
        '164,198,57': 'Android green',
        '205,149,117': 'Antique brass',
        '102,93,30': 'Antique bronze',
        '145,92,131': 'Antique fuchsia',
        '132,27,45': 'Antique ruby',
        '250,235,215': 'Antique white',
        '0,128,0': 'Ao (English)',
        '141,182,0': 'Apple green',
        '251,206,177': 'Apricot',
        '0,255,255': 'Aqua',
        '127,255,212': 'Aquamarine',
        '208,255,20': 'Arctic lime',
        '75,83,32': 'Army green',
        '143,151,121': 'Artichoke',
        '233,214,107': 'Arylide yellow',
        '178,190,181': 'Ash gray',
        '135,169,107': 'Asparagus',
        '255,153,102': 'Atomic tangerine',
        '165,42,42': 'Auburn',
        '253,238,0': 'Aureolin',
        '86,130,3': 'Avocado',
        '0,127,255': 'Azure',
        '240,255,255': 'Azure (X11/web color)',
        '137,207,240': 'Baby blue',
        '161,202,241': 'Baby blue eyes',
        '244,194,194': 'Baby pink',
        '254,254,250': 'Baby powder',
        '255,145,175': 'Baker-Miller pink',
        '250,231,181': 'Banana Mania',
        '218,24,132': 'Barbie Pink',
        '124,10,2': 'Barn red',
        '132,132,130': 'Battleship grey',
        '188,212,230': 'Beau blue',
        '159,129,112': 'Beaver',
        '245,245,220': 'Beige',
        '46,88,148': 'B\'dazzled blue',
        '156,37,66': 'Big dip o’ruby',
        '255,228,196': 'X11 color namesBisque',
        '61,43,31': 'Bistre',
        '150,113,23': 'Bistre brown',
        '202,224,13': 'Bitter lemon',
        '191,255,0': 'Bitter lime',
        '254,111,94': 'Bittersweet',
        '191,79,81': 'Bittersweet shimmer',
        '0,0,0': 'Black',
        '61,12,2': 'Black bean',
        '27,24,17': 'Black chocolate',
        '59,47,47': 'Black coffee',
        '84,98,111': 'Black coral',
        '59,60,54': 'Black olive',
        '191,175,178': 'Black Shadows',
        '255,235,205': 'Blanched almond',
        '165,113,100': 'Blast-off bronze',
        '49,140,231': 'Bleu de France',
        '172,229,238': 'Blizzard blue',
        '250,240,190': 'Blond',
        '102,0,0': 'Blood red',
        '0,0,255': 'Blue',
        '31,117,254': 'Blue (Crayola)',
        '0,147,175': 'Blue (Munsell)',
        '0,135,189': 'Blue (NCS)',
        '0,24,168': 'Blue (Pantone)',
        '51,51,153': 'Blue (pigment)',
        '2,71,254': 'RYB color model|Blue (RYB)',
        '162,162,208': 'Blue bell',
        '102,153,204': 'Blue-gray',
        '13,152,186': 'Blue-green',
        '6,78,64': 'Blue-greenBlue-green (color wheel)',
        '93,173,236': 'Blue jeans',
        '18,97,128': 'Blue sapphire',
        '138,43,226': 'IndigoBlue-violet',
        '115,102,189': 'Blue-violet (Crayola)',
        '77,26,127': 'Blue-violet (color wheel)',
        '80,114,167': 'Air Force blueBlue yonder',
        '60,105,231': '|Bluetiful',
        '222,93,131': 'Red-violetBlush',
        '121,68,59': 'Bole',
        '227,218,201': 'Bone',
        '0,106,78': 'Bottle green',
        '135,65,63': 'Brandy',
        '203,65,84': 'Brick red',
        '102,255,0': 'Bright green',
        '216,145,239': 'Bright lilac',
        '195,33,72': 'MaroonBright maroon',
        '25,116,210': 'Navy blueBright navy blue',
        '255,170,29': 'Bright yellow (Crayola)',
        '255,85,163': 'Brilliant rose',
        '251,96,127': 'Brink pink',
        '0,66,37': 'British racing green',
        '205,127,50': 'Bronze',
        '136,84,11': 'Brown',
        '175,110,77': 'Brown sugar',
        '27,77,62': 'Brunswick green',
        '123,182,97': 'Spring budBud green',
        '255,198,128': 'Buff',
        '128,0,32': 'Burgundy',
        '222,184,135': 'Burlywood',
        '161,122,116': 'Burnished brown',
        '204,85,0': 'Burnt orange',
        '233,116,81': 'Burnt sienna',
        '138,51,36': 'Burnt umber',
        '189,51,164': 'Byzantine',
        '112,41,99': 'Byzantium',
        '83,104,114': 'Cadet grey',
        '95,158,160': 'Cadet blue',
        '169,178,195': 'yCadet blue (Crayola)',
        '145,163,176': 'Cadet grey',
        '0,107,60': 'Cadmium green',
        '237,135,45': 'Cadmium orange',
        '227,0,34': 'Cadmium red',
        '255,246,0': 'Cadmium yellow',
        '166,123,91': 'Café au lait',
        '75,54,33': 'Café noir',
        '163,193,173': 'Cambridge blue',
        '193,154,107': 'Camel',
        '239,187,204': 'Cameo pink',
        '255,255,153': 'Canary',
        '255,239,0': 'Canary yellow',
        '255,8,0': 'Candy apple red',
        '228,113,122': 'Candy pink',
        '0,191,255': 'Capri',
        '89,39,32': 'Caput mortuum',
        '196,30,58': 'Cardinal',
        '0,204,153': 'Caribbean green',
        '150,0,24': 'Carmine',
        '215,0,64': 'Carmine (M&P)',
        '255,166,201': 'Carnation pink',
        '179,27,27': 'Carnelian',
        '86,160,211': 'Carolina blue',
        '237,145,33': 'Carrot orange',
        '0,86,63': 'Castleton green',
        '112,54,66': 'Catawba',
        '201,90,73': 'Cedar Chest',
        '172,225,175': 'Celadon',
        '0,123,167': 'Celadon blue',
        '47,132,124': 'Celadon green',
        '178,255,255': 'Celeste',
        '36,107,206': 'Celtic blue',
        '222,49,99': 'Cerise',
        '0,123,167': 'Cerulean',
        '42,82,190': 'Cerulean blue',
        '109,155,195': 'Cerulean frost',
        '29,172,214': 'Cerulean (Crayola)',
        '0,122,165': 'CG blue',
        '224,60,49': 'CG red',
        '247,231,206': 'Champagne',
        '241,221,207': 'Champagne pink',
        '54,69,79': 'Charcoal',
        '35,43,43': 'Charleston green',
        '230,143,172': 'Charm pink',
        '223,255,0': 'Chartreuse (traditional)',
        '127,255,0': 'Chartreuse (web)',
        '255,183,197': 'Cherry blossom pink',
        '149,69,53': 'Chestnut',
        '226,61,40': 'Chili red',
        '222,111,161': 'China pink',
        '168,81,110': 'China rose',
        '170,56,30': 'VermilionChinese red',
        '133,96,136': 'Chinese violet',
        '255,178,0': 'Chinese yellow',
        '123,63,0': 'Chocolate (traditional)',
        '210,105,30': 'Chocolate (web)',
        '88,17,26': 'Chocolate Cosmos',
        '255,167,0': 'Chrome yellow',
        '152,129,123': 'Cinereous',
        '227,66,52': 'Cinnabar',
        '205,96,126': 'Cinnamon Satin',
        '228,208,10': 'Citrine',
        '158,169,31': 'Citron',
        '127,23,52': 'Claret',
        '0,71,171': 'Cobalt blue',
        '210,105,30': 'Cocoa brown',
        '111,78,55': 'Coffee',
        '185,217,235': 'Columbia Blue',
        '248,131,121': 'Congo pink',
        '140,146,172': 'Cool grey',
        '184,115,51': 'Copper',
        '218,138,103': 'Copper (Crayola)',
        '173,111,105': 'Copper penny',
        '203,109,81': 'Copper red',
        '153,102,102': 'Copper rose',
        '255,56,0': 'Coquelicot',
        '255,127,80': 'Coral',
        '248,131,121': 'Coral pink',
        '137,63,69': 'Cordovan',
        '251,236,93': 'Corn',
        '179,27,27': 'Cornell red',
        '100,149,237': 'Cornflower blue',
        '255,248,220': 'Cornsilk',
        '46,45,136': 'Cosmic cobalt',
        '255,248,231': 'Cosmic latte',
        '129,97,60': 'Coyote brown',
        '255,188,217': 'Cotton candy',
        '255,253,208': 'Cream',
        '220,20,60': 'Crimson',
        '158,27,50': 'CrimsonCrimson (UA)',
        '167,216,222': 'Crystal',
        '245,245,245': 'Cultured',
        '0,255,255': 'Cyan',
        '0,183,235': 'CyanCyan (process)',
        '88,66,124': 'Cyber grape',
        '255,211,0': 'Cyber yellow',
        '245,111,161': 'Cyclamen',
        '102,102,153': 'Blue-gray',
        '101,67,33': 'Dark brown',
        '93,57,84': 'Dark byzantium',
        '38,66,139': 'Dark cornflower blue',
        '0,139,139': 'Dark cyan',
        '83,104,120': 'Dark electric blue',
        '184,134,11': 'Dark goldenrod',
        '1,50,32': 'Dark green',
        '0,100,0': 'Dark green (X11)',
        '26,36,33': 'Dark jungle green',
        '189,183,107': 'Dark khaki',
        '72,60,50': 'Dark lava',
        '83,75,79': 'Dark liver',
        '84,61,55': 'Dark liver (horses)',
        '139,0,139': 'Dark magenta',
        '74,93,35': 'Dark moss green',
        '85,107,47': 'Dark olive green',
        '255,140,0': 'Dark orange',
        '153,50,204': 'Dark orchid',
        '3,192,60': 'Dark pastel green',
        '48,25,52': 'Dark purple',
        '139,0,0': 'Dark red',
        '233,150,122': 'Dark salmon',
        '143,188,143': 'Dark sea green',
        '60,20,20': 'Dark sienna',
        '140,190,214': 'Dark sky blue',
        '72,61,139': 'Dark slate blue',
        '47,79,79': 'Dark slate gray',
        '23,114,69': 'Dark spring green',
        '0,206,209': 'Dark turquoise',
        '148,0,211': 'Dark violet',
        '0,112,60': 'Dartmouth green',
        '85,85,85': 'Davy\'s grey',
        '218,50,135': 'Deep cerise',
        '250,214,165': 'Deep champagne',
        '185,78,72': 'Deep chestnut',
        '0,75,73': 'Deep jungle green',
        '255,20,147': 'Deep pink',
        '255,153,51': 'Deep saffron',
        '0,191,255': 'Deep sky blue',
        '74,100,108': 'Deep Space Sparkle',
        '126,94,96': 'Deep taupe',
        '21,96,189': 'Denim',
        '34,67,182': 'Denim blue',
        '193,154,107': 'Desert',
        '237,201,175': 'Desert sand',
        '105,105,105': 'GreyDim gray',
        '30,144,255': 'Dodger blue',
        '215,24,104': 'Dogwood rose',
        '150,113,23': 'Drab',
        '0,0,156': 'Duke blue',
        '239,223,187': 'Dutch white',
        '85,93,80': 'Ebony',
        '194,178,128': 'Ecru',
        '27,27,27': 'Eerie black',
        '97,64,81': 'Eggplant',
        '240,234,214': 'Eggshell',
        '16,52,166': 'Egyptian blue',
        '22,22,29': 'Eigengrau',
        '125,249,255': 'Electric blue',
        '0,255,0': 'Electric green',
        '111,0,255': 'Electric indigo',
        '204,255,0': 'Electric lime',
        '191,0,255': 'Electric purple',
        '143,0,255': 'Electric violet',
        '80,200,120': 'Emerald',
        '108,48,130': 'Eminence',
        '27,77,62': 'English green',
        '180,131,149': 'English lavender',
        '171,75,82': 'English red',
        '204,71,75': 'English vermillion',
        '86,60,92': 'English violet',
        '0,255,64': 'Erin',
        '150,200,162': 'Eton blue',
        '193,154,107': 'Fallow]]',
        '128,24,24': 'Falu red',
        '181,51,137': 'Fandango',
        '222,82,133': 'Fandango pink',
        '244,0,161': 'Fashion fuchsia',
        '229,170,112': 'Fawn',
        '77,93,83': 'Feldgrau',
        '79,121,66': 'Fern green',
        '108,84,30': 'Field drab',
        '255,84,112': 'Fiery rose',
        '178,34,34': 'Firebrick',
        '206,32,41': 'Fire engine red',
        '233,92,75': 'Fire opal',
        '226,88,34': 'Flame',
        '238,220,130': 'Flax',
        '162,0,109': 'Flirt',
        '255,250,240': 'Floral white',
        '21,244,238': 'Fluorescent blue',
        '95,167,119': 'Forest green (Crayola)',
        '1,68,33': 'Forest green (traditional)',
        '34,139,34': 'Forest green (web)',
        '166,123,91': 'French beige',
        '133,109,77': 'French bistre',
        '0,114,187': 'French blue',
        '253,63,146': 'French fuchsia',
        '134,96,142': 'French lilac',
        '158,253,56': 'French lime',
        '212,115,212': 'French mauve',
        '253,108,158': 'French pink',
        '199,44,72': 'French raspberry',
        '246,74,138': 'French rose',
        '119,181,254': 'French sky blue',
        '136,6,206': 'French violet',
        '233,54,167': 'Frostbite',
        '255,0,255': 'Fuchsia',
        '193,84,193': 'Fuchsia (Crayola)',
        '204,57,123': 'Fuchsia purple',
        '199,67,117': 'Fuchsia rose',
        '228,132,0': 'Fulvous',
        '135,66,31': 'Fuzzy Wuzzy',
        '220,220,220': 'Gainsboro',
        '228,155,15': 'Gamboge',
        '0,127,102': 'Generic viridian',
        '248,248,255': 'Ghost white',
        '96,130,182': 'Glaucous',
        '171,146,179': 'Glossy grape',
        '0,171,102': 'GO green',
        '165,124,0': 'Gold',
        '212,175,55': 'Gold (metallic)',
        '255,215,0': 'Gold (web) (Golden)',
        '230,190,138': 'Gold (Crayola)',
        '133,117,78': 'Gold Fusion',
        '153,101,21': 'Golden brown',
        '252,194,0': 'Golden poppy',
        '255,223,0': 'Golden yellow',
        '218,165,32': 'Goldenrod',
        '103,103,103': 'Granite gray',
        '168,228,160': 'Granny Smith apple',
        '128,128,128': 'Gray (web)',
        '190,190,190': 'Gray (X11 gray)',
        '0,255,0': 'Green',
        '28,172,120': 'Green (Crayola)',
        '0,128,0': 'Green (web)',
        '0,168,119': 'Green (Munsell)',
        '0,159,107': 'Green (NCS)',
        '0,173,67': 'Green (Pantone)',
        '0,165,80': 'Green (pigment)',
        '102,176,50': 'Green (RYB)',
        '17,100,180': 'Green-blue',
        '40,135,200': 'Green-blue (Crayola)',
        '0,153,102': 'Green-cyan',
        '167,244,50': 'Green Lizard',
        '110,174,161': 'Green Sheen',
        '173,255,47': 'Green-yellow',
        '240,232,145': 'Green-yellow (Crayola)',
        '169,154,134': 'Grullo',
        '42,52,57': 'Gunmetal',
        '68,108,207': 'Han blueH',
        '82,24,250': 'Han purple',
        '233,214,107': 'Hansa yellow',
        '63,255,0': 'Harlequin',
        '218,145,0': 'Harvest gold',
        '255,122,0': 'Heat Wave',
        '223,115,255': 'Heliotrope',
        '170,152,168': 'Heliotrope gray',
        '244,0,161': 'Hollywood cerise',
        '240,255,240': 'Honeydew',
        '0,109,176': 'Honolulu blue',
        '73,121,107': 'Hooker\'s green',
        '255,29,206': 'Hot magenta',
        '255,105,180': 'Hot pink',
        '53,94,59': 'Hunter green',
        '113,166,210': 'IcebergI',
        '252,247,94': 'Icterine',
        '49,145,119': 'Illuminating emerald',
        '237,41,57': 'Imperial red',
        '178,236,93': 'Inchworm',
        '76,81,109': 'Independence',
        '19,136,8': 'India green',
        '205,92,92': 'Indian red',
        '227,168,87': 'Indian yellow',
        '75,0,130': 'Indigo',
        '0,65,106': 'Indigo dye',
        '255,79,0': 'International orange (aerospace)',
        '186,22,12': 'International orange (engineering)',
        '192,54,44': 'International orange (Golden Gate Bridge)',
        '90,79,207': 'Iris',
        '179,68,108': 'Irresistible',
        '244,240,236': 'Isabelline',
        '178,255,255': 'Italian sky blue',
        '255,255,240': 'Ivory',
        '0,168,107': 'JadeJ',
        '157,41,51': 'Japanese carmine',
        '91,50,86': 'Japanese violet',
        '248,222,126': 'Jasmine',
        '165,11,94': 'Jazzberry jam',
        '52,52,52': 'Jet',
        '244,202,22': 'Jonquil',
        '189,218,87': 'June bud',
        '41,171,135': 'Jungle green',
        '76,187,23': 'Kelly greenK',
        '58,176,158': 'Keppel',
        '232,244,140': 'Key lime',
        '195,176,145': 'Khaki (web)',
        '240,230,140': 'Khaki (X11) (Light khaki)',
        '136,45,23': 'Kobe',
        '231,159,196': 'Kobi',
        '107,68,35': 'Kobicha',
        '53,66,48': 'Kombu green',
        '79,38,131': 'KSU purple',
        '214,202,221': 'Languid lavenderL',
        '38,97,156': 'Lapis lazuli',
        '255,255,102': 'Laser lemon',
        '169,186,157': 'Laurel green',
        '207,16,32': 'Lava',
        '181,126,220': 'Lavender (floral)',
        '230,230,250': 'Lavender (web)',
        '204,204,255': 'Lavender blue',
        '255,240,245': 'Lavender blush',
        '196,195,208': 'Lavender gray',
        '124,252,0': 'Lawn green',
        '255,247,0': 'Lemon',
        '255,250,205': 'Lemon chiffon',
        '204,160,29': 'Lemon curry',
        '253,255,0': 'Lemon glacier',
        '246,234,190': 'Lemon meringue',
        '255,244,79': 'Lemon yellow',
        '255,255,159': 'Lemon yellow (Crayola)',
        '84,90,167': 'Liberty',
        '173,216,230': 'Light blue',
        '240,128,128': 'Light coral',
        '147,204,234': 'Light cornflower blue',
        '224,255,255': 'Light cyan',
        '200,173,127': 'Light French beige',
        '250,250,210': 'Light goldenrod yellow',
        '211,211,211': 'Light gray',
        '144,238,144': 'Light green',
        '254,216,177': 'Light orange',
        '197,203,225': 'Light periwinkle',
        '255,182,193': 'Light pink',
        '255,160,122': 'Light salmon',
        '32,178,170': 'Light sea green',
        '135,206,250': 'Light sky blue',
        '119,136,153': 'Light slate gray',
        '176,196,222': 'Light steel blue',
        '255,255,224': 'Light yellow',
        '200,162,200': 'Lilac',
        '174,152,170': 'Lilac Luster',
        '191,255,0': 'Lime (color wheel)',
        '0,255,0': 'Lime (web) (X11 green)',
        '50,205,50': 'Lime green',
        '25,89,5': 'Lincoln green',
        '250,240,230': 'Linen',
        '193,154,107': 'Lion',
        '222,111,161': 'Liseran purple',
        '108,160,220': 'Little boy blue',
        '103,76,71': 'Liver',
        '184,109,41': 'Liver (dogs)',
        '108,46,31': 'Liver (organ)',
        '152,116,86': 'Liver chestnut',
        '102,153,204': 'Livid',
        '255,189,136': 'Macaroni and CheeseM',
        '204,51,54': 'Madder Lake',
        '255,0,255': 'Magenta',
        '246,83,166': 'Magenta (Crayola)',
        '202,31,123': 'Magenta (dye)',
        '208,65,126': 'Magenta (Pantone)',
        '255,0,144': 'Magenta (process)',
        '159,69,118': 'Magenta haze',
        '170,240,209': 'Magic mint',
        '242,232,215': 'Magnolia',
        '192,64,0': 'Mahogany',
        '251,236,93': 'Maize',
        '242,198,73': 'Maize (Crayola)',
        '96,80,220': 'Majorelle blue',
        '11,218,81': 'Malachite',
        '151,154,170': 'Manatee',
        '243,122,72': 'Mandarin',
        '253,190,2 ': 'Mango',
        '255,130,67': 'Mango Tango',
        '116,195,101': 'Mantis',
        '136,0 ,133': 'Mardi Gras',
        '234,162,33': 'Marigold',
        '195,33,72': 'Maroon (Crayola)',
        '128,0 ,0 ': 'Maroon (web)',
        '176,48,96': 'Maroon (X11)',
        '224,176,255': 'Mauve',
        '145,95,109': 'Mauve taupe',
        '239,152,170': 'Mauvelous',
        '71,171,204': 'Maximum blue',
        '48,191,191': 'Maximum blue green',
        '172,172,230': 'Maximum blue purple',
        '94,140,49': 'Maximum green',
        '217,230,80': 'Maximum green yellow',
        '115,51,128': 'Maximum purple',
        '217,33,33': 'Maximum red',
        '166,58,121': 'Maximum red purple',
        '250,250,55': 'Maximum yellow',
        '242,186,73': 'Maximum yellow red',
        '76,145,65': 'May green',
        '115,194,251': 'Maya blue',
        '102,221,170': 'Medium aquamarine',
        '0,0,205': 'Medium blue',
        '226,6,44': 'Medium candy apple red',
        '175,64,53': 'Medium carmine',
        '243,229,171': 'Medium champagne',
        '186,85,211': 'Medium orchid',
        '147,112,219': 'Medium purple',
        '60,179,113': 'Medium sea green',
        '123,104,238': 'Medium slate blue',
        '0,250,154': 'Medium spring green',
        '72,209,204': 'Medium turquoise',
        '199,21,133': 'Medium violet-red',
        '248,184,120': 'Mellow apricot',
        '248,222,126': 'Mellow yellow',
        '254,186,173': 'Melon',
        '211,175,55': 'Metallic gold',
        '10,126,140': 'Metallic Seaweed',
        '156,124,56': 'Metallic Sunburst',
        '228,0,124': 'Mexican pink',
        '126,212,230': 'Middle blue',
        '141,217,204': 'Middle blue green',
        '139,114,190': 'Middle blue purple',
        '139,134,128': 'Middle grey',
        '77,140,87': 'Middle green',
        '172,191,96': 'Middle green yellow',
        '217,130,181': 'Middle purple',
        '229,144,115': 'Middle red',
        '165,83,83': 'Middle red purple',
        '255,235,0': 'Middle yellow',
        '236,177,118': 'Middle yellow red',
        '112,38,112': 'Midnight',
        '25,25,112': 'Midnight blue',
        '0,73,83': 'Midnight green (eagle green)',
        '255,196,12': 'Mikado yellow',
        '255,218,233': 'Mimi pink',
        '227,249,136': 'Mindaro',
        '54,116,125': 'Ming',
        '245,220,80': 'Minion yellow',
        '62,180,137': 'Mint',
        '245,255,250': 'Mint cream',
        '152,255,152': 'Mint green',
        '187,180,119': 'Misty moss',
        '255,228,225': 'Misty rose',
        '150,113,23': 'Mode beige',
        '141,163,153': 'Morning blue',
        '138,154,91': 'Moss green',
        '48,186,143': 'Mountain Meadow',
        '153,122,141': 'Mountbatten pink',
        '24,69,59': 'MSU green',
        '197,75,140': 'Mulberry',
        '200,80,155': 'Mulberry (Crayola)',
        '255,219,88': 'Mustard',
        '49,120,115': 'Myrtle green',
        '214,82,130': 'Mystic',
        '173,67,121': 'Mystic maroon',
        '246,173,198': 'Nadeshiko pink',
        '250,218,94': 'Naples yellow',
        '255,222,173': 'Navajo white',
        '0,0,128': 'Navy blue',
        '25,116,210': 'Navy blue (Crayola)',
        '70,102,255': 'Neon blue',
        '255,163,67 ': 'Neon Carrot',
        '57,255,20': 'Neon green',
        '254,65,100': 'Neon fuchsia',
        '215,131,127': 'New York pink',
        '114,116,114': 'Nickel',
        '164,221,237': 'Non-photo blue',
        '233,255,219': 'Nyanza',
        '72,191,145': 'Ocean green',
        '204,119,34': 'Ochre',
        '67,48,46': 'Old burgundy',
        '207,181,59': 'Old gold',
        '253,245,230': 'Old lace',
        '121,104,120': 'Old lavender',
        '103,49,71': 'Old mauve',
        '192,128,129': 'Old rose',
        '132,132,130': 'Old silver',
        '128,128,0': 'Olive',
        '107,142,35': 'Olive Drab (#3)',
        '60,52,31': 'Olive Drab #7',
        '181,179,92': 'Olive green',
        '154,185,115': 'Olivine',
        '53,56,57': 'Onyx',
        '168,195,188': 'Opal',
        '183,132,167': 'Opera mauve',
        '255,127,0': 'Orange',
        '255,117,56': 'Orange (Crayola)',
        '255,88,0': 'Orange (Pantone)',
        '255,165,0': 'Orange (web)',
        '255,159,0': 'Orange peel',
        '255,104,31': 'Orange-red',
        '255,83,73': 'Orange-red (Crayola)',
        '250,91,61': 'Orange soda',
        '245,189,31': 'Orange-yellow',
        '248,213,104': 'Orange-yellow (Crayola)',
        '218,112,214': 'Orchid',
        '242,189,205': 'Orchid pink',
        '226,156,210': 'Orchid (Crayola)',
        '45,56,58': 'Outer space (Crayola)',
        '255,110,74': 'Outrageous Orange',
        '74,0,0': 'Oxblood',
        '0,33,71': 'Oxford blue',
        '132,22,23': 'OU Crimson red',
        '0,102,0': 'Pakistan green',
        '104,40,96': 'Palatinate purple',
        '188,212,230': 'Pale aqua',
        '155,196,226': 'Pale cerulean',
        '237,122,155': 'Pale Dogwood',
        '250,218,221': 'Pale pink',
        '250,230,250': 'Pale purple (Pantone)',
        '201,192,187': 'Pale silver',
        '236,235,189': 'Pale spring bud',
        '120,24,74': 'Pansy purple',
        '0,155,125': 'Paolo Veronese green',
        '255,239,213': 'Papaya whip',
        '230,62,98': 'Paradise pink',
        '241,233,210': 'Parchment',
        '80,200,120': 'Paris Green',
        '222,165,164': 'Pastel pink',
        '128,0,128': 'Patriarch',
        '83,104,120': 'Payne\'s grey',
        '255,229,180': 'Peach',
        '255,203,164': 'Peach (Crayola)',
        '255,218,185': 'Peach puff',
        '209,226,49': 'Pear',
        '183,104,162': 'Pearly purple',
        '204,204,255': 'Periwinkle',
        '195,205,230': 'Periwinkle (Crayola)',
        '225,44,44': 'Permanent Geranium Lake',
        '28,57,187': 'Persian blue',
        '0,166,147': 'Persian green',
        '50,18,122': 'Persian indigo',
        '217,144,88': 'Persian orange',
        '247,127,190': 'Persian pink',
        '112,28,28': 'Persian plum',
        '204,51,51': 'Persian red',
        '254,40,162': 'Persian rose',
        '236,88,0': 'Persimmon',
        '139,168,183': 'Pewter Blue',
        '223,0,255': 'Phlox',
        '0,15,137': 'Phthalo blue',
        '18,53,36': 'Phthalo green',
        '46,39,135': 'Picotee blue',
        '195,11,78': 'Pictorial carmine',
        '253,221,230': 'Piggy pink',
        '1,121,111': 'Pine green',
        '42,47,35': 'Pine tree',
        '255,192,203': 'Pink',
        '215,72,148': 'Pink (Pantone)',
        '252,116,253': 'Pink flamingo',
        '255,221,244': 'Pink lace',
        '216,178,209': 'Pink lavender',
        '247,143,167': 'Pink Sherbet',
        '147,197,114': 'Pistachio',
        '229,228,226': 'Platinum',
        '142,69,133': 'Plum',
        '221,160,221': 'Plum (web)',
        '89,70,178': 'Plump Purple',
        '93,164,147': 'Polished Pine',
        '134,96,142': 'Pomp and Power',
        '190,79,98': 'Popstar',
        '255,90,54': 'Portland Orange',
        '176,224,230': 'Powder blue',
        '245,128,37': 'Princeton orange',
        '255,239,0 ': 'Process yellow',
        '112,28,28': 'Prune',
        '0,49,83': 'Prussian blue',
        '223,0,255': 'Psychedelic purple',
        '204,136,153': 'Puce',
        '100,65,23': 'Pullman Brown (UPS Brown)',
        '255,117,24': 'Pumpkin',
        '96,0,128': 'Purple',
        '128,0,128': 'Purple (web)',
        '159,0,197': 'Purple (Munsell)',
        '160,32,240': 'Purple (X11)',
        '150,120,182': 'Purple mountain majesty',
        '78,81,128': 'Purple navy',
        '254,78,218': 'Purple pizzazz',
        '156,81,182': 'Purple Plum',
        '154,78,174': 'Purpureus',
        '232,204,215': 'Queen pink',
        '166,166,166': 'Quick Silver',
        '142,58,89': 'Quinacridone magenta',
        '36,33,36': 'Raisin black',
        '251,171,96': 'Rajah',
        '227,11,92': 'Raspberry',
        '145,95,109': 'Raspberry glace',
        '179,68,108': 'Raspberry rose',
        '214,138,89': 'Raw sienna',
        '130,102,68': 'Raw umber',
        '255,51,204': 'Razzle dazzle rose',
        '227,37,107': 'Razzmatazz',
        '141,78,133': 'Razzmic Berry',
        '102,52,153': 'Rebecca Purple',
        '255,0,0': 'Red',
        '238,32,77': 'Red (Crayola)',
        '242,0,60': 'Red (Munsell)',
        '196,2,51': 'Red (NCS)',
        '237,41,57': 'Red (Pantone)',
        '237,28,36': 'Red (pigment)',
        '254,39,18': 'Red (RYB)',
        '255,83,73': 'Red-orange',
        '255,104,31': 'Red-orange (Crayola)',
        '255,69,0': 'Red-orange (Color wheel)',
        '228,0,120': 'Red-purple',
        '253,58,74': 'Red Salsa',
        '199,21,133': 'Red-violet',
        '192,68,143': 'Red-violet (Crayola)',
        '146,43,62': 'Red-violet (Color wheel)',
        '164,90,82': 'Redwood',
        '0,35,135': 'Resolution blue',
        '119,118,150': 'Rhythm',
        '0,64,64': 'Rich black',
        '1,11,19': 'Rich black (FOGRA29)',
        '1,2,3': 'Rich black (FOGRA39)',
        '68,76,56': 'Rifle green',
        '0,204,204': 'Robin egg blue',
        '138,127,128': 'Rocket metallic',
        '169,17,1 ': 'Rojo Spanish red',
        '131,137,150': 'Roman silver',
        '255,0,127': 'Rose',
        '249,66,158': 'Rose bonbon',
        '158,94,111': 'Rose Dust',
        '103,72,70': 'Rose ebony',
        '227,38,54': 'Rose madder',
        '255,102,204': 'Rose pink',
        '237,122,155': 'Rose Pompadour',
        '170,152,169': 'Rose quartz',
        '194,30,86': 'Rose red',
        '144,93,93': 'Rose taupe',
        '171,78,82': 'Rose vale',
        '101,0,11': 'Rosewood',
        '212,0,0': 'Rosso corsa',
        '188,143,143': 'Rosy brown',
        '0,35,102': 'Royal blue (dark)',
        '65,105,225': 'Royal blue (light)',
        '120,81,169': 'Royal purple',
        '250,218,94': 'Royal yellow',
        '206,70,118': 'Ruber',
        '209,0,86': 'Rubine red',
        '224,17,95': 'Ruby',
        '155,17,30': 'Ruby red',
        '168,28,7': 'Rufous',
        '128,70,27': 'Russet',
        '103,146,103': 'Russian green',
        '50,23,77': 'Russian violet',
        '183,65,14': 'Rust',
        '218,44,67': 'Rusty red',
        '139,69,19': 'Saddle brown',
        '255,120,0': 'Safety orange',
        '255,103,0': 'Safety orange (blaze orange)',
        '238,210,2': 'Safety yellow',
        '244,196,48': 'Saffron',
        '188,184,138': 'Sage',
        '35,41,122': 'St. Patrick\'s blue',
        '250,128,114': 'Salmon',
        '255,145,164': 'Salmon pink',
        '194,178,128': 'Sand',
        '150,113,23': 'Sand dune',
        '244,164,96': 'Sandy brown',
        '80,125,42': 'Sap green',
        '15,82,186': 'Sapphire',
        '0,103,165': 'Sapphire blue',
        '45,93,161': 'Sapphire (Crayola)',
        '203,161,53': 'Satin sheen gold',
        '255,36,0': 'Scarlet',
        '255,145,175': 'Schauss pink',
        '255,216,0': 'School bus yellow',
        '102,255,102': 'Screamin\' Green',
        '46,139,87': 'Sea green',
        '1,255,205': 'Sea green (Crayola)',
        '50,20,20': 'Seal brown',
        '255,245,238': 'Seashell',
        '255,186,0': 'Selective yellow',
        '112,66,20': 'Sepia',
        '138,121,93': 'Shadow',
        '119,139,165': 'Shadow blue',
        '0,158,96': 'Shamrock green',
        '143,212,0': 'Sheen green',
        '217,134,149': 'Shimmering Blush',
        '95,167,120': 'Shiny Shamrock',
        '252,15,192': 'Shocking pink',
        '255,111,255': 'Shocking pink (Crayola)',
        '136,45,23': 'Sienna',
        '192,192,192': 'Silver',
        '201,192,187': 'Silver (Crayola)',
        '170,169,173': 'Silver (Metallic)',
        '172,172,172': 'Silver chalice',
        '196,174,173': 'Silver pink',
        '191,193,194': 'Silver sand',
        '203,65,11': 'Sinopia',
        '255,56,85': 'Sizzling Red',
        '255,219,0': 'Sizzling Sunrise',
        '0,116,116': 'Skobeloff',
        '135,206,235': 'Sky blue',
        '118,215,234': 'Sky blue (Crayola)',
        '207,113,175': 'Sky magenta',
        '106,90,205': 'Slate blue',
        '112,128,144': 'Slate gray',
        '41,150,23': 'Slimy green',
        '200,65,134': 'Smitten',
        '16,12,8': 'Smoky black',
        '255,250,250': 'Snow',
        '137,56,67': 'Solid pink',
        '117,117,117': 'Sonic silver',
        '29,41,81': 'Space cadet',
        '128,117,50': 'Spanish bistre',
        '0,112,184': 'Spanish blue',
        '209,0,71': 'Spanish carmine',
        '152,152,152': 'Spanish gray',
        '0,145,80': 'Spanish green',
        '232,97,0': 'Spanish orange',
        '247,191,190': 'Spanish pink',
        '230,0,38': 'Spanish red',
        '0,255,255': 'Spanish sky blue',
        '76,40,130': 'Spanish violet',
        '0,127,92': 'Spanish viridian',
        '167,252,0': 'Spring bud',
        '135,255,42': 'Spring Frost',
        '0,255,127': 'Spring green',
        '236,235,189': 'Spring green (Crayola)',
        '0,123,184': 'Star command blue',
        '70,130,180': 'Steel blue',
        '204,51,204': 'Steel pink',
        '95,138,139': 'Steel Teal',
        '250,218,94': 'Stil de grain yellow',
        '228,217,111': 'Straw',
        '250,80,83': 'Strawberry',
        '255,147,97': 'Strawberry Blonde',
        '145,78,117': 'Sugar Plum',
        '255,204,51': 'Sunglow',
        '227,171,87': 'Sunray',
        '250,214,165': 'Sunset',
        '207,107,169': 'Super pink',
        '168,55,49': 'Sweet Brown',
        '212,69,0 ': 'Syracuse Orange',
        '217,154,108': 'Tan (Crayola)',
        '242,133,0': 'Tangerine',
        '228,113,122': 'Tango pink',
        '251,77,70': 'Tart Orange',
        '72,60,50': 'Taupe',
        '139,133,137': 'Taupe gray',
        '208,240,192': 'Tea green',
        '248,131,121': 'Tea rose',
        '244,194,194': 'Tea rose',
        '0,128,128': 'Teal',
        '54,117,136': 'Teal blue',
        '207,52,118': 'Telemagenta',
        '226,114,91': 'Terra cotta',
        '216,191,216': 'Thistle',
        '222,111,161': 'Thulian pink',
        '252,137,172': 'Tickle Me Pink',
        '10,186,181': 'Tiffany Blue',
        '219,215,210': 'Timberwolf',
        '238,230,0': 'Titanium yellow',
        '255,99,71': 'Tomato',
        '0,117,94': 'Tropical rainforest',
        '0,115,207': 'True Blue',
        '28,5,179': 'Trypan Blue',
        '62,142,222': 'Tufts blue',
        '222,170,136': 'Tumbleweed',
        '64,224,208': 'Turquoise',
        '0,255,239': 'Turquoise blue',
        '160,214,180': 'Turquoise green',
        '138,154,91': 'Turtle green',
        '250,214,165': 'Tuscan',
        '111,78,55': 'Tuscan brown',
        '124,72,72': 'Tuscan red',
        '166,123,91': 'Tuscan tan',
        '192,153,153': 'Tuscany',
        '138,73,107': 'Twilight lavender',
        '102,2,60': 'Tyrian purple',
        '217,0,76': 'UA red',
        '18,10,143': 'Ultramarine',
        '65,102,245': 'Ultramarine blue',
        '255,111,255': 'Ultra pink',
        '252,108,133': 'Ultra red',
        '99,81,71': 'Umber',
        '255,221,202': 'Unbleached silk',
        '91,146,229': 'United Nations blue',
        '165,0,33 ': 'University of Pennsylvania red',
        '255,255,102': 'Unmellow yellow',
        '1,68,33': 'UP Forest green',
        '123,17,19': 'UP maroon',
        '174,32,41': 'Upsdell red',
        '175,219,245': 'Uranian blue',
        '0,79,152': 'USAFA blue',
        '243,229,171': 'Vanilla',
        '243,143,169': 'Vanilla ice',
        '197,179,88': 'Vegas gold',
        '200,8,21': 'Venetian red',
        '67,179,174': 'Verdigris',
        '227,66,52': 'Vermilion',
        '217,56,30': 'Vermilion',
        '160,32,240': 'Veronica',
        '143,0,255': 'Violet',
        '127,0,255': 'Violet (color wheel)',
        '150,61,127': 'Violet (crayola)',
        '134,1,175': 'Violet (RYB)',
        '238,130,238': 'Violet (web)',
        '50,74,178': 'Violet-blue',
        '118,110,200': 'Violet-blue (Crayola)',
        '247,83,148': 'Violet-red',
        '64,130,109': 'Viridian',
        '0,150,152': 'Viridian green',
        '159,29,53': 'Vivid burgundy',
        '0,204,255': 'Vivid sky blue',
        '255,160,137': 'Vivid tangerine',
        '159,0,255': 'Vivid violet',
        '205,255,0': 'Volt',
        '245,222,179': 'Wheat',
        '255,255,255': 'White',
        '162,173,208': 'Wild blue yonder',
        '212,112,162': 'Wild orchid',
        '255,67,164': 'Wild Strawberry',
        '252,108,133': 'Wild watermelon',
        '167,85,2': 'Windsor tan',
        '114,47,55': 'Wine',
        '103,49,71': 'Wine dregs',
        '255,0,124': 'Winter Sky',
        '86,136,125': 'Wintergreen Dream',
        '201,160,220': 'Wisteria',
        '193,154,107': 'Wood brown',
        '238,237,9 ': 'Xanthic',
        '241,180,47 ': 'Xanthous',
        '255,255,0': 'Yellow',
        '252,232,131': 'Yellow (Crayola)',
        '239,204,0': 'Yellow (Munsell)',
        '255,211,0': 'Yellow (NCS)',
        '254,223,0': 'Yellow (Pantone)',
        '255,239,0': 'Yellow (process)',
        '254,254,51': 'Yellow (RYB)',
        '154,205,50': 'Yellow-green',
        '197,227,132': 'Yellow-green (Crayola)',
        '48,178,26': 'Yellow-green (Color Wheel)',
        '255,174,66': 'Yellow Orange',
        '255,149,5': 'Yellow Orange (Color Wheel)',
        '255,247,0': 'Yellow Sunshine',
        '46,80,144': 'YInMn Blue',
        '57,167,142': 'Zomp'
    }

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
