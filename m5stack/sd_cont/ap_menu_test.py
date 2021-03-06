# -*- coding: utf-8 -*-
# ap_menu_test.py
version='1.0'

from color import *
import time

MLINES=10

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

def item_dialog(n):
    global tft,menu,msel,dialog_on
    text = menu['items'][msel][0]
    tft.fill_rect(10,40,100,40,NAVY)
    tft.text(text,12,42,WHITE)
    rect(10,40,100,40,WHITE)
    dialog_on=True
    
def clear_dialog():
    global tft
    tft.fill_rect(10,40,100,40,NAVY)
    rect(10,40,100,40,NAVY)
    dialog_on=False
    
def reset(n):
    global tft
    print('reset')
    tft.text('Reseting...',5,5,WHITE)    
    import machine
    machine.reset()
    
def quit(n):
    global quit_f
    print('quit')
    quit_f=True
    
    
def on_up(n):
    global msel,dialog_on
    if dialog_on:
        clear_dialog()
    if msel>0:
        msel-=1
        show_menu()
    print('on_up %s msel:%s' % (menu['name'],msel))

def on_down(n):
    global msel, menu, dialog_on
    if dialog_on:
        clear_dialog()
    if msel < len(menu['items']) -1:
        msel+=1
        print('on_down %s msel:%s' % (menu['name'],msel))
        show_menu()

def on_enter(n):
    global msel, menu
    print('on_enter')
    items=menu['items']
    action= items[msel][1]
    if action:
        action(n)

    
MENU_TEST={
    'name':'Test',
    'items':[
        ('Item 1',item_dialog),
        ('Item 2',item_dialog),
        ('Quit', quit),
        ('Reset',reset),
        ]
    }

def rect(x,y,w,h,c):
    global tft
    tft.hline(x,y, w,c)
    tft.hline(x,y+h,w,c)
    tft.vline(x,y, h,c)
    tft.vline(x+w,y,h,c)

    
def show_menu(refresh=False):
    global msel,mstart,menu,tft
    if refresh:
        tft.fill(NAVY)
    if msel< mstart:
        mstart=msel
    if msel >= mstart+MLINES:
        mstart= msel -MLINES+1

    x=0
    y=0
    w= 320
    h=20
    menu_name=menu['name']
    tft.text(menu_name,x+2,y+5,WHITE)
    rect(x,y,w,h,WHITE)
    
    y+=25
    items = menu['items']
    i=0
    for item in items[mstart:]:
        if i > MLINES:
            break
        menux = item[0]
        if i+mstart==msel:
            tft.text(menux,x,y,color=BLACK,background=WHITE)
        else:
            tft.text(menux,x,y,color=WHITE)
        y+=15
        i+=1
    


def main(vs):
    global var_store,tft,msel,mstart,menu,btn,dialog_on,quit_f
    var_store=vs
    tft = var_store['tft']
    btnA=var_store['btnA']
    btnB=var_store['btnB']
    btnC=var_store['btnC']
    dialog_on=False
    quit_f=False
    msel=0
    mstart=0
    menu=MENU_TEST
    show_menu(True)

    while True:
        if chk_btn():
            if btn['A']:
                on_up('A')
            elif btn['B']:
                on_down('B')
            elif btn['C']:
                on_enter('C')
            
        time.sleep(0.1)
        if quit_f:
            break
