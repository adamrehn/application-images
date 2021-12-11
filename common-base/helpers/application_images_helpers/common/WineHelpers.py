from .IOHelpers import IOHelpers
from os.path import exists, join
from subprocess import run
import os, shutil, tempfile


# Our mapping from Windows UI scale factors to DPI values
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

# The template for the .reg file used to configure Wine's DPI scaling settings
DPI_REGISTRY_TEMPLATE = '''Windows Registry Editor Version 5.00

[HKEY_CURRENT_USER\Control Panel\Desktop]
"LogPixels"=dword:{dpi}

[HKEY_CURRENT_USER\Software\Wine\Fonts]
"LogPixels"=dword:{dpi}

[HKEY_CURRENT_CONFIG\Software\Fonts]
"LogPixels"=dword:{dpi}
'''


class WineHelpers:
	'''
	Helper functionality related to running Windows applications through Wine
	'''
	
	@staticmethod
	def bind_mount_registry(configDir):
		'''
		Redirects Wine's registry files to use data from the application's bind-mounted configuration directory
		'''
		
		# If the _registry subdirectory of the config directory doesn't exist then create it
		registryDir = join(configDir, '_registry')
		if not exists(registryDir):
			os.makedirs(registryDir)
		
		# If the user.reg file doesn't exist in the config directory then populate it
		userRegOriginal = join(os.environ.get('WINEPREFIX'), 'user.reg')
		userRegBindMount = join(registryDir, 'user.reg')
		if not exists(userRegBindMount):
			shutil.copy2(userRegOriginal, userRegBindMount)
		
		# If the system.reg file doesn't exist in the config directory then populate it
		systemRegOriginal = join(os.environ.get('WINEPREFIX'), 'system.reg')
		systemRegBindMount = join(registryDir, 'system.reg')
		if not exists(systemRegBindMount):
			shutil.copy2(systemRegOriginal, systemRegBindMount)
		
		# Replace the Wine's registry files with symlinks to the bind-mounted files from the config directory
		os.unlink(userRegOriginal)
		os.unlink(systemRegOriginal)
		os.symlink(userRegBindMount, userRegOriginal)
		os.symlink(systemRegBindMount, systemRegOriginal)
	
	@staticmethod
	def configure_dpi_scaling(configDir, logFunc):
		'''
		Configures Wine's DPI scaling settings based on the WINESCALE environment variable
		'''
		
		# Attempt to retrieve the scale factor if one was specified, otherwise default to a scale of 1.0x (100%)
		scaleFactor = 1.0
		envValue = os.environ.get('WINESCALE', None)
		if envValue is not None:
			try:
				scaleFactor = float(envValue)
			except:
				logFunc('Warning: WINESCALE value {} is not a valid floating-point number, ignoring.'.format(envValue))
		
		# Find the closest supported scale factor
		if scaleFactor not in DPI_VALUES:
			candidates = list([s for s in reversed(DPI_VALUES.keys()) if scaleFactor >= s])
			closest = candidates[0] if len(candidates) > 0 else 1.0
			logFunc('Warning: requested scale factor {} is not supported, using {} instead.'.format(scaleFactor, closest))
			scaleFactor = closest
		
		# Retrieve the DPI value for our scale factor
		dpi = DPI_VALUES.get(scaleFactor)
		logFunc('Setting scale factor to {} (DPI: {})'.format(scaleFactor, dpi))
		
		# Determine whether the existing DPI settings (if any) match the desired scale factor
		dpiFile = join(configDir, '_registry', 'dpi.txt')
		if exists(dpiFile) and IOHelpers.read_file(dpiFile).strip() == str(dpi):
			
			logFunc('Existing DPI value matches desired DPI value, nothing to do.')
			
		else:
			
			# Generate a .reg file to update Wine's DPI scaling registry keys
			regFile = join(tempfile.gettempdir(), 'dpi.reg')
			IOHelpers.write_file(regFile, DPI_REGISTRY_TEMPLATE.format(dpi='{:0>8x}'.format(dpi)))
			
			# Import the keys into the registry
			command = ['wine64', 'regedit', '/S'] + WineHelpers.transform_paths([regFile])
			logFunc(command)
			run(command, check=True, capture_output=True, env={**os.environ, **{'WINEDEBUG': '-all'}})
			
			# Write the DPI value to disk so we can check it next time
			IOHelpers.write_file(dpiFile, str(dpi))
	
	@staticmethod
	def transform_paths(args):
		'''
		Transforms any Linux filesystem paths in the supplied command-line arguments into their Windows filesystem path counterparts
		'''
		
		# Process each command-line argument in turn
		winePrefix = os.environ.get('WINEPREFIX')
		processed = []
		for arg in args:
			
			# If the argument represents a Linux filesystem path then transform it into a Windows filesystem path
			# (Note: even if we aggregate multiple paths into a single invocation to avoid running multiple child processes, `winepath` is
			#  still far slower than desired and delays application startup times significantly, so we perform this transformation manually)
			if arg.startswith('/') and exists(arg):
				arg = arg.replace(winePrefix, 'C:') if arg.startswith(winePrefix) else 'Z:{}'.format(arg)
				arg = arg.replace('/', '\\')
			
			processed.append(arg)
		
		return processed
	
	@staticmethod
	def wait_for_wineserver():
		'''
		Waits for all processes running in the current Wine prefix to complete execution
		'''
		run(['wineserver', '--wait'])
