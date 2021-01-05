from planet_util import *
planet_names=['Sun','Moon','Mercury','Venus','Mars','Jupiter','Saturn','Uranus','Neptune','Pluto']

class Planet:
    def __init__(self):
        self.RA=None
        self.N=None
        self.i=None
        self.w=None
        self.a=None
        self.e=None
        self.M=None

    def pcal(self, d, sun):
        E = self.cal_E(self.M,self.e)
        x = self.a * (cos_deg(E) - self.e)
        y = self.a * sqrt(1 - self.e * self.e) * sin_deg(E)
        r = sqrt( x*x + y*y)
        v = rev(atan2_deg(y,x))

        # heliocentric eclipic rectangular coord:
        xh = r*(cos_deg(self.N) * cos_deg(v +self.w) - sin_deg(self.N) * sin_deg(v + self.w) * cos_deg(self.i))
        yh = r*(sin_deg(self.N) * cos_deg(v + self.w) + cos_deg(self.N) * sin_deg(v + self.w) * cos_deg(self.i))
        zh = r * sin_deg(v + self.w) * sin_deg(self.i)

        # convert to spherical coord
        lon = rev(atan2_deg(yh, xh))
        lat = atan2_deg(zh, sqrt(xh*xh + yh*yh))

        xg = xh + sun.xs
        yg = yh + sun.ys
        zg = zh

        xe = xg
        ye = yg * cos_deg(sun.ecl) - zg * sin_deg(sun.ecl)
        ze = yg * sin_deg(sun.ecl) + zg * cos_deg(sun.ecl)

        self.RA = rev(atan2_deg(ye,xe))
        self.Dec = atan2_deg(ze, sqrt(xe*xe + ye*ye))

        lx, bx = equ_to_ecl(d, self.RA,self.Dec)
        self.eclon= lx
        self.eclat= bx

        
    def cal_E(self, M,e):
        E0 = M + (180.0/pi) * e * sin_deg(M) * (1.0 + e * cos_deg(M))
        E=None
        while 1:
            E1 = E0- (E0 - (180.0/pi) * e * sin_deg(E0) - M) / (1-e * cos_deg(E0))
            if (E1 - E0) < 0.005:
                E = E1
                break
            E0 = E1
                
        return E

                
class Mercury(Planet):
    def cal(self, d, sun):
        self.name='Mercury'
        self.N = rev(48.3313 + 3.24587e-5 * d)
        self.i = rev(7.0047 + 5.00e-8 * d)
        self.w = rev(29.1241 + 1.01444e-5 * d)
        self.a= 0.387098
        self.e = 0.205635 + 5.59e-10 * d
        self.M = rev(168.6562 + 4.0923344368 * d)
        self.pcal(d, sun)

class Venus(Planet):
    def cal(self,d,sun):
        self.name ='Venus'
        self.N = rev(76.6799 +2.46590E-5 *d);
        self.i = rev(3.3946 +2.7E-8  * d);
        self.w = rev(54.8910 +1.38374E-5  *d);
        self.a=0.723330;
        self.e =0.006773  + -1.302E-9 * d;
        self.M = rev(48.0052 +1.6021302244  * d);
        self.pcal(d,sun);
        
class Mars(Planet):
    def cal(self,d,sun):
        self.name='Mars'
        self.N = rev(49.5574 +2.11081E-5 *d);
        self.i = rev(1.8497 + -1.78E-8 * d);
        self.w = rev(286.5016 + 2.92961E-5 *d);
        self.a=1.523688;
        self.e =0.093405  + 2.516E-9 * d;
        self.M = rev(18.6021 +0.5240207766  * d);
        self.pcal(d,sun);

class Jupiter(Planet):
    def cal(self,d,sun):
        self.name='Jupiter'
        self.N = rev(100.4542 +2.76854E-5 *d);
        self.i = rev(1.3030 +-1.557E-7  * d);
        self.w = rev(273.8777 +1.64505E-5  *d);
        self.a=5.20256;
        self.e =0.048498  + 4.469E-9 * d;
        self.M = rev(19.8950 + 0.0830853001 * d);
        self.pcal(d,sun);
        
class Saturn(Planet):
    def cal(self,d,sun):
        self.name='Saturn'
        self.N = rev(113.6634 +2.38980E-5 *d);
        self.i = rev(2.4886 + - 1.081E-7 * d);
        self.w = rev(339.3939 + 2.97661E-5 *d);
        self.a=9.55475;
        self.e = 0.055546 + - 9.499E-9 * d;
        self.M = rev(316.9670 + 0.0334442282 * d);
        self.pcal(d,sun);
        
