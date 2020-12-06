from __future__ import print_function
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
import numpy as np
import os

def char_to_pixels(text, path='./fonts/arialbd.ttf', fontsize=14):
    """
    Based on https://stackoverflow.com/a/27753869/190597 (jsheperd)
    """
    font = ImageFont.truetype(path, fontsize) 
    # PATH RELATIVE TO cwd:
    #print(os.path.isfile(path))
    #font = ImageFont.truetype('./Raspberry_Code/displays/fonts/dig.ttf', fontsize) 
    w, h = font.getsize(text)  
    h *= 2
    image = Image.new('1', (w, h), 1)
    draw = ImageDraw.Draw(image)
    draw.text((0, 0), text, font=font)
    arr = np.asarray(image)
    arr = np.where(arr, False, True)
    arr = arr[(arr).any(axis=1)]
    arr = np.delete(arr, len(arr[0])-1, 1)
    arr = np.delete(arr, len(arr[0])-1, 1)
    return arr

def display(arr):
    result = np.where(arr, '#', ' ')
    print('\n'.join([''.join(row) for row in result]))

#Test:
#s = "ABCabc"
#arr = char_to_pixels(
#    s, 
#    fontsize=20)
#print(arr.shape)
#display(arr)
#print()