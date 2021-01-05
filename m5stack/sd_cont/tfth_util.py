import time
import sys

def clear_tdiff():
    tdiff = load_tdiff()
    if tdiff !=0:
        f=open('tdiff','w')
        f.write('0')
        f.close()

def get_time():
    tzone= load_tzone()
    tdiff = load_tdiff()
    tm = time.time() + tdiff + tzone*60*60
    return tm

def load_geo_cfg():
    try:
        from geo_cfg import lat,lon,drx
        return lat,lon,drx
    except Exception as e:
        sys.print_exception(e)
    lat=22.15  # for HK
    lon=114.15
    drx='E'
    save_geo_cfg(lat,lon,drx)
    return lat,lon,drx

def load_tdiff():
    tdiff=0
    try:
        f=open('tdiff')
        tdiff = int(f.read())
        f.close()
    except Exception as e:
        sys.print_exception(e)
        f=open('tdiff','w')
        f.write('0')
        f.close()
    return tdiff

def load_tzone():
    try:
        f=open('tzone.cfg')
        tz=f.read()
        f.close()
        return int(tz)
    except:
        tz=8  # for HONG KONG 
        save_tzone(tz)
        return tz

def save_geo_cfg(lat,lon,drx):
    ss='lat=%s\nlon=%s\ndrx="%s"\n' % (lat,lon,drx)
    f=open('geo_cfg.py','w')
    f.write(ss)
    f.close()
    if 'geo_cfg' in sys.modules:
        del sys.modules['geo_cfg']
    return 'OK'

def save_tdiff(tmx):
    tdiff = tmx -time.time()
    f=open('tdiff','w')
    f.write(str(tdiff))
    f.close()

def save_tzone(tz):
    f=open('tzone.cfg','w')
    f.write(str(tz))
    f.close()
