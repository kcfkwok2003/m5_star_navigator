
g_width=20
g_sign={}
g_sign['ari']=bytearray([
     0x00, 0x00, 0x00, 0x00, 0x18, 0x0c, 0x24, 0x12, 0x42, 0x21, 0x42, 0x21,
   0x84, 0x10, 0x80, 0x00, 0x80, 0x00, 0x80, 0x00, 0x80, 0x00, 0x80, 0x00,
   0x80, 0x00, 0x80, 0x00, 0x80, 0x00, 0x00, 0x00])
g_sign['tau']=bytearray([
     0x00, 0x00, 0x00, 0x00, 0x06, 0x30, 0x08, 0x08, 0x10, 0x04, 0x20, 0x02,
   0xc0, 0x01, 0x30, 0x06, 0x08, 0x08, 0x08, 0x08, 0x04, 0x10, 0x04, 0x10,
   0x08, 0x08, 0x08, 0x08, 0x30, 0x06, 0xc0, 0x01 ])
g_sign['gem']=bytearray([
     0x01, 0x40, 0x06, 0x30, 0xf8, 0x0f, 0x10, 0x04, 0x10, 0x04, 0x10, 0x04,
   0x10, 0x04, 0x10, 0x04, 0x10, 0x04, 0x10, 0x04, 0x10, 0x04, 0xf8, 0x0f,
   0x06, 0x30, 0x01, 0x40, 0x00, 0x00, 0x00, 0x00])
g_sign['can']=bytearray([
     0x80, 0x03, 0x60, 0x0c, 0x10, 0x30, 0x08, 0x40, 0x0e, 0x80, 0x11, 0x00,
   0x11, 0x00, 0x11, 0x70, 0x0e, 0x88, 0x00, 0x88, 0x00, 0x88, 0x01, 0x70,
   0x02, 0x10, 0x0c, 0x08, 0x30, 0x06, 0xc0, 0x01])
g_sign['leo']=bytearray([
      0x80, 0x01, 0x60, 0x06, 0x10, 0x08, 0x08, 0x10, 0x08, 0x10, 0x1c, 0x08,
   0x22, 0x08, 0x41, 0x04, 0x41, 0x04, 0x41, 0x02, 0x22, 0x02, 0x1c, 0x44,
   0x00, 0x24, 0x00, 0x18, 0x00, 0x00, 0x00, 0x00])
g_sign['vir']=bytearray([
     0x18, 0x03, 0xa5, 0x04, 0x63, 0x04, 0x21, 0x04, 0x21, 0x14, 0x21, 0x2c,
   0x21, 0x44, 0x21, 0x44, 0x21, 0x24, 0x21, 0x14, 0x21, 0x08, 0x21, 0x34,
   0x00, 0x02, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00])
g_sign['lib']=bytearray([
     0x80, 0x01, 0x60, 0x06, 0x10, 0x08, 0x10, 0x08, 0x08, 0x10, 0x08, 0x10,
   0x10, 0x08, 0x10, 0x08, 0x60, 0x06, 0x40, 0x02, 0x7e, 0x7e, 0x00, 0x00,
   0x00, 0x00, 0xfe, 0x7f, 0x00, 0x00, 0x00, 0x00])
g_sign['sco']=bytearray([
     0x18, 0x03, 0xa5, 0x04, 0x63, 0x04, 0x21, 0x04, 0x21, 0x04, 0x21, 0x04,
   0x21, 0x04, 0x21, 0x04, 0x21, 0x04, 0x21, 0x04, 0x21, 0x48, 0x21, 0xf0,
   0x00, 0x40, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00])
g_sign['sag']=bytearray([
     0x00, 0x3e, 0x00, 0x30, 0x00, 0x28, 0x00, 0x24, 0x08, 0x22, 0x10, 0x01,
   0xa0, 0x00, 0x40, 0x00, 0xa0, 0x00, 0x10, 0x01, 0x08, 0x02, 0x04, 0x00,
   0x02, 0x00, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00])
g_sign['cap']=bytearray([
       0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x60, 0x00, 0x51, 0x00, 0x51, 0x00,
   0x51, 0x00, 0x4a, 0x00, 0x84, 0x38, 0x84, 0x44, 0x80, 0x82, 0x00, 0x81,
   0x80, 0x82, 0x40, 0x44, 0x00, 0x38, 0x00, 0x00])
g_sign['aqu']=bytearray([
     0x00, 0x00, 0x10, 0x42, 0x18, 0x63, 0x94, 0x52, 0xa4, 0x94, 0x62, 0x8c,
   0x21, 0x84, 0x00, 0x00, 0x00, 0x00, 0x10, 0x42, 0x18, 0x63, 0x94, 0x52,
   0xa4, 0x94, 0x62, 0x8c, 0x21, 0x84, 0x00, 0x00])
g_sign['pis']=bytearray([
     0x00, 0x00, 0x02, 0x10, 0x04, 0x08, 0x08, 0x04, 0x08, 0x04, 0x10, 0x02,
   0x10, 0x02, 0xfe, 0x1f, 0x10, 0x02, 0x10, 0x02, 0x08, 0x04, 0x08, 0x04,
   0x04, 0x08, 0x02, 0x10, 0x00, 0x00, 0x00, 0x00])

