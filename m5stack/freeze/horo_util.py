from math_util import *

SIGNS=['ari','tau','gem','can','leo','vir','lib','sco','sag','cap','aqu','pis']

def cal_asc(yr,mon,mday,hr,minu,sec,tzone,lat,lon,drx='E'):
    dcd = hms_to_decday(hr,minu,sec)
    gh,gm,gs = hmsCIVIL_to_hmsGMT(hr,minu,sec,tzone)
    gst = ymdhmsGMT_to_gst(yr,mon,mday,gh,gm,gs)
    lst = gst_to_lst(gst,lon,drx)
    jd = ymd_to_jd(yr,mon,mday+dcd)
    eps = cal_eps(jd)
    asc = cal_asc_from_lst(lst,lat,eps)
    return asc,lst

def cal_asc_from_lst(lst, lat, eps):
    ramc = lst * 15  # hr to degree
    y = cos_deg(ramc)
    x = -(sin_deg(eps) * tan_deg(lat) + cos_deg(eps) * sin_deg(ramc))
    asc = atan2_deg(y, x)
    return asc

def cal_B(yr):
    jd = date_to_jd(yr,1,0.0)
    S = jd- 2415020.0
    T=S / 36525.0
    R= 6.6460656 + (2400.051262 * T) + (0.00002581 * T*T)
    U=R-(24*(yr-1900))
    B=24 - U
    return B

def cal_eps(d):
    # d: julian day
    T = d / 36525.0 # number of Julian centuries since epoch 1900
    de =( 46.845 * T + 0.0059*T*T - 0.00181*T*T*T)/3600.0
    e = 23.452294 - de
    return e

def cal_mc(lst, ari_ang):
    alst = lst * 15
    if alst <0:
        alst = 360+ lst
    ang = ari_ang + alst
    if ang > 360:
        ang = ang -360
    return ang

def cal_sign_angles(asc):
    if asc < 0:
        asc = 360 + asc

    s_ang={}
    ang=360 - asc
    #print ang
    for i in range(12):
        s = SIGNS[i]
        s_ang[s] =  ang
        ang+=30
        if ang >= 360:
            ang= ang - 360
    return s_ang

def date_to_jd(y,m,d,greg=True): # year,month,day: day with decimal of day
    # default greg is True, for gregorian calendar
    if m==1 or m==2:
        y=y-1
        m=m+12
    A= int(y/100.0)
    B=2-A +int(A/4.0)
    if not greg:
        B=0
    jd = int(365.25 * (y + 4716)) + int(30.6001 * (m+1)) + d + B - 1524.5
    return jd

def gst_to_lst(gst, lon, drx):  # drx='W' or 'E'
    lon = lon / 15.0   # convert to hr
    if drx=='W':
        lst = gst -lon
    else:
        lst = gst + lon
    if lst > 24:
        lst -=24
    if lst <0:
        lst +=24
    return lst

def hms_to_decday(h,m,s):
    d = (h + m /60.0 + s /3600.0)/24.0
    return d

def hms_to_hr(h,m,s):
    hr = h + m/60.0 + s/(60.0*60.0)
    return hr


def hmsCIVIL_to_hmsGMT(h,m,s,zone,daylight=False):
    if daylight:
        h-=1
    hr = hms_to_hr(h,m,s)
    hr -= zone
    if hr > 24:
        hr-=24
    if hr <0:
        hr+=24
    return hr_to_hms(hr)

def hr_to_hms(hr):
    h = int(hr)
    m1 = (hr % 1) * 60
    m = int(m1)
    s = (m1 % 1) * 60
    return h,m,s

def jd_to_ymdhms(jd):
    di = jd+0.5
    I,F = divmod(di, 1)
    I=int(I)
    if I > 2299160:
        A = int((I-1867216.25)/36524.25)
        B = I+1+A-int(A/4.0)
    else:
        A=I
    C=B+1524
    D=int((C-122.1)/365.25)
    E=int(365.25 * D)
    G=int((C-E)/30.6001)
    d = C-E+F-int(30.6001 * G)
    if G < 13.5:
        m=G-1
    else:
        m=G-13
    if m > 2.5:
        y=D-4716
    else:
        y=D-4715
    d,dds=divmod(d,1)
    d=int(d)
    hrs=dds * 24
    hh,mm,ss=hr_to_hms(hrs)
    return y,m,d,hh,mm,ss

def ymd_to_jd(y,m,d,greg=True): # year,month,day: day with decimal of day
    # default greg is True, for gregorian calendar
    if m==1 or m==2:
        y=y-1
        m=m+12
    A= int(y/100.0)
    B=2-A +int(A/4.0)
    if not greg:
        B=0
    jd = int(365.25 * (y + 4716)) + int(30.6001 * (m+1)) + d + B - 1524.5
    return jd

def ymdhmsGMT_to_gst(yr,m,md,hh,mm,ss):
    A=0.0657098
    C=1.002738
    D=0.997270
    B= cal_B(yr)
    jd1 = ymd_to_jd(yr,m,md)
    jd0 =ymd_to_jd(yr,1,0.0)
    days = jd1 - jd0
    T0= days * A - B
    hr = hms_to_hr(hh,mm,ss)
    gst = hr * C + T0
    if gst > 24:
        gst -=24
    if gst<0:
        gst+=24
    return gst


if __name__=='__main__':
    yy,mn,dd,hh,mm,ss,zone = 2019,8,31,16,53,38,8
    asc,lst = cal_asc(yy,mn,dd,hh,mm,ss,zone,22.15, 114.15,'E')
    print('asc: %s lst:%s############' % (asc,lst))
    skip='''
    jd=2446113.75
    y,m,d,hh,mm,ss = jd_to_ymdhms(jd)
    print('jd_to_ymdhms: %s %s %s %02d:%02d:%02d' % (y,m,d,hh,mm,ss))

    yr,mon,mday,hr,minu,sec=2019,10,20,16,50,0
    jds = ymd_to_jd(yr,mon,mday)+hms_to_decday(hr,minu,sec)- zone/24.0
    print('jds:%s %s-%s-%s %02d:%02d:%02d' % (jds,yr,mon,mday,hr,minu,sec))
    yr1,mon1,mday1,hr1,minu1,sec1=jd_to_ymdhms(jds)
    print('jd_to_ymdhms %s-%s-%s %02d:%02d:%02d' % (yr1,mon1,mday1,hr1,minu1,sec1))
    '''
    sign_angles=cal_sign_angles(asc)
    ari_ang = sign_angles['ari']
    print("ari: %s" % ari_ang)
    mc = cal_mc(lst, ari_ang)
    print('mc:%s' % mc)
    
