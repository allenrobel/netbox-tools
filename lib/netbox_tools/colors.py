#!/usr/bin/env python3
rgb2color = dict()
rgb2color['2196f3'] = 'blue'
rgb2color['00bcd4'] = 'cyan'
rgb2color['4caf50'] = 'green'
rgb2color['2f6a31'] = 'green_dark'
rgb2color['3f51b5'] = 'indigo'
rgb2color['ff9800'] = 'orange'
rgb2color['9c27b0'] = 'purple'
rgb2color['f44336'] = 'red'
rgb2color['009688'] = 'teal'
rgb2color['ffeb3b'] = 'yellow'
rgb2color['c0c0c0'] = 'gray_light'
rgb2color['9e9e9e'] = 'gray'
rgb2color['607d8b'] = 'gray_dark'

color2rgb = dict([(value, key) for key, value in rgb2color.items()])

def color(s):
    if s in rgb2color:
        return rgb2color[s]
    elif s in rgb2color:
        return rgb2color[s]
    else:
        return s

def color_to_rgb(s):
    '''
    If s is not in color2rgb, and is 6 characters long, we assume it is a valid rgb string and return it unchanged.
    '''
    if s in color2rgb:
        return color2rgb[s]
    if len(s) == 6:
        return s
    else:
        print('colors.color_to_rgb: exiting. Unknown color {}.  Valid colors: {}'.format(s, ', '.join(color2rgb.keys())))
        exit(1)

def rgb_to_color(s):
    if s in rgb2color:
        return rgb2color[s]
    else:
        print('colors.rgb_to_color: exiting. Unknown rgb {}.  Valid rgb: {}'.format(s, ', '.join(rgb2color.keys())))
        exit(1)