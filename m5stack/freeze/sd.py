from machine import SDCard, Pin
import sys
import os

PIN_MISO=2
PIN_MOSI=23
PIN_SCK=18
PIN_CS=13
SD_PATH='/sd'

class SD:
    def __init__(self,miso=PIN_MISO, mosi=PIN_MOSI, sck=PIN_SCK, cs=PIN_CS, sd_path=SD_PATH):
        self.miso=miso
        self.mosi=mosi
        self.cs = cs
        self.sck = sck
        self.sdcard=None
        self.sd_path=sd_path
        self.inited=False
        self.mounted=False
        
    def start(self):
        try:
            self.sdcard = SDCard(slot=2, miso=Pin(self.miso), mosi=Pin(self.mosi), sck=Pin(self.sck), cs=Pin(self.cs))
            self.inited=True
            self.mount()
        except Exception as e:
            sys.print_exception(e) 
            print('sd init failure')
            
    def mount(self):
        try:
            os.mount(self.sdcard,self.sd_path)
            self.mounted=True
        except Exception as e:
            sys.print_exception(e) 
            print('sd mount failure')
            

    def stop(self):
        if self.mounted:
            self.mounted=False
            try:
                os.umount(self.sd_path)
            except Exception as e:
                sys.print_exception(e) 
                print('sd umount failure')
        if self.inited:
            try:
                self.sdcard.deinit()
            except Exception as e:
                sys.print_exception(e) 
                print('sd deinit failure')
            
