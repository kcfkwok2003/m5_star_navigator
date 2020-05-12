# -*- coding: utf-8 -*-
# tfth.py

VERSION ='tfth-0.1'

from m5stack import *
from math_util import *
import horo_util as hu
import planet_util as pu
from g_sign import g_sign
from g_planet import g_planet

import sys
import time
import gc
from sun import Sun
from moon import Moon
from planet import *
from g_stars import ct as constel

import font as fnt
fnt.table.set_e('etfontx32cg')

var_store={}

ASC_COLOR = FUCHSIA
REQU_COLOR = RED
MC_COLOR = FUCHSIA

WDAYS=['MON','TUE','WED','THU','FRI','SAT','SUN']

BITMASK=[0x01,0x02,0x04,0x08,0x10,0x20,0x40,0x80]
from tfth_util import *
def _cos_deg(ang):
    global convention
    if convention:
        return -cos_deg(ang)
    else:
        return cos_deg(ang)



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

class TFTHoro:
    def __init__(self,tft,tzone=8,lat=22.15,lon=114.15,drx='E',convention=False):
        self.tzone=tzone
        self.lat=lat
        self.lon=lon
        self.drx=drx
        self.set_convention(convention)
        self.g_planet = g_planet
        self.constel = constel
        self.tft=tft
        self.planets={}
        self.planets_angles={}
        
    def cal_horo_info(self):
        self.planets={}
        self.planets_angles={}        
        asc, lst= hu.cal_asc(self.yr,self.mon,self.mday,self.hr,self.minu,self.sec,self.tzone,self.lat,self.lon,self.drx)
        self.asc = asc
        self.lst = lst
        self.sign_angles = hu.cal_sign_angles(asc)
        self.ari_ang = self.sign_angles['ari']
        self.mc = hu.cal_mc(lst, self.ari_ang)
        self.cal_sun_loc()
        self.cal_planets_loc()

    def cal_planets_loc(self):
        sun = self.planets['Sun']
        for pnx in [Mercury(), Venus(), Mars(), Jupiter(), Saturn(), Uranus(), Neptune(), Pluto(), Moon()]:
            pnx.cal(self.days_0, sun)
            self.planets[pnx.name]=pnx
        pnx_names = list(self.planets)
        for pnx_name in pnx_names:
            pnx = self.planets[pnx_name]
            phi = self.ari_ang + pnx.eclon
            while phi in self.planets_angles:
                phi +=0.1
            self.planets_angles[phi]=pnx_name

    def cal_sun_loc(self):
        sun=Sun()
        sun.cal(self.days_0)
        self.planets['Sun']=sun

    def draw_asc(self,xc,yc,r,color):
        global convention
        xl = xc -r
        xr = xc + r
        tft=self.tft
        tft.line(xl,yc,xr,yc,color)
        if convention: # True, arrow in left side
            tft.line(xl,yc,xl+10,yc-3,color)
            tft.line(xl,yc,xl+10,yc-2,color)
            tft.line(xl,yc,xl+10,yc-1,color)
        else:
            tft.line(xr,yc,xr-10,yc-3,color)
            tft.line(xr,yc,xr-10,yc-2,color)
            tft.line(xr,yc,xr-10,yc-1,color)

    def draw_mc(self,xc,yc,r3,mc,c): # c:color
        # draw mc line
        sin_mc = sin_deg(mc)
        _cos_mc = _cos_deg(mc)
        xmc = int(_cos_mc * r3 +xc)
        ymc = int(sin_mc * r3 +yc)
        if xmc > xc:
            xmc2 = xc - (xmc-xc)
        else:
            xmc2 = xc + (xc -xmc)
        if ymc > yc:
            ymc2 = yc - (ymc -yc)
        else:
            ymc2 = yc + (yc - ymc)
        tft = self.tft
        tft.line(xmc,ymc,xmc2,ymc2,c)
        tft.line(xmc+1,ymc,xmc2+1,ymc2,c)

    def draw_sign(self,xc,yc,r1,r3,rs,c):
        s_ang = self.sign_angles
        tft = self.tft
        for s in hu.SIGNS:
            phi = s_ang[s]
            sin_phi = sin_deg(phi)
            _cos_phi = _cos_deg(phi)
            x1 = int(_cos_phi * r1 + xc)
            y1 = int(sin_phi * r1 + yc)
            x3 = int(_cos_phi * r3 + xc)
            y3 = int(sin_phi * r3 + yc)
            tft.line(x1,y1,x3,y3,c)

            #place sign
            sphi = phi + 15
            xsc = int(_cos_deg(sphi) * rs + xc)
            ysc = int(sin_deg(sphi) * rs + yc)
            bs = g_sign[s]
            nbs = self.conv_mono_to_rgb565(bs,NAVY,YELLOW)
            h = int(len(bs)/2.0)
            #frm = framebuf.FrameBuffer(nbs,20,h,framebuf.RGB565)
            ofs=-9
            #tft.blit_buffer(frm,xsc+ofs,ysc+ofs,20,16)
            tft.blit_buffer(nbs,xsc+ofs,ysc+ofs,16,h)
            phi +=30
            del bs
            del nbs
            gc.collect()
            
    def conv_mono_to_rgb565(self,bs,bg,fg):
        # bs is 16 x 16
        nbs =bytearray()
        rbs=bs[:]
        while rbs:
            for i in range(2):
                for j in range(8):
                    if BITMASK[j] & rbs[i]:
                        nbs.append(fg >> 8)
                        nbs.append(fg & 0xff)
                    else:
                        nbs.append(bg >> 8)
                        nbs.append(bg & 0xff)                        
            rbs=rbs[2:]
        return nbs

    def conv_mono2_to_rgb565(self,bs,bg,fg):
        # bs is 12 x 12
        nbs =bytearray()
        rbs=bs[:]
        while rbs:
            for j in range(8):
                if BITMASK[j] & rbs[0]:
                    nbs.append(fg >> 8)
                    nbs.append(fg & 0xff)
                else:
                    nbs.append(bg >> 8)
                    nbs.append(bg & 0xff)
            for j in range(4):
                if BITMASK[j] & rbs[1]:
                    nbs.append(fg >> 8)
                    nbs.append(fg & 0xff)
                else:
                    nbs.append(bg >> 8)
                    nbs.append(bg & 0xff)                    
            rbs=rbs[2:]
        return nbs    
            
    def ra_dec_to_xyplot(self,ra,dec,ari_ang,xc,yc,r6,requ,r8,rr):
        # r6,r7,r8 : for constellation r7: eclipse
        #r6 = 93    # lat -45
        #requ = 63    # lat 0deg
        #r8 = 36    # lat 40deg
        # rr 1pt ~ 1.5deg
        angx=ari_ang + ra
        rd = dec /rr
        r = requ - rd
        sin_phi = sin_deg(angx)
        _cos_phi = _cos_deg(angx)
        x1 = int(_cos_phi * r + xc)
        y1 = int(sin_phi * r + yc)
        return x1,y1
            
            
    def set_convention(self,conventionx): #True: astrology, False:astronomy
        global convention
        convention=conventionx

    def set_datetime(self,yr,mon,mday,hr,minu,sec):
        self.yr=yr
        self.mon=mon
        self.mday=mday
        self.hr=hr
        self.minu=minu
        self.sec=sec
        self.days_0 = pu.days_since_2000_jan_0(yr,mon,mday)

    def show_constellation(self,constellation,ari_ang,xc,yc,r6,requ,r8,rr,c):
        tft=self.tft
        stars= constellation['stars']
        lines = constellation['lines']
        star_pos=[]
        for line in lines:
            s=1
            for star in line:
                ra, dec = stars[star]
                ra = ra * 15
                x,y = self.ra_dec_to_xyplot(ra,dec,ari_ang,xc,yc,r6,requ,r8,rr)
                
                if s:
                    s=0
                    x0=x
                    y0=y
                    continue
                tft.line(x0,y0,x,y,BLUE)
                star_pos.append((x,y))
                #self.star(x,y,WHITE)
                x0=x
                y0=y
        # highlight star
        for x,y in star_pos:
            self.star(x,y, WHITE)
        del star_pos
        
    def star(self,x0,y0,c):
        tft = self.tft
        tft.pixel(x0,y0,c)
        #tft.pixel(x0+1,y0,c)
        #tft.pixel(x0-1,y0,c)
        #tft.pixel(x0,y0+1,c)
        #tft.pixel(x0,y0-1,c)

    def start_gr(self,first_cycle):
        tft=self.tft
        ari_ang = self.ari_ang
        xc = 120
        yc = 120
        r0 = 119
        #r1 = 115
        r2 = 99
        #r3 = 94
        requ = 50   # lat 0deg = equator
        rs = int((r0 + r2) /2.0)
        if first_cycle:
            tft.fill(NAVY)
        else:
            tft.fill_rect(0,0,220,37,NAVY)
            tft.fill_rect(0,37,240,283,NAVY)
                      
        tft.circle(xc,yc,r0,LIME)
        tft.circle(xc,yc,r2,LIME)
        tft.circle(xc,yc,requ,REQU_COLOR)
        self.draw_asc(xc,yc,r2,ASC_COLOR)
        self.draw_mc(xc,yc,r2,self.mc,MC_COLOR)
        self.draw_sign(xc,yc,r0,r2,rs,YELLOW)

        gc.collect()
        
        #show planets
        r4=90
        r5=82

        # r6,r8: for constellation
        r6 = 74  # lat -45 deg
        r8 = 29  # lat 40 deg
        # rr 1pt ~ 1.8deg
        rr=1.8

        last_ang=10
        angs = list(self.planets_angles)
        angs.sort()
        for angx in angs:
            org_angx = angx
            pn_name = self.planets_angles[angx]
            pnx = self.planets[pn_name]

            # indicate line short
            sin_angx = sin_deg(angx)
            _cos_angx = _cos_deg(angx)
            x3 = int(_cos_angx * r2 + xc)
            y3 = int(sin_angx * r2 + yc)
            x4 = int(_cos_angx * r4 + xc)
            y4 = int(sin_angx * r4 + yc)
            tft.line(x3,y3,x4,y4,YELLOW)

            # show planet symbol
            if angx - last_ang < 14:
                angx = last_ang + 14
            sin_angx = sin_deg(angx)
            _cos_angx = _cos_deg(angx)
            x5 = int(_cos_angx * r5 + xc)
            y5 = int(sin_angx * r5 + yc)
            bs = self.g_planet[pn_name]
            nbs = self.conv_mono2_to_rgb565(bs,NAVY,WHITE)
            h = int(len(bs)/2.0)
            ofs=7

            # indicate line long
            tft.line(x4,y4,x5,y5,YELLOW)

            # indicate line to ecliptic circle
            xx,yy =self.ra_dec_to_xyplot(pnx.RA, pnx.Dec, ari_ang, xc, yc, r6, requ, r8, rr)
            tft.line(xx,yy,x5,y5,YELLOW)

            # planet symbol
            tft.blit_buffer(nbs,x5-ofs,y5-ofs,12,h) 
            last_ang = angx
            del bs
            del nbs
        
        # plot ecl circle
        eclon = 0
        eclat = 0
        e = 23.441884
        s=1
        for i in range(144):
            eclon = i * 2.5
            ra,dec = pu.ecl_to_equ(eclon,eclat,e)
            x,y = self.ra_dec_to_xyplot(ra,dec,ari_ang,xc,yc,r6,requ,r8,rr)
            if s:
                s=0
                x0=x
                y0=y
                continue
            #s==0
            s=1
            tft.line(x0,y0,x,y,YELLOW)

        # horizontal line
        alt=0
        azi=0
        s=1
        for i in range(180):
            azi = i * 2
            H, dec = pu.hor_to_equ(alt,azi,self.lat,self.lst)

            x, y = self.ra_dec_to_xyplot(H,dec,ari_ang,xc,yc,r6,requ,r8,rr)
            #print('azi:',azi,'H:',H, 'dec:',dec,'x,y:',x,y)
            if s:
                s=0
                x0=x
                y0=y
                continue
            #s==0
            s=1
            tft.line(x0,y0,x,y,LIME)

        # plot constellation
        for ctx in self.constel:
            self.show_constellation(self.constel[ctx],ari_ang,xc,yc,r6,requ,r8,rr,WHITE)


        gc.collect()

