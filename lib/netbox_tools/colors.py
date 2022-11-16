#!/usr/bin/env python3
'''
Convert rgb to color and vice-versa.
'''
import sys

rgb2color = {}
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

def color(color_name):
    '''
    return the mapped value for color_name, if it's in one
    of the two dictionaries rgb2color/color2rgb.  Else,
    return color_name unchanged.
    '''
    if color_name in rgb2color:
        return rgb2color[color_name]
    if color_name in color2rgb:
        return color2rgb[color_name]
    return color_name

def color_to_rgb(color_name):
    '''
    If color_name is not in color2rgb, and is 6 characters long, we assume it is a valid rgb string and return it unchanged.
    Else, exit with error.
    '''
    if color_name in color2rgb:
        return color2rgb[color_name]
    if len(color_name) == 6:
        return color_name
    print('colors.color_to_rgb: exiting. Unknown color {}.  Valid colors: {}'.format(color_name, ', '.join(color2rgb.keys())))
    sys.exit(1)

def rgb_to_color(rgb):
    '''
    If rgb is in rgb2color, return the color name.  Else, exit with error.
    '''
    if rgb in rgb2color:
        return rgb2color[rgb]
    print('colors.rgb_to_color: exiting. Unknown rgb {}.  Valid rgb: {}'.format(rgb, ', '.join(rgb2color.keys())))
    sys.exit(1)
