# ref:
# https://github.com/adafruit/micropython-adafruit-rgb-display
#
from machine import Pin,SPI
import utime
import ustruct
import framebuf
import os
VERSION='1.0'

convention=False

RST_PIN=33
DC_PIN=27
CS_PIN=14
SCK_PIN=18
MOSI_PIN=23
MISO_PIN=19
LED_PIN=32

SCR_WIDTH=320
SCR_HEIGHT=240

GPIO_LOW=0
GPIO_HIGH=1

BITMASK=[0x80,0x40,0x20,0x10,0x08,0x04,0x02,0x01]

from color import *

class TFT:
    _COLUMN_SET = 0x2a
    _PAGE_SET = 0x2b
    _RAM_WRITE = 0x2c
    _RAM_READ = 0x2e
    _ENCODE_PIXEL = ">H"
    _ENCODE_POS = ">HH"
    _DECODE_PIXEL = ">BBB"
    _INIT = (
        (0xef, b'\x03\x80\x02'),
        (0xcf, b'\x00\xc1\x30'),
        (0xed, b'\x64\x03\x12\x81'),
        (0xe8, b'\x85\x00\x78'),
        (0xcb, b'\x39\x2c\x00\x34\x02'),
        (0xf7, b'\x20'),
        (0xea, b'\x00\x00'),
        (0xc0, b'\x23'),  # Power Control 1, VRH[5:0]
        (0xc1, b'\x10'),  # Power Control 2, SAP[2:0], BT[3:0]
        (0xc5, b'\x3e\x28'),  # VCM Control 1
        (0xc7, b'\x86'),  # VCM Control 2
        (0x36, b'\x08'),  # old:x48 Memory Access Control  //kcf: change mx=0
        (0x3a, b'\x55'),  # Pixel Format
        (0xb1, b'\x00\x18'),  # FRMCTR1
        (0xb6, b'\x08\x82\x27'),  # Display Function Control
        (0xf2, b'\x00'),  # 3Gamma Function Disable
        (0x26, b'\x01'),  # Gamma Curve Selected
        (0xe0,  # Set Gamma
         b'\x0f\x31\x2b\x0c\x0e\x08\x4e\xf1\x37\x07\x10\x03\x0e\x09\x00'),
        (0xe1,  # Set Gamma
         b'\x00\x0e\x14\x03\x11\x07\x31\xc1\x48\x08\x0f\x0c\x31\x36\x0f'),
        (0x11, None),
        (0x29, None),
    )
    
    def __init__(self,sck=SCK_PIN,mosi=MOSI_PIN, miso=MISO_PIN,rst=RST_PIN,dc=DC_PIN,cs=CS_PIN, width=SCR_WIDTH, height=SCR_HEIGHT, led=LED_PIN):
        self.width=width
        self.height=height
        self.sck=Pin(sck)
        self.mosi=Pin(mosi)
        self.miso=Pin(miso)
        self.rst=Pin(rst)
        self.dc=Pin(dc)
        self.cs=Pin(cs)
        self.led=Pin(led)

    def start_spi(self,baud=32000000):
        self.spi=spi = SPI(baudrate=baud, polarity=1,phase=0,sck=self.sck,mosi=self.mosi,miso=self.miso)
        self.cs.init(self.cs.OUT, value=1)
        self.dc.init(self.dc.OUT, value=0)
        self.rst.init(self.rst.OUT, value=1)
        self.led.init(self.led.OUT, value=1)
        self.reset()
        for cmd,data in self._INIT:
            self._write(cmd, data)
            

    def reset(self):
        self.rst(0)
        utime.sleep_ms(50)
        self.rst(1)
        utime.sleep_ms(50)
        
    def _write(self, command=None, data=None):
        if command is not None:
            self.dc(0)
            self.cs(0)
            self.spi.write(bytearray([command]))
            self.cs(1)
        if data is not None:
            self.dc(1)
            self.cs(0)
            self.spi.write(data)
            self.cs(1)

    def _read(self, command=None, count=0):
        self.dc(0)
        self.cs(0)
        if command is not None:
            self.spi.write(bytearray([command]))
        if count:
            data = self.spi.read(count)
        self.cs(1)
        return data

    def stop_spi(self):
        self.spi.deinit()
        self.spi=None
                           
    def circle(self,x0,y0,r,c):
        x = -r
        y = 0
        err = 2-2 * r
        while True:
            self.pixel(x0 - x, y0 + y, c)
            self.pixel(x0 + x, y0 + y, c)
            self.pixel(x0 + x, y0 - y, c)
            self.pixel(x0 - x, y0 - y, c)
            e2 = err
            if e2 <= y:
                y+=1
                err += y * 2 + 1
                if -x == y and e2 <= x:
                    e2 = 0
            if e2 > x:
                x+=1
                err += x * 2 + 1
            if x >0:
                break
    def conv_font_to_rgb565(self,bs,w,bg,fg):
        #
        wb = int(w/8)
        nbs =bytearray()
        rbs=bs[:]
        while rbs:
            for i in range(wb):
                for j in range(8):
                    if BITMASK[j] & rbs[i]:
                        nbs.append(fg >> 8)
                        nbs.append(fg & 0xff)
                    else:
                        nbs.append(bg >> 8)
                        nbs.append(bg & 0xff)                        
            rbs=rbs[wb:]
        return nbs
    
    def draw_char_at(self,ch, x, y, font, bg=BLACK,fg=WHITE):
        h = font.Height
        bs = font.table.get(ch)   #[ch]
        w = int((len(bs) / h) * 8)
        nbs = self.conv_font_to_rgb565(bs,w,bg,fg)

        self.blit_buffer(nbs, x, y, w,h)
        return w

    def draw_string_at(self,text,x0,y0,font, bg=BLACK, fg=WHITE):
        x=x0
        for ch in text:
            w =self.draw_char_at(ch, x, y0, font,bg,fg)
            x+= w

    def fill_circle(self,x0,y0,r,c):
        x = -r
        y = 0
        err = 2-2 * r
        while True:
            self.pixel(x0 - x, y0 + y, c)
            self.pixel(x0 + x, y0 + y, c)
            self.pixel(x0 + x, y0 - y, c)
            self.pixel(x0 - x, y0 - y, c)
            self.hline(x0+x, y0+y, 2*(-x) + 1, c)
            self.hline(x0+x, y0-y, 2*(-x) + 1, c)
            e2 = err
            if e2 <= y:
                y+=1
                err += y * 2 + 1
                if -x == y and e2 <= x:
                    e2 = 0
            if e2 > x:
                x+=1
                err += x * 2 + 1
            if x >0:
                break

    def fill(self, color=0):
        self.fill_rect(0,0,self.width,self.height,color)

    def fill_rect(self,x,y,width,height,color):
        """Draw a filled rectangle."""
        x = min(self.width - 1, max(0, x))
        y = min(self.height - 1, max(0, y))
        w = min(self.width - x, max(1, width))
        h = min(self.height - y, max(1, height))
        self._block(x, y, x + w - 1, y + h - 1, b'')
        chunks, rest = divmod(w * h, 512)
        pixel = self._encode_pixel(color)
        if chunks:
            data = pixel * 512
            for count in range(chunks):
                self._write(None, data)
        if rest:
            self._write(None, pixel * rest)

    def _block(self, x0, y0, x1, y1, data=None):
        """Read or write a block of data."""
        self._write(self._COLUMN_SET, self._encode_pos(x0, x1))
        self._write(self._PAGE_SET, self._encode_pos(y0, y1))
        if data is None:
            size = ustruct.calcsize(self._DECODE_PIXEL)
            return self._read(self._RAM_READ,
                              (x1 - x0 + 1) * (y1 - y0 + 1) * size)
        self._write(self._RAM_WRITE, data)

    def _encode_pos(self, a, b):
        """Encode a postion into bytes."""
        return ustruct.pack(self._ENCODE_POS, a, b)


    def _encode_pixel(self, color):
        """Encode a pixel color into bytes."""
        return ustruct.pack(self._ENCODE_PIXEL, color)

    def _decode_pixel(self, data):
        """Decode bytes into a pixel color."""
        return color565(*ustruct.unpack(self._DECODE_PIXEL, data))

    def pixel(self, x, y, color=None):
        """Read or write a pixel."""
        if color is None:
            return self._decode_pixel(self._block(x, y, x, y))
        if not 0 <= x < self.width or not 0 <= y < self.height:
            return
        self._block(x, y, x, y, self._encode_pixel(color))

    def hline(self, x, y, width, color):
        """Draw a horizontal line."""
        self.fill_rect(x, y, width, 1, color)

    def vline(self, x, y, height, color):
        """Draw a vertical line."""
        self.fill_rect(x, y, 1, height, color)

    def plotLineLow(self,x0,y0,x1,y1,c):
        dx = x1 -x0
        dy = y1 -y0
        yi =1
        if dy <0:
            yi = -1
            dy = -dy
        D= 2*dy -dx
        y =y0
        x =x0
        while x < x1:
            self.pixel(x,y,c)
            if D >0:
                y += yi
                D -= 2*dx
            D += 2*dy
            x +=1

    def plotLineHigh(self, x0,y0,x1,y1,c):
        dx = x1 - x0
        dy = y1 -y0
        xi = 1
        if dx <0:
            xi =-1
            dx = -dx
        D = 2*dx -dy
        x = x0
        y = y0
        while y < y1:
            self.pixel(x,y,c)
            if D >0:
                x += xi
                D -= 2*dy
            D += 2*dx
            y+=1

    def rect(self, x,y,w,h,c):
        self.hline(x,y, w,c)
        self.hline(x,y+h,w,c)
        self.vline(x,y, h,c)
        self.vline(x+w,y,h,c)
    
    def line(self, x0,y0,x1,y1,c):
        # ref: https://en.wikipedia.org/wiki/Bresenham%27s_line_algorithm
        if abs(y1 -y0) < abs(x1 -x0):
            if x0 > x1:
                self.plotLineLow(x1,y1,x0,y0,c)
            else:
                self.plotLineLow(x0,y0,x1,y1,c)
        else:
            if y0 > y1:
                self.plotLineHigh(x1,y1,x0,y0,c)
            else:
                self.plotLineHigh(x0,y0,x1,y1,c)
                
    def blit_buffer(self, buffer, x, y, width, height):
        """Copy pixels from a buffer."""
        if (not 0 <= x < self.width or
            not 0 <= y < self.height or
            not 0 < x + width <= self.width or
            not 0 < y + height <= self.height):
            print('%s,%s,%s,%s,%s,%s' % (x,y,width,height,self.width,self.height))
            raise ValueError("out of bounds")
        self._block(x, y, x + width - 1, y + height - 1, buffer)

    def text(self, text, x=0, y=0, color=0xffff, background=0x0000):
        x = min(self.width - 1, max(0, x))
        y = min(self.height - 1, max(0, y))
        w = len(text) * 8  #self.width - x
        h = min(self.height - y, 8)
        #buffer = bytearray(self.width * h * 2)
        # kcf test, swap hi lo
        buffer = bytearray(w * h * 2)
        fb = framebuf.FrameBuffer(buffer, w, h, framebuf.RGB565)
        fb.fill(background)
        fb.text(text, 0, 0, color)
        self.blit_buffer(buffer, x, y, w, h)


    def on(self):
        self.led.value(1)

    def off(self):
        self.led.value(0)

#tft=TFT()

def test(tft):
    tft.start_spi()
    tft.fill(0)
    tft.hline(0,0,320,color565(255,0,0))
    tft.vline(0,0,240,color565(0,255,0))
    tft.fill_rect(10,10,300,220,color565(0,0,255))
    tft.text('Hello World',50,50)
    tft.fill_circle(100,100,30,color565(0,255,0))
    tft.circle(100,100,30,color565(0,255,255))
    tft.line(0,0,100,50,color565(255,255,0))
    tft.line(0,0,50,100,color565(255,0,255))
    tft.stop_spi()


        

    
