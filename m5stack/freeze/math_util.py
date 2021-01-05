from math import atan2, pi, sin, cos, floor,sqrt,tan,atan,asin,acos

def atan2_deg(y,x):
    return atan2(y,x) * 180.0/pi

def atan_deg(x):
    return atan(x) * 180.0/pi

def asin_deg(x):
    return asin(x) * 180.0/pi

def acos_deg(x):
    if x <-1.0:
        x=-1.0
    if x > 1.0:
        x=1.0
    return acos(x) * 180.0/pi

def sin_deg(x):
    return sin(x * pi/180.0)

def cos_deg(x):
    return cos(x * pi/180.0)

def tan_deg(x):
    return tan(x * pi/180.0)

def rev(x):
    if x >= 360.0 or x < 0.0:
        return x - floor(x / 360.0) * 360.0
    else:
        return x
    
