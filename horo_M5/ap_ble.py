# ap_ble.py
version='1.0'

from color import *
import time

def start_ble(var_store):
    btnC= var_store['btnC']
    hm = var_store['horo_main']
    tft = var_store['tft']
    info = hm.info
    apname = info['apname']
    ip = info['ip']
    tft.fill_rect(20,20,200,100,NAVY)
    tft.rect(20,20,200,100,LIME)
    tft.text(apname, 25,30, color=WHITE)
    tft.text(ip, 25,40,color=WHITE)    
    tft.text('starting ble',25,50,color=WHITE)
    import ble_set_ap
    ble_uart = ble_set_ap.start(hm.AP_ESSID)
    var_store['ble_uart']=ble_uart
    var_store['ble_started']=True
    tft.text('BLE:%s' % hm.AP_ESSID, 25,50,color=WHITE)
    tft.text('Press C to exit',25,60)    
    while True:
        if btnC.value()==0:
            break
        time.sleep(1)        

def main(vs):
    start_ble(vs)
