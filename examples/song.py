#ref : https://gist.github.com/nicksort/4736535

from machine import Pin,PWM
from array import array
import time
c = 261
d = 294
e = 329
f = 349
g = 391
gS = 415
a = 440
aS = 466
b = 494
cH = 523
cSH = 554
dH = 587
dSH = 622
eH = 659
fH = 698
fSH = 740
gH = 784
gSH = 830
aH = 880
DUTY_ON=99
DUTY_OFF=0

class SONG:
  def __init__(self,pinx):
    global Pin,PWM
    self.speaker=PWM(Pin(pinx,Pin.OUT))
    self.speaker.duty(0)

  def set_notes(self, notes, durations):
      self.notes=notes
      self.durations=durations
      
  def play(self):
      global DUTY_ON,DUTY_OFF
      for i in range(len(self.notes)):
        self.speaker.freq(self.notes[i])
        self.speaker.duty(DUTY_ON)
        time.sleep_ms(self.durations[i])
        self.speaker.duty(DUTY_OFF)
        time.sleep(0.05)

if __name__=='__main__':
  NOTES1=[a,a,a,f,cH,a,f,cH,a]
  DURATIONS1=[500,500,500,350,150,500,350,150,650]
  song=SONG(25)
  song.set_notes(NOTES1,DURATIONS1)
  song.play()
  