btn={'A':False, 'B':False, 'C':False}

def chk_btn():
    global  var_store
    btnA=var_store['btnA']
    btnB=var_store['btnB']
    btnC=var_store['btnC']
    if btnA.value()==0:
        btn['A']=True
        return True
    else:
        btn['A']=False
    if btnB.value()==0:
        btn['B']=True
        return True
    else:
        btn['B']=False
    if btnC.value()==0:
        btn['C']=True
        return True
    else:
        btn['C']=False
    
    
def main(vs):
    global var_store, free_mem
    var_store = vs
    print("tfth.main")
    horo_main=var_store['horo_main']
    sd = var_store['sd']
    tft = var_store['tft']
    free_mem = var_store['free_mem']
    tzone = load_tzone()
    lat,lon,drx = load_geo_cfg()
    syn=sync_time()
    tm = get_time()
    ct = time.localtime(tm)
    yr,mon,mday,hr,minu,sec,wday,_,=ct    
    tfth = TFTHoro(tft,tzone=tzone, lat=lat,lon=lon,drx=drx)
    tfth.set_datetime(yr,mon,mday,hr,minu,sec)
    var_store['tfth']=tfth
    var_store['tft']=tft
    tft.start_spi()
    first_cycle=True
    while True:
        if chk_btn():
            break
        try:
            _t(horo_main,tfth,tft,first_cycle)
            if first_cycle:
                first_cycle=False
        except Exception as e:
            sys.print_exception(e)
            time.sleep(1)
        i=0
        while True:
            if chk_btn():
                break
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
    # command mode
    free_mem()
    if btn['A']:
        print('ap_lunar')
        from machine import RTC, deepsleep
        rtc = RTC()
        rtc.memory('ap_lunar')
        #tft.text('Lunar calendar...',5,5)
        #time.sleep(1)
        deepsleep(1) # use deepsleep to reset and release all memory        
        
    
def _t(horo_main,tfth,tft,first_cycle):
    tm = get_time()
    ct = time.localtime(tm)
    yr,mon,mday,hr,minu,sec,wday,_,=ct    
    tfth.set_datetime(yr,mon,mday,hr,minu,sec)
    tfth.cal_horo_info()
    tfth.start_gr(first_cycle)

    tft.draw_string_at('%d' % yr,220,5,fnt,fg=WHITE,bg=NAVY)
    tft.draw_string_at('%02d' % mon,268,37,fnt,fg=WHITE,bg=NAVY)
    tft.draw_string_at('%02d' % mday,268,69,fnt,fg=WHITE,bg=NAVY)
    tft.draw_string_at('%s' % WDAYS[wday],244,101,fnt,fg=WHITE,bg=NAVY)

    tft.draw_string_at('%02d' % hr,268,133,fnt,fg=WHITE,bg=NAVY)
    tft.draw_string_at(':%02d' % minu,244,165,fnt,fg=WHITE,bg=NAVY)
    
    gc.collect()

