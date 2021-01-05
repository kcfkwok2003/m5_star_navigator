# horo_main.py
version='1.0'
import network,time
import ubinascii
import urandom
urandom.seed(time.time())
from machine import unique_id, Pin, I2C, Timer, reset
from micropython import schedule
import os
import hashlib
import micropython
micropython.alloc_emergency_exception_buf(100)

uid = unique_id()
HEADER='horo-1.0m'
AP_ESSID="horo-%02x%02x" % (uid[-2],uid[-1])
AP_AUTHMODE=3
AP_PASSW=''
WEBREPL_PASSW='1234'

help_dict={
    'epd_type':'epd4in2'
    }
# prepare for global
oled=None
timer=None
wlan=None
sta=None
PASS=None

info={}

for i in range(8):
    AP_PASSW+='%d' % urandom.randint(0,9)

# main.py content
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

info = horo_main.info
ip = info['ip']
apname = info['apname']
tft.fill(NAVY)
tft.text(apname, 5,5, color=WHITE)
tft.text(ip, 5,15,color=WHITE)
tft.text('Use webrepl to program', 5,25,color=WHITE)        
"""

FILE_CONT={}
FILE_CONT['boot.py']="""# This file is executed on every boot (including wake-boot from deepsleep)
#import esp
#esp.osdebug(None)
import webrepl
webrepl.start()
"""
FILE_CONT['webrepl_cfg.py']="PASS = '1234'\n"
FILE_CONT['ap0.py']="PASS ='%s'\n" % AP_PASSW


def install(folder):
    fp='sd/%s/filelist.txt' % folder
    f=open(fp)
    lines = f.readlines()
    f.close()
    for line in lines:
        fn = line.strip()
        ifn ='sd/%s/%s' % (folder,fn)
        print('read "%s"' % ifn)
        f=open( ifn,'rb')
        cont=f.read()
        f.close()
        f=open(fn,'wb')
        f.write(cont)
        f.close()

def cp(fn1,fn2):
    f=open(fn1,'rb')
    cont=f.read()
    f.close()
    f=open(fn2,'wb')
    f.write(cont)
    f.close()    

def bkpk():
    fs=os.listdir('')
    if 'sd' not in fs:
        print('no sd, backup failure')
        return
    uid = get_uid().decode('utf-8')
    fs =os.listdir('sd')
    if uid not in fs:
        os.mkdir('sd/'+uid)
    cp('passkey','sd/%s/passkey' % uid)

def rcpk():
    fs=os.listdir('')
    if 'sd' not in fs:
        print('no sd, recover failure')
        return
    uid = get_uid().decode('utf-8')
    fs =os.listdir('sd')
    if uid not in fs:
        print('no passkey folder, recover failure')
        return
    cp('sd/%s/passkey' % uid,'passkey')

HELP_TEXT="""
# for the 1st time setup:
>>>import horo_main as m
>>>m.get_uid()  # get uid for passkey registration
>>>m.setup_main(board,ssid,password,[passkey])
# insert horo sdcard and reboot
>>>m.reset()
# afer reboot, install horo
>>>m=horo_main;m.install('horo_%(epd_type)s')

# for 1st time start sdcard
>>>from sd import SD
>>>sd=SD(cs=13,mosi=15,sck=14,miso=2)
>>>sd.start()
# to check sd mounted?
>>>sd.mounted

