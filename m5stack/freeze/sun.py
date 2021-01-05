from planet_util import *

class Sun:
    def __init__(self):
        skip='''
        self.xs
        self.ys
        self.ecl
        self.M
        self.L
        self.r
        self.lon
        self.RA
        '''
        pass
    
    def cal(self, d):
        N =0.0
        i= 0.0
        a=1
        w = 282.9404 + 4.70935e-5 * d
        e = 0.016709 - 1.151e-9 * d
        self.M = rev(356.0470 + 0.9856002585 * d)
        self.ecl = 23.4393 - 3.563e-7 * d

        E = self.M + e*(180.0/pi) * sin_deg(self.M) * (1.0 + e * cos_deg(self.M))  # E,M in degree
        self.L = rev(w +self.M) # mean longitude
        x = cos_deg(E) - e
        y = sin_deg(E) * sqrt(1 - e*e)

        self.r = sqrt(x*x + y*y)
        v = atan2_deg(y,x)
        self.lon = rev(v + w)
        self.xs = self.r * cos_deg(self.lon)
        self.ys = self.r * sin_deg(self.lon)
        zs = 0.0;
        xe = self.xs;
        #ye = ys * cos_deg(ecl) - zs * sin_deg(ecl);
        ye = self.ys * cos_deg(self.ecl);
        #ze = self.ys * sin_deg(self.ecl) - zs * cos_deg(self.ecl);
        ze = self.ys * sin_deg(self.ecl) 
        #//RA = rev(atan2_deg(ye,xe)) ;
        self.RA = rev(atan2_deg(ye,self.xs)) ;
        self.Dec = atan2_deg(ze, sqrt(xe*xe + ye*ye));
        self.eclon =self.lon
        
    
if __name__=='__main__':
    import time
    tm= time.localtime()
    yx = tm.tm_year
    mx = tm.tm_mon
    dx = tm.tm_mday
    yx= 1958
    mx=2
    dx=18
    d = 367 * yx - 7 * (yx + (mx +9) / 12) /4 + 275 * mx/9 + dx - 730530
    print('d:',d)
    sun=Sun()
    sun.cal(d)
    print('RA:',sun.RA)
    print('Dec:',sun.Dec)
    
