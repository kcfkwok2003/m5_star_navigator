from math_util import *
import sys
version=1.02

if sys.platform=='esp32':
    import ubinascii,hashlib,machine
    def verify_key(passkey):
        N1,N2,N3,N4,N5 = [3,5,2,7,3]   # secrets
        uid = ubinascii.hexlify(machine.unique_id()).upper()
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
    try:
        f=open('passkey')
        passkey=f.read()
        f.close()
        if not verify_key(passkey):
            raise Exception('No passkey!')
    except Exception as e:
        sys.print_exception(e)
        sys.exit(1)
        raise Exception('No passkey!')
    
def cal_asc(lst, lat, eps):
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

def days_since_2000_jan_0(yr,mon,mday):
    d = 367 * yr - 7 * (yr + (mon +9) / 12) /4 + 275 * mon/9 + mday - 730530
    return d

def ecl_to_equ(lamda, beta,  e): #eclon, eclat, epsilon
    # lamda & beta in decimal degree
    sin_delta = sin_deg(beta) * cos_deg(e) + cos_deg(beta) * sin_deg(e) * sin_deg(lamda)
    dec = asin_deg(sin_delta)
    y = sin_deg(lamda) *cos_deg(e) - tan_deg(beta) * sin_deg(e)
    x = cos_deg(lamda)
    ra =atan2_deg(y, x)
    return ra, dec


def equ_to_ecl(d, alpha,delta):  # julian_day, Ra, dec
    e = cal_eps(d)
    y =sin_deg(alpha)* cos_deg(e) + tan_deg(delta) * sin_deg(e)
    x =cos_deg(alpha)
    lamda = atan_deg(y/x)
    if x< 0:
        lamda = 180 + lamda
    else:
        if y<0:
            lamda = 360+lamda

    beta = asin_deg(sin_deg(delta) * cos_deg(e) - cos_deg(delta) * sin_deg(e) * sin_deg(alpha))
    return lamda, beta

def hor_to_equ(alt, azi,lat,lst):  # altitude, azimuth, latitude,local sidereal time
    sin_A= sin_deg(azi)
    dec = asin_deg(sin_deg(alt) * sin_deg(lat) + cos_deg(alt) * cos_deg(lat) * cos_deg(azi))
    cos_H =(sin_deg(alt) - sin_deg(lat)* sin_deg(dec))/(cos_deg(lat) * cos_deg(dec))
    #print('cos_H:',cos_H)
    H = acos_deg(cos_H)
    if sin_A >=0:
        H=360-H
    H = H / 15.0  # convert to hour
    ra = lst - H
    if ra <0:
        ra+=24
    ra = ra * 15  # back to deg
    return ra, dec

