# -*- coding: utf-8 -*-
# hello.py
version='1.0'
import time
from color import *

def main(vs):
    global var_store
    var_store=vs
    btnC = var_store['btnC']
    tft = var_store['tft']
    tft.fill(NAVY)
    tft.rect(20,20,200,100,LIME)
    tft.text('Hello World!',25,50)
    tft.text('Press C to exit',25,60)
    cnt=0
    while True:
        if btnC.value()==0:
            break
        time.sleep(1)
        tft.text('%s' % cnt, 25,80)
        cnt+=1
