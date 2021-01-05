# -*- coding: utf-8 -*-

import font as fnt
fnt.table.set_c('ctfontx32cg')
fnt.table.set_e('etfontx32cg')

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
    for ch in '農曆庚子+123':
        show_chr(ch)

test()