class Uranus(Planet):
    def cal(self,d,sun):
        self.name='Uranus'
        self.N = rev(74.0005 + 1.3978E-5 *d);
        self.i = rev(0.7733 + 1.9E-8 * d);
        self.w = rev(96.6612 + 3.0565E-5 *d);
        self.a = 19.18171 + - 1.55E-8  *d;
        self.e = 0.047318  + 7.45E-9  * d;
        self.M = rev(142.5905 + 0.011725806  * d);
        self.pcal(d,sun);
        
class Neptune(Planet):
    def cal(self,d,sun):
        self.name='Neptune'
        self.N = rev(131.7806 + 3.0173E-5 *d);
        self.i = rev(1.7700 + - 2.55E-7 * d);
        self.w = rev(272.8461 + - 6.027E-6 *d);
        self.a = 30.05826 + 3.313E-8   *d;
        self.e = 0.008606   + 2.15E-9  * d;
        self.M = rev(260.2471 + 0.005995147  * d);
        self.pcal(d,sun);

class Pluto:
    def cal(self,d,sun):
        self.name='Pluto'
        S = 50.03 + 0.033459652 *d;
        P = 238.95 + 0.003968789 *d;
        lon = 238.9508 + 0.00400703 *d +                       \
            -19.799 *sin_deg(P) + 19.848 * cos_deg(P) +                 \
            +0.897 *sin_deg(2*P) -4.956 * cos_deg(2*P) +                \
            +0.610 *sin_deg(3*P) +1.211 * cos_deg(3*P)+                 \
            -0.341 *sin_deg(4*P) -0.190 * cos_deg(4*P) +                \
            +0.128 *sin_deg(5*P) -0.034 * cos_deg(5*P) +                \
            -0.038 * sin_deg(6*P) +0.031 *cos_deg(6*P) +                \
            +0.020 * sin_deg(S-P) -0.010 *cos_deg(S-P);
        lat= -3.9082 +                         \
            -5.453 *sin_deg(P) - 14.975*cos_deg(P) +            \
            +3.257 *sin_deg(2*P) + 1.673*cos_deg(2*P) +         \
            -1.051 *sin_deg(3*P) + 0.328*cos_deg(3*P) +         \
            +0.179 *sin_deg(4*P) - 0.292*cos_deg(4*P) +         \
            +0.019 *sin_deg(5*P) + 0.100*cos_deg(5*P) +         \
            -0.031 *sin_deg(6*P) - 0.026*cos_deg(6*P) +         \
            + 0.011*cos_deg(S-P);
        
        r= 40.72 +                                     \
            +6.68 *sin_deg(P) + 6.90 *cos_deg(P) +                      \
            -1.18 *sin_deg(2*P) - 0.03*cos_deg(2*P) +                   \
            +0.15 *sin_deg(3*P) - 0.14*cos_deg(3*P);
        #//convert the perturbed lon lat r to xh,yh,zh
        xh = r * cos_deg(lon) * cos_deg(lat);
        yh = r * sin_deg(lon) * cos_deg(lat);
        zh = r * sin_deg(lat);
        #//rs = sun_dict['r']
        #//rs=1
        #// lonsun = sun_dict['lon']
        #// xs = rs * cos_deg(lonsun)
        xs = cos_deg(sun.lon);
        #//  ys = rs * sin_deg(lonsun)
        ys = sin_deg(sun.lon);
        xg = xh + xs;
        yg = yh + ys;
        zg = zh;
        
        #//ecl = sun_dict['ecl']
        xe = xg;
        ye = yg * cos_deg(sun.ecl) - zg *sin_deg(sun.ecl);
        ze = yg * sin_deg(sun.ecl) + zg * cos_deg(sun.ecl);
        
        self.RA = rev(atan2_deg(ye,xe));
        self.Dec = atan2_deg(ze,sqrt(xe*xe + ye*ye))
        lx, bx = equ_to_ecl(d, self.RA,self.Dec)
        self.eclon= lx
        self.eclat= bx

        
if __name__=='__main__':
    import time
    from sun import Sun
    from moon import Moon
    tm= time.localtime()
    yx = tm.tm_year
    mx = tm.tm_mon
    dx = tm.tm_mday
    dxd = tm.tm_hour /24.0 + tm.tm_min / (24.0*60) + tm.tm_sec / (24.0*60*60)
    d = 367 * yx - 7 * (yx + (mx +9) / 12) /4 + 275 * mx/9 + dx - 730530 + dxd
    
    sun = Sun()
    sun.cal(d)
    print('Sun:')
    print('Ra:',sun.RA)
    print('Dec:',sun.Dec)    
    print('lon:',sun.lon)

    for pn in [Mercury(), Venus(), Mars(), Jupiter(), Saturn(), Uranus(), Neptune(), Pluto(), Moon()]:
        pn.cal(d,sun)
        print(pn.name)
        print('Ra:',pn.RA)
        print('Dec:',pn.Dec)
        print('eclon:',pn.eclon)
        print('eclat:',pn.eclat)
        print('')




