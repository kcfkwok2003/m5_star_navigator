# -*- coding: utf-8 -*-
# lunar.py
# 2015/02/27 罗兵
# some modified refer to:https://zhuanlan.zhihu.com/p/80214800
# modified by kcf to port into micropython
import time
import horo_util as hu

version='1.0m'

class Ctime:
    def __init__(self,tm):
        self.tm=tm
        self._update()

    def __str__(self):
        return '%d-%d-%d %02d:%02d:%02d' % (self.year,self.month,self.day,self.hour,self.minute,self.second)
    
    def _update(self):
        tt = time.localtime(self.tm)
        self.year=tt[0]
        self.month=tt[1]
        self.day=tt[2]
        self.hour = tt[3]
        self.minute=tt[4]
        self.second=tt[5]                                   
        
    def add_days(self,i):
        return self.tm + (i*24*60*60) 
    
class Lunar(object):
    #******************************************************************************
    # 下面为阴历计算所需的数据,为节省存储空间,所以采用下面比较变态的存储方法.
    #******************************************************************************
    #数组g_lunar_month_day存入阴历2000年到2050年每年中的月天数信息，
    #阴历每月只能是29或30天，一年用12（或13）个二进制位表示，对应位为1表30天，否则为29天
    g_lunar_month_day = [
        0xc960, #2000
        0xd4a8, 0xd4a0, 0xda50, 0x5aa8, 0x56a0, 0xaad8, 0x25d0, 0x92d0, 0xc958, 0xa950,   #2010
        0xb4a0, 0xb550, 0xb550, 0x55a8, 0x4ba0, 0xa5b0, 0x52b8, 0x52b0, 0xa930, 0x74a8,   #2020
        0x6aa0, 0xad50, 0x4da8, 0x4b60, 0x9570, 0xa4e0, 0xd260, 0xe930, 0xd530, 0x5aa0,   #2030
        0x6b50, 0x96d0, 0x4ae8, 0x4ad0, 0xa4d0, 0xd258, 0xd250, 0xd520, 0xdaa0, 0xb5a0,   #2040
        0x56d0, 0x4ad8, 0x49b0, 0xa4b8, 0xa4b0, 0xaa50, 0xb528, 0x6d20, 0xada0, 0x55b0,   #2050
    ]

    #数组gLanarMonth存放阴历1999年到2050年闰月的月份，如没有则为0，每字节存两年
    g_lunar_month = [
        0x04,   #2001
        0x00, 0x20, 0x70, 0x05, 0x00,   #2011
        #0x40, 0x02, 0x07, 0x00, 0x50,   #2010
        0x40, 0x90, 0x06, 0x00, 0x40,   #2021
        #0x04, 0x09, 0x00, 0x60, 0x04,   #2020
        0x02, 0x06, 0x00, 0x50, 0x03,   #2031
        #0x00, 0x20, 0x60, 0x05, 0x00,   #2030
        0x0b, 0x00, 0x60, 0x05, 0x00,   #2041
        #0x30, 0xb0, 0x06, 0x00, 0x50,   #2040
        0x20, 0x70, 0x05, 0x00, 0x30    #2051 note: not sure 2051 is correct?   
        #0x02, 0x07, 0x00, 0x50, 0x03    #2050
    ]

    START_YEAR = 2000
    
    # 天干
    gan = '甲乙丙丁戊己庚辛壬癸'
    # 地支
    zhi = '子丑寅卯辰巳午未申酉戌亥'
    # 生肖
    xiao = '鼠牛虎兔龙蛇马羊猴鸡狗猪'
    # 月份
    lm = '正二三四五六七八九十冬腊'
    ke_v ='正一二三四五六七'
    # 日份
    ld = '初一初二初三初四初五初六初七初八初九初十十一十二十三十四十五十六十七十八十九二十廿一廿二廿三廿四廿五廿六廿七廿八廿九三十'
    # 节气
    jie = '小寒大寒立春雨水惊蛰春分清明谷雨立夏小满芒种夏至小暑大暑立秋处暑白露秋分寒露霜降立冬小雪大雪冬至'
    jie_qi_odd = "立春惊蛰清明立夏芒种小暑立秋白露寒露立冬大雪小寒"  # 节气节点，如立春-惊蛰是正月，两个节气一个月
    # 节气对应农历干支月
    jie_qi_month = {
        "立春": [0, "寅"],
	"惊蛰": [1, "卯"],
        "清明": [2, "辰"],
        "立夏": [3, "巳"],
        "芒种": [4, "午"],
        "小暑": [5, "未"],
        "立秋": [6, "申"],
        "白露": [7, "酉"],
        "寒露": [8, "戌"],
        "立冬": [9, "亥"],
        "大雪": [10, "子"],
        "小寒": [11, "丑"],
    }

    def __init__(self, dt = None):
        '''初始化：参数为datetime.datetime类实例，默认当前时间'''
        self.localtime = dt  #if dt else datetime.datetime.today()
        self.gz_year_value = ""
        #self.ln_month_value = ""
        #self.wu_xing = ""

    def localtime_date(self):
        return time.localtime(self.localtime)

        
    def sx_year(self): # 返回生肖年
        ct = self.localtime #取当前时间
        
        year = self.ln_year() - 3 - 1 # 农历年份减3 （说明：补减1）
        year = year % 12 # 模12，得到地支数
        return self.xiao[year]

    def gz_year(self): # 返回干支纪年
        ct = self.localtime #取当前时间
        year = self.ln_year() - 3 - 1 # 农历年份减3 （说明：补减1）
        G = year % 10 # 模10，得到天干数
        Z = year % 12 # 模12，得到地支数
        self.gz_year_value = self.gan[G] + self.zhi[Z]
        return self.gz_year_value

    def gz_month(self):  # 返回干支纪月（原作者未实现）
        """
       干支纪月的计算规则较为复杂，是本人在前人的基础上实现的，填补了空白。
        1、首先判断当前日期所处的节气范围，
        2、特别要考虑年数是否需要增减，以立春为界，如正月尚未立春的日子年数减一，
        3、月的天干公式 （年干序号 * 2 + 月数） % 10 ，其中 0 表示最后一个天干，
        4、月的地支是固定的，查表可得。
        :return:
        """
        ct = Ctime(self.localtime)  # 取当前时间
        jie_qi = self.ln_jie()
        nl_month_val = self.ln_month()
        if len(jie_qi) > 0 and jie_qi in self.jie_qi_odd:   # 如果恰好是节气当日
            if self.jie_qi_month[jie_qi][0] == 0 and nl_month_val == 12:  #
                year = self.ln_year() - 3  # 虽然农历已经是腊月，但是已经立春， 所以年加一
                G = year % 10  # 模10，得到天干数
                Z = year % 12  # 模12，得到地支数
                nl_year = self.gan[G] + self.zhi[Z]
                nl_month = 0
            else:
                nl_year = self.gz_year_value  # 干支纪年
                nl_month = self.jie_qi_month[jie_qi][0]  # 计算出干支纪月
        else:      # 如果不是节气日，则循环判断后一个分月节气是什么
            nl_year = self.gz_year_value
            nl_month = 0
            for i in range(-1, -40, -1):
                var_days = Ctime( ct.add_days(i)) #ct + datetime.timedelta(days=i)
                #print('ct: %s i:%s' % (ct,i))
                #print('delta:%s' % datetime.timedelta(days=i))
                #print('var_days:%s' % var_days)
                
                jie_qi = self.nl_jie(var_days)
                #print('var_days:%s jie_qi:%s' % (var_days,jie_qi))
                if len(jie_qi) > 0 and jie_qi in self.jie_qi_odd:
                    if self.jie_qi_month[jie_qi][0] > 0:
                        nl_month = self.jie_qi_month[jie_qi][0]
                    elif self.jie_qi_month[jie_qi][0] == 0 and nl_month_val == 12:   #
                        year = self.ln_year() - 3    # 虽然农历已经是腊月，但是已经立春， 所以年加一
                        G = year % 10  # 模10，得到天干数
                        Z = year % 12  # 模12，得到地支数
                        nl_year = self.gan[G] + self.zhi[Z]
                        nl_month = 0
                    else:
                        nl_month = 0
                    break
        gan_str = self.gan
        # print(nl_year[0])
        month_num = (gan_str.find(nl_year[0])+1) * 2 + nl_month + 1
        M = month_num % 10
        if M == 0:
            M = 10
        a =self.gan[M-1]
        #print('jie_qi:%s' % jie_qi)
        #print('jie_qi_month:%s' % self.jie_qi_month)
        b =self.jie_qi_month[jie_qi][1]
        gz_month = a+b
        return gz_month


    def gz_day(self): # 返回干支纪日
        ct = Ctime(self.localtime) #取当前时间
        C = ct.year // 100 #取世纪数，减一
        y = ct.year % 100 #取年份后两位（若为1月、2月则当前年份减一）
        y = y - 1 if ct.month == 1 or ct.month == 2 else y
        M = ct.month #取月份（若为1月、2月则分别按13、14来计算）
        M = M + 12 if ct.month == 1 or ct.month == 2 else M
        d = ct.day #取日数
        i = 0 if ct.month % 2 == 1 else 6 #取i （奇数月i=0，偶数月i=6）
        
        #下面两个是网上的公式
        # http://baike.baidu.com/link?url=MbTKmhrTHTOAz735gi37tEtwd29zqE9GJ92cZQZd0X8uFO5XgmyMKQru6aetzcGadqekzKd3nZHVS99rewya6q
        # 计算干（说明：补减1）
        G = 4 * C + C // 4 + 5 * y + y // 4 + 3 * (M + 1) // 5 + d - 3 - 1
        G = G % 10
        # 计算支（说明：补减1）
        Z = 8 * C + C // 4 + 5 * y + y // 4 + 3 * (M + 1) // 5 + d + 7 + i - 1
        Z = Z % 12

        #返回 干支纪日
        return self.gan[G] + self.zhi[Z]

    def gz_hour(self): # 返回干支纪时（时辰）
        """
        原作者计算的时干支，实际上只返回了时辰的地支，缺少天干；
        我补充了天干的计算，公式皆为原创
        时干数 = ((日干 % 5)*2 + 时辰 -2) % 10
        :return:
        """
        ct = Ctime(self.localtime)  # 取当前时间
        # 计算支
        hour=ct.hour
        minute=ct.minute
        Z = round((hour / 2) + 0.1) % 12  # 之所以加0.1是因为round的bug!!
        #print('Z:%s h:%s m:%s' % (Z,hour,minute))
        ke = minute // 15
        if (hour % 2)==1:
            ke+=4
        kev =self.ke_v[ke] + '刻'
        #print('ke:%s' % ke)
        gz_day_value = self.gz_day()
        gz_day_num = self.gan.find(gz_day_value[0]) + 1
        gz_day_yu = gz_day_num % 5
        hour_num = Z + 1
        if gz_day_yu == 0:
            gz_day_yu = 5
        gz_hour_num = (gz_day_yu * 2 - 1 + hour_num-1) % 10
        if gz_hour_num == 0:
            gz_hour_num = 10
        # 返回 干支纪时（时辰）
        return self.gan[gz_hour_num-1] + self.zhi[Z], ke, kev
   
    def ln_year(self): # 返回农历年
        year, _, _ = self.ln_date()
        return year

    def ln_month(self): # 返回农历月
        _, month, _ = self.ln_date()
        return month

    def ln_day(self): # 返回农历日
        _, _, day = self.ln_date()
        return day

    def ln_date(self): # 返回农历日期整数元组（年、月、日）（查表法）
        delta_days = self._date_diff() 
        #print('delta_days',delta_days)
        
        #阳历1901年2月19日为阴历1901年正月初一
        #阳历1901年1月1日到2月19日共有49天
        # 2000-2-5 为阴历2000年正月初一
        #阳历2000年1月1日到2月5日共有35天
        if (delta_days < 35):
            year = self.START_YEAR - 1
            if (delta_days <5):
              month = 11; 
              day = 11 + delta_days
            else:
                month = 12;
                day = delta_days - 4
            return (year, month, day)

        #下面从阴历2000年正月初一算起
        delta_days -= 35
        year, month, day = self.START_YEAR, 1, 1
        #计算年
        tmp = self._lunar_year_days(year)
        while delta_days >= tmp:
            delta_days -= tmp
            year += 1
            tmp = self._lunar_year_days(year)

        #计算月
        (foo, tmp) = self._lunar_month_days(year, month)
        while delta_days >= tmp:
            delta_days -= tmp
            if (month == self._get_leap_month(year)):
                (tmp, foo) = self._lunar_month_days(year, month)
                if (delta_days < tmp):
                    return (0, 0, 0)
                delta_days -= tmp
            month += 1
            (foo, tmp) = self._lunar_month_days(year, month)

        #计算日
        day += delta_days
        return (year, month, day)
    
    def ln_date_str(self):# 返回农历日期字符串，形如：农历正月初九
        _, month, day = self.ln_date()
        return '农历{}月{}'.format(self.lm[month-1], self.ld[(day-1)*2:day*2])
    
    def ln_jie(self): # 返回农历节气
        ct = Ctime(self.localtime) #取当前时间
        year = ct.year
        for i in range(24):
            #因为两个都是浮点数，不能用相等表示
            delta = self._julian_day() - self._julian_day_of_ln_jie(year, i)
            #print('delta:',delta)
            if -.5 <= delta <= .5:
                return self.jie[i*2:(i+1)*2]
        return ''

    def nl_jie(self,dt):
        year = dt.year
        for i in range(24):
            # 因为两个都是浮点数，不能用相等表示
            rd = self.rulian_day(dt)
            jd = self._julian_day_of_ln_jie(year,i)
            delta = self.rulian_day(dt) - self._julian_day_of_ln_jie(year, i)
            #print('i:%s yr:%s, rulian:%s jd:%s delta:%s' % (i,year,rd,jd,delta))
            if -.5 <= delta <= .5:
                return self.jie[i * 2:(i + 1) * 2]
        return ''

    def ln_jie_2(self):
        ct = Ctime(self.localtime)
        yc=y = ct.year
        m = ct.month
        d = ct.day
        d2 = hu.ymd_to_jd(y,m,d)
        #print('*** ymd: %s-%s-%s' % (y,m,d))
        if m==1 and d<25:
            yc=y-1
            i=23
        else:
            i=0
        jd1 = self._julian_day_of_ln_jie(yc,i)
        datec1 = hu.jd_to_ymdhms(jd1)
        d1 = hu.ymd_to_jd(datec1[0],datec1[1],datec1[2])            
        while True:
            if i+1 >23:
                jd3=self._julian_day_of_ln_jie(yc+1,0)
            else:
                jd3=self._julian_day_of_ln_jie(yc,i+1)
            datec3 = hu.jd_to_ymdhms(jd3)
            d3 = hu.ymd_to_jd(datec3[0],datec3[1],datec3[2])            
            if d1==d2:
                jie1 =self.jie[i*2:(i+1)*2]
                return jie1,0
            if d1 < d2 and d2 < d3:
                td =int(d2 - d1)
                jie1 =self.jie[i*2:(i+1)*2]
                return jie1, td
            i+=1
            if i>23:
                yc+=1
                i=0
            d1 = d3

        
    #显示日历
    def calendar(self):
        pass

    #######################################################
    #            下面皆为私有函数
    #######################################################
    
    def _date_diff(self):
        '''返回基于2000/01/01日差数'''
        
        days = (self.localtime - time.mktime((2000,1,1,0,0,0,0,0,0))) // (24*60*60)
        return int(days)  # (self.localtime - datetime.datetime(1901, 1, 1)).days

    def _get_leap_month(self, lunar_year):
        flag = self.g_lunar_month[(lunar_year - self.START_YEAR) // 2]
        if (lunar_year - self.START_YEAR) % 2:
            return flag & 0x0f
        else:
            return flag >> 4

    def _lunar_month_days(self, lunar_year, lunar_month):
        #print('lunar_year:',lunar_year)
        #print('start_year:',self.START_YEAR)
        #print('diff:', (lunar_year-self.START_YEAR))
        
        if (lunar_year < self.START_YEAR):
            return 30

        high, low = 0, 29
        iBit = 16 - lunar_month;

        if (lunar_month > self._get_leap_month(lunar_year) and self._get_leap_month(lunar_year)):
            iBit -= 1

        if (self.g_lunar_month_day[lunar_year - self.START_YEAR] & (1 << iBit)):
            low += 1
           
        if (lunar_month == self._get_leap_month(lunar_year)):
            if (self.g_lunar_month_day[lunar_year - self.START_YEAR] & (1 << (iBit -1))):
                 high = 30
            else:
                 high = 29

        return (high, low)

    def _lunar_year_days(self, year):
        days = 0
        for i in range(1, 13):
            (high, low) = self._lunar_month_days(year, i)
            days += high
            days += low
        return days
    
    # 返回指定公历日期的儒略日（http://blog.csdn.net/orbit/article/details/9210413）
    def _julian_day(self):
        ct = Ctime( self.localtime) #取当前时间
        year = ct.year
        month = ct.month
        day = ct.day

        if month <= 2:
            month += 12
            year -= 1

        B = year / 100
        B = 2 - B + year / 400

        dd = day + 0.5000115740 #本日12:00后才是儒略日的开始(过一秒钟)*/
        return int(365.25 * (year + 4716) + 0.01) + int(30.60001 * (month + 1)) + dd + B - 1524.5    

    def rulian_day(self, dt):   # 重写_julian_day 函数，变成可以传参的函数
        year = dt.year
        month = dt.month
        day = dt.day
        if month <= 2:
            month += 12
            year -= 1

        B = year / 100
        B = 2 - B + year / 400

        dd = day + 0.5000115740  # 本日12:00后才是儒略日的开始(过一秒钟)*/
        return int(365.25 * (year + 4716) + 0.01) + int(30.60001 * (month + 1)) + dd + B - 1524.5
    
    # 返回指定年份的节气的儒略日数（http://blog.csdn.net/orbit/article/details/9210413）
    def _julian_day_of_ln_jie(self, year, st):
        s_stAccInfo =[
             0.00, 1272494.40, 2548020.60, 3830143.80, 5120226.60, 6420865.80,
             7732018.80, 9055272.60, 10388958.00, 11733065.40, 13084292.40, 14441592.00,
             15800560.80, 17159347.20, 18513766.20, 19862002.20, 21201005.40, 22529659.80,
             23846845.20, 25152606.00, 26447687.40, 27733451.40, 29011921.20, 30285477.60]

        #已知1900年小寒时刻为1月6日02:05:00
        base1900_SlightColdJD = 2415025.5868055555
        
        if (st < 0) or (st > 24):
            return 0.0
     
        stJd = 365.24219878 * (year - 1900) + s_stAccInfo[st] / 86400.0
     
        return base1900_SlightColdJD + stJd


        
        
# 测试
def test(ct=None):
    ln = Lunar(ct)    
    print('公历 {} '.format(ln.localtime_date()))
    print('{} 【{}】 {}年 {}日 {}时'.format(ln.ln_date_str(), ln.gz_year(), ln.sx_year(), ln.gz_day(), ln.gz_hour()))
    print('节气：{}'.format(ln.ln_jie()))
    print('节气2：{}'.format(ln.ln_jie_2()))
    print('gz_year:%s' % ln.gz_year())
    print('sx_year:%s' % ln.sx_year())
    yr,mon,day= ln.ln_date()
    print('%s - %s - %s' % (yr,mon,day))
    print('%s月' % ln.gz_month())
    print('%s月 %s' % (ln.lm[mon-1], ln.ld[(day-1)*2:day*2]))
    #print('%s日 %s时' % (ln.gz_day(), ln.gz_hour()))
    #print('ln_date_str:%s' % ln.ln_date_str())
    for hr in range(2):
        for minute in range(60):
            ct = time.mktime((2019,10,24,hr,minute,0,0,0,0))
            ln = Lunar(ct)
            ln.gz_hour()

def test_jie(tx=None,ct=None):
    ln = Lunar(ct)
    #ln.ln_jie_2x()
    print('%s %s' % (str(tx),str(ln.ln_jie_2())))
        
if __name__ == '__main__':
    #ct = time.mktime((2020,1,1,0,13,15,0,0,0))
    #ct = time.mktime((2019,12,31,0,13,15,0,0,0))
    for m,d in [(1,1),(1,5),(1,6),(1,7),(1,19),(1,20),(1,21),(2,3),(2,4),(2,5),(2,18),(2,19),(2,20),(3,4),(3,5),(3,6),(3,19),(3,20),(3,21),(3,22),(4,3),(4,4),(4,5),(4,18),(4,19),(4,20),(5,4),(5,5),(5,6),(5,19),(5,20),(5,21),(6,4),(6,5),(6,6),(6,20),(6,21),(6,22),(7,5),(7,6),(7,7),(11,21),(11,22),(11,23),(12,5),(12,6),(12,7),(12,8),(12,20),(12,21),(12,22),(4,21)]:
        tx =(2020,m,d,0,0,0,0,0,0)
        ct =time.mktime(tx)
        test_jie(tx,ct)
    for m,d in [(1,1),(1,4),(1,5),(1,6),(1,19),(1,20),(1,21)]:
        tx =(2021,m,d,0,0,0,0,0,0)
        ct =time.mktime(tx)
        test_jie(tx,ct)
        
