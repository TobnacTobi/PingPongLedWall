from .display import DisplayInterface
import neopixel
import board

# LED strip configuration:
LED_COUNT      = 300     # Number of LED pixels.
LED_PIN        = board.D18      # GPIO pin connected to the pixels (18 uses PWM!).
LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53
WIDTH = 20

matrix = [
    0,  1,  2,  3,  4,  5,  6,  7,  8,  9,  10,  11,  12,  13,  14,  15,  16,  17,  18,  19, 
    39,  38,  37,  36,  35,  34,  33,  32,  31,  30,  29,  28,  27,  26,  25,  24,  23,  22,  21,  20,
    40,  41,  42,  43,  44,  45,  46,  47,  48,  49,  50,  51,  52,  53,  54,  55,  56,  57,  58,  59,
    79,  78,  77,  76,  75,  74,  73,  72,  71,  70,  69,  68,  67,  66,  65,  64,  63,  62,  61,  60,
    80,  81,  82,  83,  84,  85,  86,  87,  88,  89,  90,  91,  92,  93,  94,  95,  96,  97,  98,  99,
    119,  118,  117,  116,  115,  114,  113,  112,  111,  110,  109,  108,  107,  106,  105,  104,  103,  102,  101,  100,
    120,  121,  122,  123,  124,  125,  126,  127,  128,  129,  130,  131,  132,  133,  134,  135,  136,  137,  138,  139,
    159,  158,  157,  156,  155,  154,  153,  152,  151,  150,  149,  148,  147,  146,  145,  144,  143,  142,  141,  140,
    160,  161,  162,  163,  164,  165,  166,  167,  168,  169,  170,  171,  172,  173,  174,  175,  176,  177,  178,  179,
    199,  198,  197,  196,  195,  194,  193,  192,  191,  190,  189,  188,  187,  186,  185,  184,  183,  182,  181,  180,
    200,  201,  202,  203,  204,  205,  206,  207,  208,  209,  210,  211,  212,  213,  214,  215,  216,  217,  218,  219,
    239,  238,  237,  236,  235,  234,  233,  232,  231,  230,  229,  228,  227,  226,  225,  224,  223,  222,  221,  220,
    240,  241,  242,  243,  244,  245,  246,  247,  248,  249,  250,  251,  252,  253,  254,  255,  256,  257,  258,  259,
    279,  278,  277,  276,  275,  274,  273,  272,  271,  270,  269,  268,  267,  266,  265,  264,  263,  262,  261,  260,
    280,  281,  282,  283,  284,  285,  286,  287,  288,  289,  290,  291,  292,  293,  294,  295,  296,  297,  298,  299
]
#made with following function:
#i = 0
#for y in range(0,15):
#    for x in range (0,20):
#        if(y%2 == 0):
#            print(str(i) + ', ', end='\n' if (x == 19) else ' ')
#        else:
#            print(str(20*(y+1) - x - 1) + ', ', end='\n' if (x == 19) else ' ')
#        i+=1

class LEDDisplay(DisplayInterface):
    strip = None

    def __init__(self, w, h):
        super(LEDDisplay, self).__init__(w, h)
        self.strip = neopixel.NeoPixel(LED_PIN, LED_COUNT, brightness = 1.0, auto_write = False)

    def drawPixel(self, x, y, color):
        # r, g, b = color
        try:
            self.strip.setPixelColor(matrix[y * WIDTH + x], color)
            # self.strip.setPixelColor(matrix[y * WIDTH + x], (r*(self.brightness/100), g*(self.brightness/100), b*(self.brightness/100)))
        except:
            print('Could not draw colors:')
            # print(r)
            # print(g)
            # print(b)

    def run_display(self): # call this in main process permanently
        self.strip.show()

    def setBrightness(self, b): # insert value 0 - 100
        self.strip.brightness = (b/100)