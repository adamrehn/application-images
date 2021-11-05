#!/usr/bin/env python3
from subprocess import run
import sys


# Logs a message to stderr
def log(message):
	print(message, file=sys.stderr, flush=True)


# Run `reg add` with the supplied arguments, converting Dockerfile-friendly forward slashes in the key path to the expected backslashes
for wine in ['wine', 'wine64']:
	command = ['xvfb-run', '-a', wine, 'reg', 'add', sys.argv[1].replace('/', '\\')] + sys.argv[2:]
	log(command)
	run(command, check=True)

# Wait for `wineserver` to flush the registry changes to disk and exit before we finish, otherwise the changes won't be captured in the filesystem layer
run('/usr/bin/wait-for-wineserver.py')
