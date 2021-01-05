from m5stack import TFT
import random as r
import time as t
tft=TFT()
tft.start_spi()
r.seed(10)
for i in range(100):
    for j in range(100):
        x=r.randint(1,319)
        y=r.randint(1,239)
        z=r.randint(0x00,0xffff)
        tft.pixel(x,y,z)
        t.sleep(0.01)
