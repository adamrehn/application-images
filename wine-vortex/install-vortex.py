#!/usr/bin/env python3
from subprocess import run, Popen, DEVNULL, PIPE, STDOUT
import os, sys


# Prints and executes a command, checking its exit code to verify success
def execute(command, **kwargs):
	print(command, flush=True)
	run(command, **kwargs, check=True)


# Start the installer as a child process and capture its output
installer = sys.argv[1]
child = Popen(
	['xvfb-run', '-a', 'wine64', installer],
	env={**os.environ, 'WINEDEBUG': '-taskschd,+x11drv'},
	stdin=DEVNULL,
	stdout=PIPE,
	stderr=STDOUT,
	universal_newlines=True
)

# Process the installer output until we detect that installation has completed and Vortex is attempting to start
output = ''
completed = False
while not completed:
	
	# Read the next chunk of output and print it
	buffer = child.stdout.read(1024)
	print(buffer, end='', flush=True)
	
	# Append the chunk to our existing output and check for the string that indicates the main installer window has closed
	output += buffer
	if 'X connection to :99 broken (explicit kill or server shutdown)' in output:
		completed = True

# Kill the Vortex process, since this will block `wineserver --wait` even though it doesn't block the installer process
print('\nInstaller has completed and Vortex has started automatically, stopping it...', flush=True)
execute(['wine64', 'taskkill', '/f', '/im', 'Vortex.exe'])

# Wait for the installer process to complete and then wait for Wine to flush all changes to disk
print('Vortex has stopped, waiting for all Wine processes to complete...', flush=True)
child.wait()
execute(['wineserver', '--wait'])
