#clean.py
#run in docker
version="1.0"
ref_path="/mpy/kcfkwok/m5stack"
target_path="/mpy/micropython/ports/esp32/modules"

import os
fs = os.listdir(ref_path)
for fx in fs:
    fn = '%s/%s' % (target_path, fx)
    if os.path.isfile(fn):
        print('rm %s' % fn)
        os.remove(fn)
