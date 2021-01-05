# horo_main.py
version='1.0'
import network,time
import ubinascii
import urandom
urandom.seed(time.time())
from machine import unique_id, Pin, I2C, Timer, reset
from micropython import schedule
import os
import sys
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
    'epd_type':'M5'
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
        cp(ifn, fn)

def cp(fn1,fn2):
    f1 =open(fn1,'rb')
    f2 =open(fn2,'wb')
    ss = f1.read(1000)
    while ss:
        f2.write(ss)
        ss = f1.read(1000)
    f1.close()
    f2.close()

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
        try:
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
        except Exception as e:
            sys.print_exception(e)
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
        
    from main_codes import MAIN_CONT    
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
        
