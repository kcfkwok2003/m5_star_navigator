# -*- coding: utf-8 -*-
import sys
import gc

class Table:
    def __init__(self,thres=10):
        self.dictx={}
        self.info={'c':{},'e':{}}
        self.info['c']['font_path']=None
        self.info['e']['font_path']=None
        self.info['c']['fd']=None
        self.info['e']['fd']=None
        self.info['c']['dictm']={}
        self.info['e']['dictm']={}
        self.info['c']['NBYTES']=0
        self.info['e']['NBYTES']=0
        self.thres=thres

    def set_c(self, font_info):
        global Height
        self.info['c']['font_path']='%s.cg' % font_info        
        mapx = __import__('%smap' % font_info)
        self.info['c']['dictm']=mapx.dictm
        self.NBYTES=self.info['c']['NBYTES']=mapx.NBYTES
        Height = mapx.Height

    def set_e(self, font_info):
        global Height
        self.info['e']['font_path']='%s.cg' % font_info        
        mapx = __import__('%smap' % font_info)
        self.info['e']['dictm']=mapx.dictm
        self.NBYTES=self.info['e']['NBYTES']=mapx.NBYTES
        Height = mapx.Height
        
    def open_file(self,n):
        try:
            fd = open(self.info[n]['font_path'],'rb')
            return fd
        except Exception as e:
            self.fd=None
            if sys.platform=='esp32':
                sys.print_exception(e)
            else:
                print('exc',e)
                

    def _get(self,n,k):
        if not self.info[n]['fd']:
            self.info[n]['fd']=self.open_file(n)
        if len(self.dictx) > self.thres:
            del self.dictx
            self.dictx={}
            gc.collect()
        fd = self.info[n]['fd']
        dictm = self.info[n]['dictm']
        NBYTES = self.info[n]['NBYTES']
        if fd:
            if k in dictm:
                ofs = dictm[k]
                fd.seek(ofs)
                bs = fd.read(NBYTES)
                self.dictx[k]=bs
                return bs
        return bytearray([0x00]*NBYTES)
    
    def get(self,k):
        if k in self.dictx:
            return self.dictx[k]
        if k in self.info['c']['dictm']:
            return self._get('c',k)
        if k in self.info['e']['dictm']:
            return self._get('e',k)
        return bytearray([0x00]*self.NBYTES)
            


table=Table()
    
