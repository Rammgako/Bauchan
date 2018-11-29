import signal
import os
import subprocess
import traceback

#Running bash script created in bauchand.py
def handle(signum, frame):
    print('Received signal, opening terminal')
    try:
        args = ['/usr/bin/open', '-n', '-a', 'Terminal', os.path.expanduser('~/.bauchan.temp.sh')]
        print('Executing: %s' % ' '.join(args))
        output = subprocess.check_output(args)
    except Exception:
        traceback.print_exc()
    else:
        print('Terminal should be opened: %s' % output)

#signal magic
signal.signal(signal.SIGUSR2, handle)

pid = os.getpid()
print('Running bauchand with PID=%d' % pid)
with open(os.path.expanduser('~/.bauchan.pid'), 'w') as f:
    f.write('%d\n' % pid)
while True:
    signal.pause()
