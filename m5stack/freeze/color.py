def color565(r, g, b):
    return (r & 0xf8) << 8 | (g & 0xfc) << 3 | b >> 3

RED = color565(255,0,0)
GREEN = color565(0,128,0)
LIME = color565(0,255,0)
BLUE = color565(0,0,255)
YELLOW= color565(255,255,0)
BLACK = color565(0,0,0)
AQUA = color565(0,255,255)
NAVY = color565(0,0,128)
FUCHSIA = color565(255,0,255)
PURPLE = color565(128,0,128)
MAROON = color565(128,0,0)
GREY = color565(128,128,128)
SILVER = color565(192,192,192)
WHITE = color565(255,255,255)


