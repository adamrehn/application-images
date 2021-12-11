from application_images_helpers.common import IOHelpers
import argparse, os


# The template entrypoint script code
ENTRYPOINT_TEMPLATE = '''#!/usr/bin/env python3
from application_images_helpers.common import EntrypointHelpers
import argparse

# Parse the supplied command-line arguments
parser = argparse.ArgumentParser(add_help=False)
parser.add_argument(
	'---entrypoint-additional-instance',
	action='store_true',
	help="Indicates that environment setup should be skipped because we are running an additional application instance in an existing container"
)
options, applicationArgs = parser.parse_known_args()

# Invoke the main function for the entrypoint
EntrypointHelpers.entrypoint_main(
	application={},
	configDir={},
	args=applicationArgs,
	useWine={},
	wineArchitecture={},
	skipSetup=options.entrypoint_additional_instance
)
'''


def generate_application_entrypoint():
	
	# Our supported command-line arguments
	parser = argparse.ArgumentParser()
	parser.add_argument('--application', required=True, help='The path to the application that is being wrapped')
	parser.add_argument('--architecture', required=False, type=int, choices=[32, 64], help="The architecture of the application (32-bit or 64-bit, only required for Wine)")
	parser.add_argument('--configDir', required=True, help='The path to the application\'s config directory (AppData directory for Wine)')
	parser.add_argument('--wine', action='store_true', help="Specifies that the application is a Windows executable that will be run through Wine")
	parser.add_argument('--outfile', required=True, help="The output path for the generated wrapper script")

	# Parse our command-line arguments
	args = parser.parse_args()
	
	# Fill out the entrypoint template with the supplied values and write it to the specified output file
	IOHelpers.write_file(args.outfile, ENTRYPOINT_TEMPLATE.format(
		repr(args.application),
		repr(args.configDir),
		repr(args.wine),
		repr(args.architecture)
	))
	
	# Mark the entrypoint script as executable
	os.chmod(args.outfile, 0o755)
