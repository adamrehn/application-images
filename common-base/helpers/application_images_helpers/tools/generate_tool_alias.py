from application_images_helpers.common import IOHelpers
import argparse, os

def generate_tool_alias():
	
	# Our supported command-line arguments
	parser = argparse.ArgumentParser()
	parser.add_argument('--command', required=True, help='The command being aliases')
	parser.add_argument('--outfile', required=True, help="The output path for the generated alias script")

	# Parse our command-line arguments
	args = parser.parse_args()
	
	# Fill out the alias template with the supplied values and write it to the specified output file
	template = '#!/usr/bin/env bash\n{} "$@"'
	IOHelpers.write_file(args.outfile, template.format(args.command))
	
	# Mark the alias script as executable
	os.chmod(args.outfile, 0o755)
