# Restart the program at regular intervals

import subprocess
import sys
import time

while 1:
    p = subprocess.Popen(['python3', '/home/zx/Desktop/test/2.py'],
                         stdin=sys.stdin,
                         stdout=sys.stdout,
                         stderr=sys.stderr,
                         shell=False)

    time.sleep(3600)  # 1 h

    p.kill()