# other commands:
m.bkpk()   # backup passkey to sd
m.rcpk()   # recover passkey from sd
""" % help_dict

def help():
    print(HELP_TEXT)

    

def get_uid():
    uid = ubinascii.hexlify(unique_id())
    return uid

def verify_key(passkey):
    N1,N2,N3,N4,N5 = [3,5,2,7,3]   # secrets
    uid = ubinascii.hexlify(unique_id()).upper()
    x = hashlib.sha1(uid)
    y = hashlib.sha1(uid[N1:])
    vs = x.digest()
    ws = y.digest()

    phash=0
    for v in vs[N2:]:
        if type(v)!=type(1):
            v= ord(v)
        phash=phash*N3 + v
    for v in ws[N4:]:
        if type(v)!=type(1):
            v= ord(v)
        phash=phash*N5 + v
    phash=str(phash)
    if phash == passkey:
        return True
    return False



def setup_webrepl():
    global PASS
    if PASS:
        return PASS
    fs = os.listdir()
    if 'webrepl_cfg.py' in fs:
        from webrepl_cfg import PASS
        return PASS
    f=open('webrepl_cfg.py','w')
    f.write("PASS = '%s'\n" % WEBREPL_PASSW)
    f.close()
    return ''

    
def setup_ap(scl=21,sda=22,rst=None):
    global wlan, info
    from ap0 import PASS
    wlan = network.WLAN(network.AP_IF)
    print('setup_ap:%s' % wlan.active())
    if wlan.active():
        wlan.active(False)
    wlan.active(True)
    wlan.config(essid=AP_ESSID)
    wlan.config(authmode=AP_AUTHMODE, password=PASS)
    ips = wlan.ifconfig()
    webrepl_pass = setup_webrepl()
    info['HEADER']=HEADER
    info['apname']=AP_ESSID
    info['appass']=PASS
    info['webrepl_pass']=webrepl_pass
    info['ip']=ips[0]
    return wlan

def setup_ap1():
    global wlan, info
    from ap0 import PASS
    wlan = network.WLAN(network.AP_IF)
    print('setup_ap:%s' % wlan.active())
    if wlan.active():
        wlan.active(False)
    wlan.active(True)
    wlan.config(essid=AP_ESSID)
    wlan.config(authmode=AP_AUTHMODE, password=PASS)
    ips = wlan.ifconfig()
    webrepl_pass = setup_webrepl()
    info['HEADER']=HEADER
    info['apname']=AP_ESSID
    info['appass']=PASS
    info['webrepl_pass']=webrepl_pass
    info['ip']=ips[0]
    return wlan, info

def setup_sta(scl=21,sda=22,rst=None):
    global sta, info
    webrepl_pass = setup_webrepl()
    msg='Connecting...'
    info['HEADER']=HEADER
    fs = os.listdir()
    if 'ap.py' in fs:
        from ap import apname, appass
        sta = network.WLAN(network.STA_IF)
        sta.active(True)
        sta.connect(apname,appass)
        expire=time.time()+ 10
        while time.time() < expire:
            if sta.isconnected():
                break
        if sta.isconnected():
            ips = sta.ifconfig()
            info['apname']=apname
            info['ip']=ips[0]
            info['webrepl_pass']=webrepl_pass
            return sta
        sta.active(False)
    # connected failure
    msg='no essid to connect'
    info['msg']=msg
    info['apname']='-----'
    info['ip']='-'
    info['webrepl_pass']=webrepl_pass
    raise Exception(msg)
        
def setup_main(board=None,apname=None,appass=None,inpasskey=None):
    passkey= inpasskey
    if not passkey:
        try:
            f=open('passkey')
            passkey=f.read()
            f.close()
        except:
            print('no passkey!')
            return
    if not verify_key(passkey):
        print('passkey not match!')
        return
    if inpasskey:
        f=open('passkey','w')
        f.write(inpasskey)
        f.close()
        
    main_cont = MAIN_CONT.get(board,None)
    if main_cont is None:
        print('usage:setup_main(board,apname,appass,passkey=None)')
        print('board: T5,T8,wfk')
        print('apname: wifi ssid')
        print('appass: wifi password')
        return
    f=open('main.py','w')
    f.write(main_cont)
    f.close()
    print('main.py created for '+board)
    print('press reset to reboot')
    fns = FILE_CONT.keys()
    for fn in fns:
        f=open(fn,'w')
        f.write(FILE_CONT[fn])
        f.close()
        print('update '+fn)
    if apname is not None and appass is not None:
        f=open('ap.py','w')
        f.write("apname='%s'\nappass='%s'" % (apname,appass))
        f.close()
        print('ap.py updated')
        
