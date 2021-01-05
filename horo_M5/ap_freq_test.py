# -*- coding: utf-8 -*-
# ap_freq_test.py
version='1.0'
from color import *
from machine import PWM, Pin
import time

btn={'A':False, 'B':False, 'C':False}
def chk_btn():
    global  var_store
    btnA=var_store['btnA']
    btnB=var_store['btnB']
    btnC=var_store['btnC']
    if btnA.value()==0:
        if not btn['A']:
            btn['A']=True
            return True
    else:
        btn['A']=False
    if btnB.value()==0:
        if not btn['B']:
            btn['B']=True
            return True
    else:
        btn['B']=False
    if btnC.value()==0:
        if not btn['C']:
            btn['C']=True
            return True
    else:
        btn['C']=False
        
def inc_freq(n):
    global tft, freq,p25
    freq +=1000
    tft.fill_rect(0,10,128,16,NAVY)    
    tft.text('{:^10}'.format(freq),5,10,WHITE)
    p25.freq(freq)
    p25.duty(100)
    
def dec_freq(n):
    global tft, freq,p25
    freq -=1000
    if freq < 0:
        freq=0
    tft.fill_rect(0,10,128,16,NAVY)        
    tft.text('{:^10}'.format(freq),5,10,WHITE)
    p25.freq(freq)
    p25.duty(100)    

def set_mute(n):
    global tft, freq,p26
    freq=0
    tft.fill_rect(0,10,128,16,NAVY)
    tft.text('{:^10}'.format('mute'),5,10,WHITE)
    p25.duty(0)
    
def main(vs):
    global tft,var_store,freq,mute,p25
    var_store=vs
    freq=1000
    mute=True
    print('ap_freq_test run')
    tft=var_store['tft']
    horo_main = var_store['horo_main']
    btnA = var_store['btnA']
    tft.fill(NAVY)
    tft.text('{:^10}'.format('mute'),5,10,WHITE)
    p25=PWM(Pin(25))
    p25.duty(0)

    while True:
        if chk_btn():
            if btn['A']:
                inc_freq('A')
            elif btn['B']:
                dec_freq('B')
            elif btn['C']:
                set_mute('C')
            
        time.sleep(0.1)


