#!/usr/bin/env python3
from subprocess import run
import os, sys


# Our mapping from scale factors to DPI values
# (Lookup table from here: <https://www.tenforums.com/tutorials/5990-change-dpi-scaling-level-displays-windows-10-a.html>)
DPI_VALUES = {
	
	# 100% => 96pt DPI
	1.0: 96,
	
	# 125% => 120pt DPI
	1.25: 120,
	
	# 150% => 144pt DPI
	1.5: 144,
	
	# 200% => 192pt DPI
	2.0: 192,
	
	# 250% => 240pt DPI
	2.5: 240,
	
	# 300% => 288pt DPI
	3.0: 288,
	
	# 400% => 384pt DPI
	4.0: 384,
	
	# 500% => 480pt DPI
	5.0: 480
	
}

# Logs a message to stderr
def log(message):
	print(message, file=sys.stderr, flush=True)

# If the supplied command-line parameter represents a filesystem path then this transforms it so it can be passed to the entrypoint command
def processPaths(p):
	p = os.path.expandvars(p)
	if p.startswith('/') and os.path.exists(p):
		p = run(['winepath', '--windows', p], capture_output=True).stdout.decode('utf-8').strip()
	return p


# Attempt to retrieve the scale factor if one was specified, otherwise default to a scale of 1.0x (100%)
scaleFactor = 1.0
envValue = os.environ.get('WINESCALE', None)
if envValue is not None:
	try:
		scaleFactor = float(envValue)
	except:
		log('Warning: WINESCALE value {} is not a valid floating-point number, ignoring.'.format(envValue))

# Find the closest supported scale factor
if scaleFactor not in DPI_VALUES:
	candidates = list([s for s in reversed(DPI_VALUES.keys()) if scaleFactor >= s])
	closest = candidates[0] if len(candidates) > 0 else 1.0
	log('Warning: requested scale factor {} is not supported, using {} instead.'.format(scaleFactor, closest))
	scaleFactor = closest

# Retrieve the DPI value for our scale factor and convert it to a hexadecimal representation with 8 digits as expected by `reg add`
# (Format specifier from here: <https://stackoverflow.com/a/12638477>)
dpi = '{0:#0{1}x}'.format(DPI_VALUES.get(scaleFactor), 8 + len('0x'))

# Update Wine's DPI scaling registry keys
env = {**os.environ, **{'WINEDEBUG': '-all'}}
for key in ['HKCU\\Control Panel\\Desktop', 'HKCU\\Software\\Wine\\Fonts', 'HKCC\\Software\\Fonts']:
	command = ['wine64', 'reg', 'add', key, '/t', 'REG_DWORD', '/v', 'LogPixels', '/d', dpi, '/f']
	log(command)
	run(command, check=True, env=env)

# If an entrypoint command was specified then run it, otherwise just start a bash shell
entrypoint = list([processPaths(a) for a in sys.argv[1:]]) if len(sys.argv) > 1 else ['/bin/bash']
log(entrypoint)
sys.exit(run(entrypoint).returncode)
