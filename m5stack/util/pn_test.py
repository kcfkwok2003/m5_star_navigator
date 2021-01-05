from g_planet_1 import *

BITMASK =  [0x01,0x02,0x04,0x08,0x10,0x20,0x40,0x80]
INVMASK =  [0x7f,0xbf,0xdf,0xef,0xf7,0xfb,0xfd,0xfe]

def hline(hb,lb,y):
    hs =''
    for bx in [hb,lb]:
        for bm in BITMASK:
            if (bx & bm):
                hs +='*'
            else:
                hs +='-'
    print(hs)
                
def test():
    bs = g_planet['Sun']
    y=0
    while bs:
        hb,lb,bs = bs[0],bs[1],bs[2:]
        hline(hb,lb,y)
        y+=1
        

test()
