import sys

header="""# -*- coding: utf-8 -*-
Height=%s
NBYTES=%s
dictm={
"""

class MK_FONT:
    def __init__(self, txtfn, fontfn, outfn):
        self.txtfn = txtfn
        self.fontfn = fontfn
        self.outfn = outfn

    def run(self):
        font = __import__(self.fontfn)
        txtfd =open(self.txtfn,'rb')
        lines = txtfd.readlines()
        print('lines:%s' % lines)
        chs =[]
        for line in lines:
            print('line:%s' % line)
            line = line.strip().decode('utf-8')
            for x in line:
                if x not in chs:
                    print('x:%s' % x)
                    chs.append(x)
        chs.sort()
        outfname = '%s.cg' % self.outfn
        print('write to %s' % outfname)
        f=open(outfname, 'wb')
        mapx ={}
        ofs=0
        print("chx:%s" % chs[0])
        bs = font.table.get(chs[0])
        lenx = len(bs)
        for chx in chs:
            print("chx:%s" % chx)
            bs = font.table.get(chx)
            mapx[chx]=ofs
            if len(bs) != lenx:
                err = 'length not match %s ~ %s' % (lenx, len(bs))
                raise BaseException(err)
            f.write(bs)
            ofs+=lenx
        f.close()
        outfname = '%smap.py' % self.outfn
        print('write to %s' % outfname)
        f=open(outfname, 'wb')
        txt=header % (font.Height, lenx)
        if "'" in chs:
            txt +='"%s":%s,\n' % ("'", mapx["'"])
            chs.remove("'")
        if "\\" in chs:
            txt +='"\\\\":%s,\n' %  mapx["\\"]
            chs.remove("\\")
        for chx in chs:
            txt +="'%s':%s,\n" % (chx, mapx[chx])
        txt+='}\n'        
        f.write(txt.encode('utf-8'))
        f.close()

HELP="""Usage:
for chinese characters
python3 extrfont.py words.txt chfontx32 ctfontx32cg

for English characters
python3 extrfont.py ewords.txt efontx32 etfontx32cg
"""


if __name__=='__main__':
    import sys
    try:
        txtfn= sys.argv[1]
        fontfn = sys.argv[2]
        outfn = sys.argv[3]
    except:
        print(HELP)
        sys.exit(1)
    cc = MK_FONT(txtfn, fontfn, outfn)
    cc.run()
