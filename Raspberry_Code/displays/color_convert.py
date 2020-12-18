import math

def RGBToOneValue(r, g, b):
    value = math.floor(r)<<16
    value += math.floor(g)<<8
    value += math.floor(b)
    return math.floor(value)

#from: https://axonflux.com/handy-rgb-to-hsl-and-rgb-to-hsv-color-model-c
# h, s, v are in [0, 1]

def HSVtoRGB(h, s, v):
    i = math.floor(h * 6)
    f = h * 6 - i
    p = v * (1-s)
    q = v * (1-f*s)
    t = v * (1 - (1-f)*s)

    i %= 6

    if(i == 0):
        rgbTuple = (v, t, p)
    elif(i == 1):
        rgbTuple = (q, v, p)
    elif(i == 2):
        rgbTuple = (p, v, t)
    elif(i == 3):
        rgbTuple = (p, q, v)
    elif(i == 4):
        rgbTuple = (t, p, v)
    else: # i == 5
        rgbTuple = (v, p, q)

    r, g, b = rgbTuple
    return (r*255, g*255, b*255)
    #return RGBToOneValue(r*255, g*255, b*255)

def MixColors(color1, color2, mixture): # color tuples need to have same amount of elements; mixture in [0, 1.0]
    # if(not len(color1) == len(color2)):
    #     raise Exception('colors dont have same components')
    ret = ()
    for i in range(len(color1)):
        a = math.floor((mixture)*(color1[i]) + (color2[i])*(1-mixture))
        ret = ret + (a,)
    return ret