# -*- coding: utf-8 -*-

import tfontx32 as fnt
BITMASK=[0x80,0x40,0x20,0x10,0x08,0x04,0x02,0x01]

h=fnt.Height

def show_chr(chx):
    bs =fnt.table.get(chx)
    ww = int(len(bs)/h)
    txt=''
    for j in range(h):
        for i in range(ww):
            bx = bs[j*ww + i]
            for msk in BITMASK:
                if msk & bx:
                    txt+='*'
                else:
                    txt+='-'
        txt+='\n'
    print (txt)

def test():
    for ch in 'THU':
        show_chr(ch)

test()

