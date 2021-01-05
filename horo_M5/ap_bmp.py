# ap_bmp.py
version='1.0'

import time

def main(vs):
    global var_store
    var_store=vs
    tft=var_store['tft']
    btnC = var_store['btnC']    
    render_bmp(vs,50,0,215,215)
    tft.text('Press C to exit',2,220)
    while True:
        if btnC.value()==0:
            break
        time.sleep(1)
        
def render_bmp(vs,x=50,y=0,w=215,h=215):
    global var_store
    var_store = vs
    btnA = var_store['btnA']
    tft = var_store['tft']
    y0=y
    y = y+h
    f=open('test3.bmp','rb')
    f.seek(0x8a)
    ss = f.read((w+1)*2)
    n=0
    while ss:
        if btnA.value()==0:
            break
        n+=1
        bs=bytearray()
        bx=ss[:]
        while bx:
            bs.append(bx[1])
            bs.append(bx[0])
            bx=bx[2:]
            if btnA.value()==0:
                break
        tft.blit_buffer(bs,x,y,w,1)
        ss=f.read((w+1)*2)
        y-=1
        if y==y0:
            break
    print('n:%s' % n)
