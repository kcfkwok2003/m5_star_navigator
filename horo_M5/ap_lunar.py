# -*- coding: utf-8 -*-
# ap_lunar.py
version='1.0'

from color import *
from tfth_util import *
import lunar as ln
import time
import sys
import font as fnt
fnt.table.set_c('ctfontx32cg')
fnt.table.set_e('etfontx32cg')

WDAYS=['MON','TUE','WED','THU','FRI','SAT','SUN']
def sync_time():
    import ntptime
    try:
        print('sync time')
        ntptime.settime()
        clear_tdiff()
        return True
    except Exception as e:
        sys.print_exception(e)
        print('sync time failure')

def main(vs):
    global var_store, tft
    var_store=vs
    tft = var_store['tft']
    tft.fill(NAVY)
    syn = sync_time()
    while True:
        tm = get_time()
        ct = time.localtime(tm)
        yr,mon,mday,hr,minu,sec,wday,_,=ct
        show_lunar(yr,mon,mday,hr,minu,sec)
        show_datetime(yr,mon,mday,hr,minu,sec,wday)
        i=0
        while True:
            time.sleep(0.5)
            tm = get_time()
            ct = time.localtime(tm)
            yr,mon,mday,hr,minu,sec,wday,_,=ct
            colon=' '
            if i:
                colon=':'
            i = not i
            tft.draw_string_at(colon,244,165,fnt,fg=WHITE,bg=NAVY)
            if sec==0:
                if minu==0 or not syn:
                    # sync every hour
                    syn = sync_time()
                break

def show_lunar(yr,mon,mday,hr,minu,sec):
    global tft
    ct = time.mktime((yr,mon,mday,hr,minu,sec,0,0,0))
    lnx = ln.Lunar(ct)
    gz_yr = lnx.gz_year()
    sx_yr = lnx.sx_year()
    xyr, xmon, xday = lnx.ln_date()
    jie, ofs = lnx.ln_jie_2()
    gz_hr, gz_ke, gz_kev = lnx.gz_hour()
    if gz_ke >0:
        gz_hr += gz_kev
    x=10
    y=5
    tft.draw_string_at('農曆',x,y+0,fnt,bg=NAVY)
    tft.draw_string_at('%s%s年' % (gz_yr,sx_yr), x,y+32, fnt,bg=NAVY)
    tft.draw_string_at('%s月%s' % (lnx.lm[xmon-1], lnx.ld[(xday-1)*2:xday*2]), x,y+64,fnt,bg=NAVY)
    tft.draw_string_at('%s月' % lnx.gz_month(),x,y+96,fnt,bg=NAVY)
    tft.draw_string_at('%s日' % lnx.gz_day(),x,y+128,fnt,bg=NAVY)
    tft.draw_string_at('%s' % gz_hr,x,y+160,fnt,bg=NAVY)
    print('ofs:%d' % ofs)
    if ofs==0:
        tft.draw_string_at('%s' % jie,x,y+192,fnt,bg=NAVY)
    else:
        tft.draw_string_at('%s+%d' % (jie,ofs),x,y+192,fnt,bg=NAVY)

def show_datetime(yr,mon,mday,hr,minu,sec,wday):
    global tft
    tft.draw_string_at('%d' % yr,220,5,fnt,fg=WHITE,bg=NAVY)
    tft.draw_string_at('%02d' % mon,268,37,fnt,fg=WHITE,bg=NAVY)
    tft.draw_string_at('%02d' % mday,268,69,fnt,fg=WHITE,bg=NAVY)
    tft.draw_string_at('%s' % WDAYS[wday],244,101,fnt,fg=WHITE,bg=NAVY)

    tft.draw_string_at('%02d' % hr,268,133,fnt,fg=WHITE,bg=NAVY)
    tft.draw_string_at(':%02d' % minu,244,165,fnt,fg=WHITE,bg=NAVY)

    
