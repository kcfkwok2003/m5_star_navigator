Height=32
font_path='/sd/chfontx32.cg'
NBYTES=128
ZONE1_V128=128
ZONE2_X4E00=0x4e00
ZONE3_X9FFF=0x9fff

import sys

def set_font_path(p):
    global font_path
    font_path =p

def u_to_cp(ux):
    bs = ux.encode('utf-8')
    if len(bs)==3:
        i2 = bs[0] & 0x0f
        i1 = bs[1] & 0x3f
        i0 = bs[2] & 0x3f
        cp = (i2 << 12) + (i1 << 6) + i0
        return cp
    if len(bs)==1:
        return bs[0]
    return 0


class Table:
    def __init__(self):
        self.dictx={}
        try:
            import efontx32
            self.dictx.update(efontx32.table.dictx)
        except:
            print("fail to import efontx32")
            
    def __getitem__(self,k):
        if k in self.dictx:
            return self.dictx[k]
        try:
            print('k:',k)
            bs =self.get(k)
            self.dictx[k]=bs
            return bs
        except Exception as e:
            sys.print_exception(e)
        return self.dictx[u'\x80']

    def get(self,ux):
        global font_path
        cp = u_to_cp(ux)
        if cp >= ZONE2_X4E00 and cp <= ZONE3_X9FFF:
            f=open(font_path,'rb')
            ofs = NBYTES * (cp - ZONE2_X4E00)
            f.seek(ofs)
            bs = f.read(NBYTES)
            f.close()
            return bs
        raise Exception("char not found")
            
table=Table()

