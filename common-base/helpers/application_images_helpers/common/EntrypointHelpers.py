from .IOHelpers import IOHelpers
from .WineHelpers import WineHelpers
from os.path import exists, expandvars, join
from subprocess import run
import os

class EntrypointHelpers:
	'''
	Helper functionality for container image entrypoint scripts
	'''
	
	@staticmethod
	def _log(message):
		'''
		Prints a formatted log message to stderr
		'''
		IOHelpers.log_stderr('[entrypoint] {}'.format(message), color='cyan', attrs=['bold'])
	
	@staticmethod
	def _ensure_config_dir_exists(configDir):
		'''
		Ensures the application's bind-mounted configuration directory exists and is owned by the non-root user
		'''
		
		# Create the directory if it doesn't already exist
		if not exists(configDir):
			os.makedirs(configDir)
		
		# If the directory is not already owned by the non-root user then take ownership of it
		nonrootUID = os.geteuid()
		nonrootGID = os.getgid()
		info = os.stat(configDir)
		if info.st_uid != nonrootUID or info.st_gid != nonrootGID:
			run(['sudo', 'chown', '{}:{}'.format(nonrootUID, nonrootGID), configDir], check=True)
	
	@staticmethod
	def _setup_environment(configDir, useWine):
		'''
		Performs initial environment setup when the container first starts
		'''
		
		# Ensure the application's bind-mounted configuration directory exists and is owned by the non-root user
		EntrypointHelpers._log('Ensuring the bind-mounted configuration directory exists and is owned by the non-root user...')
		EntrypointHelpers._ensure_config_dir_exists(configDir)
		
		# If we are running an application with Wine then perform the appropriate setup
		if useWine:
			
			# Store registry data in the bind-mounted configuration directory to ensure it persists across multiple runs
			EntrypointHelpers._log('Redirecting the Wine registry to the bind-mounted configuration directory...')
			WineHelpers.bind_mount_registry(configDir)
			
			# Configure Wine's DPI scaling settings based on the WINESCALE environment variable
			EntrypointHelpers._log('Configuring Wine DPI scaling settings...')
			WineHelpers.configure_dpi_scaling(configDir, lambda message: EntrypointHelpers._log('-- {}'.format(message)))
	
	@staticmethod
	def _process_paths(args, useWine):
		'''
		Transforms any filesystem paths in the supplied command-line arguments to ensure they can be consumed by the application
		'''
		
		# Process each command-line argument in turn
		processed = []
		for arg in args:
			
			# Expand any variables in the argument
			arg = expandvars(arg)
			
			# If the argument represents a path on the host filesystem then prefix it with the bind-mount for the root of the host filesystem
			hostPath = join('/host', arg[1:])
			if arg.startswith('/') and not exists(arg) and exists(hostPath):
				arg = hostPath
			
			processed.append(arg)
		
		# If we are running an application with Wine then perform any additional necessary transformations
		if useWine:
			EntrypointHelpers._log('Transforming Linux filesystem paths into Windows filesystem paths...')
			processed = WineHelpers.transform_paths(processed)
		
		return processed
	
	@staticmethod
	def entrypoint_main(application, configDir, args=[], useWine=False, wineArchitecture=None, skipSetup=False):
		'''
		The main startup function for container image entrypoint scripts
		'''
		
		# Perform initial setup, unless we are skipping it (e.g. when running additional application instances in an existing container)
		if not skipSetup:
			EntrypointHelpers._setup_environment(configDir, useWine)
		
		# If we are running an application with Wine then configure the application accordingly
		commandPrefix = []
		envVars = {}
		if useWine:
			commandPrefix = ['wine64' if wineArchitecture == 64 else 'wine']
			envVars['WINEDEBUG'] = '-all'
		
		# Execute the application and wait for it to complete
		command = commandPrefix + [application] + EntrypointHelpers._process_paths(args, useWine)
		EntrypointHelpers._log(command)
		run(command, env={**os.environ, **envVars})
		
		# If we are running an application with Wine and this is the primary application instance then wait for the Wine server to complete execution
		if useWine and not skipSetup:
			EntrypointHelpers._log('Waiting for wineserver to finish running...')
			WineHelpers.wait_for_wineserver()
