#!/usr/bin/env python3
from subprocess import run
import sys, time

# Wait for `wineserver` to flush any pending changes to disk and exit before we finish, otherwise the changes won't be captured in the filesystem layer
print('Waiting for wineserver to finish execution...', file=sys.stderr, flush=True)
pid = 'dummy'
while len(pid) > 0:
	time.sleep(1)
	pid = run(['pidof', 'wineserver'], capture_output=True).stdout.decode('utf-8').strip()
