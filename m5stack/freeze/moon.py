from planet_util import *

class Moon:
    def cal(self,d,sun):
        self.name='Moon'
        N=rev(125.1228 - 0.0529538083 * d);
        i=rev(5.1454);
        w= rev(318.0634 + 0.1643573223 * d);
        a = 60.2666;  #// # Earth radii
        e= 0.054900;
        M=rev(115.3654 + 13.0649929509 * d);
        L= rev(M + N + w);
        D= rev(L-sun.L);
        F= rev(L-N);
        E0= M + (180.0/pi) * e * sin_deg(M) * (1.0 + e * cos_deg(M)); #//  # E,M in degree
        #E1;
        #E;
        while 1:
            E1= E0 - (E0 - (180.0/pi) * e * sin_deg(E0) -M) / (1 - e * cos_deg(E0));
            if ((E1 - E0) < 0.005):
                E=E1;
                break;                
            E0=E1;
                
        x = a * (cos_deg(E) - e);
        y = a * sqrt(1 - e*e) * sin_deg(E);
        r = sqrt( x*x + y*y);
        v= rev(atan2_deg(y,x));
        xh= r*(cos_deg(N) * cos_deg(v+w) - sin_deg(N) * sin_deg(v+w) * cos_deg\
                      (i));
        yh =r*(sin_deg(N) * cos_deg(v+w) + cos_deg(N) * sin_deg(v+w) * cos_deg\
                      (i));
        zh =r*sin_deg(v+w) * sin_deg(i);
        lonecl = rev(atan2_deg(yh,xh));
        latecl = atan2_deg(zh, sqrt(xh*xh + yh*yh));
        #  //# perturbations in longitude
        Evect =-1.274 * sin_deg(M - 2*D); #// # (Evection)
        Varia =0.658 * sin_deg(2 *D); #// # (Variation)
        Yearly =-0.186 * sin_deg(sun.M); #//  # (Yearly equation)
        Paral=-0.035 * sin_deg(D); #//  # (Parallactic equation)
        pert_lon= Evect +                      \
            Varia +                                     \
            Yearly +                                    \
            -0.059 * sin_deg(2 * M - 2*D)+                      \
            -0.057 * sin_deg(M - 2*D + sun.M)+                  \
            +0.053 * sin_deg(M + 2*D)+                  \
            +0.046 * sin_deg(2*D -sun.M)+                       \
            +0.041 * sin_deg(M -sun.M)+                 \
            Paral +                                     \
            -0.031 * sin_deg(M + sun.M)+                        \
            -0.015 * sin_deg(2*F - 2*D)+                        \
            +0.011 * sin_deg(M - 4*D);
        #//# perturbations in latitude
        pert_lat = -0.173 * sin_deg(F - 2*D) + \
            -0.055 * sin_deg(M -F -2*D) +                       \
            -0.046 * sin_deg(M +F -2*D) +                       \
            +0.033 * sin_deg(F + 2*D) +                 \
            +0.017 * sin_deg(2*M + F);
        #//# perturbations in lunar distance (Earth radii)
        pert_dist= -0.58 * cos_deg(M - 2*D) +  \
            -0.46 * cos_deg(2*D);
        self.lon =lon= lonecl + pert_lon;
        self.lat =lat= latecl + pert_lat;
        self.dist = dist = r + pert_dist;
        #//#convert the perturbed lon lat r to xh,yh,zh
        xh = dist * cos_deg(lon) * cos_deg(lat);
        yh = dist * sin_deg(lon) * cos_deg(lat);
        zh = dist * sin_deg(lat);
        xs =  cos_deg(sun.lon);
        ys =  sin_deg(sun.lon);
        xg = xh + xs;
        yg = yh + ys;
        zg = zh;
        xe = xg;
        ye = yg * cos_deg(sun.ecl) - zg *sin_deg(sun.ecl);
        ze = yg * sin_deg(sun.ecl) + zg * cos_deg(sun.ecl);
        self.RA = rev(atan2_deg(ye,xe));
        self.Dec = atan2_deg(ze,sqrt(xe*xe + ye*ye))
        lx, bx = equ_to_ecl(d, self.RA,self.Dec)
        self.eclon= lx
        self.eclat= bx
