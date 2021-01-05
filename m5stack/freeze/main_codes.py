# main_codes.py
# main.py content
version='1.0'
MAIN_CONT={}
MAIN_CONT['M5']="""
# main.py
version='1.0'
import gc
import sys
from machine import RTC, deepsleep,Pin
from color import *
btnC=Pin(37, Pin.IN, Pin.PULL_UP)
btnB=Pin(38, Pin.IN, Pin.PULL_UP)
btnA=Pin(39, Pin.IN, Pin.PULL_UP)

def free_mem():
    for item in sys.modules:
        del sys.modules[item]
    objs = globals()
    for obj in ['tfth','m5stack']:
        if obj in objs:
            print('del %s' % objs[obj])
            del objs[obj]
    gc.collect()
    
try:
    import horo_main1 as horo_main
    print('horo_main1 used')
except Exception as e:
    import horo_main
try:
    horo_main.setup_sta()
except Exception as e:
    sys.print_exception(e)
from sd import SD
sd=SD(cs=4,mosi=23,sck=18,miso=19)
import m5stack
tft= m5stack.TFT()
tft.start_spi()
tft.fill_rect(0,0,320,20,NAVY)
tft.text('starting...',5,5)
import gc
gc.collect()
var_store={'tft':tft, 'horo_main':horo_main,'sd':sd, 'free_mem':free_mem,'btnA':btnA, 'btnB':btnB,'btnC':btnC}
if btnA.value()==0:
    import ap_menu
    app_name =ap_menu.main(var_store)
    while app_name:
        old_app_name=app_name
        app = __import__(old_app_name)
        app_name= app.main(var_store)
        del sys.modules[old_app_name]
        free_mem()
else:    
    rtc = RTC()
    app_name=rtc.memory()
    if app_name:
        app=__import__(app_name.decode('utf-8'))
        app.main(var_store)
        sys.exit(1)
               
    import ap_bmp
    ap_bmp.render_bmp(var_store)
    free_mem()
    import tfth
    app_name = tfth.main(var_store)
    free_mem()
    while app_name:
        old_app_name=app_name
        app = __import__(old_app_name)
        app_name= app.main(var_store)
        del sys.modules[old_app_name]
        free_mem()

tft.fill(NAVY)
info = horo_main.info
ip = info['ip']
if ip=='-':
    horo_main.setup_ap1()
    tft.text(info['appass'], 5,35, color=WHITE)

ip = info['ip']
apname = info['apname']
tft.text(apname, 5,5, color=WHITE)
tft.text(ip, 5,15,color=WHITE)
tft.text('Use webrepl to program', 5,25,color=WHITE)        
"""
