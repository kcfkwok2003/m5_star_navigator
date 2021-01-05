from machine import Pin, PWM
import time
import array
FREQS=array.array('H',[261,293,329,349,392,440,494,523])
p25 = PWM(Pin(25))
p25.duty(0)
while 1:
    for fx in FREQS:
        p25.duty(1)    
	p25.freq(fx)
        time.sleep(1)
        p25.duty(0)
        time.sleep(0.1)
    time.sleep(2)
