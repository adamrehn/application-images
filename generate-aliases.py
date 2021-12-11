#!/usr/bin/env python3
from os.path import join
from pathlib import Path
from subprocess import run
import argparse, docker, os


# The template code for our alias scripts
TEMPLATE = '''#!/usr/bin/env bash

# Determine if an instance of the container image for this application is already running
EXISTING=`docker ps --filter 'name={name}-running' --format '{{{{.ID}}}}'`
if [ "$EXISTING" != "" ]; then
	
	# Start a second instance of the application inside the running container
	docker exec -ti '{name}-running' {entrypoint} ---entrypoint-additional-instance "$@"
	
else
	
	# Start a new container for the application
	docker-shell --name='{name}-running' '' '{image}' -- "$@"
	
fi
'''

# Generates an alias for the specified container image
def generate(client, outdir, name, image):
	
	# Attempt to retrieve the container image entrypoint
	details = client.images.get(image)
	entrypoint = details.attrs.get('Config', {}).get('Entrypoint', None)
	if entrypoint is None:
		raise RuntimeError('failed to retrieve entrypoint for image "{}"!'.format(image))
	
	# Generate the alias script
	alias = join(outdir, name)
	Path(alias).write_bytes(TEMPLATE.format(name=name, image=image, entrypoint=' '.join(entrypoint)).encode('utf-8'))
	run(['chmod', '+x', alias], check=True)


# Our supported command-line arguments
parser = argparse.ArgumentParser()
parser.add_argument('--outdir', default=os.getcwd(), help="The output directory for the generated alias scripts (defaults to the current directory)")

# Parse our command-line arguments
args = parser.parse_args()

# Generate aliases for all available applications
client = docker.from_env()
generate(client, args.outdir, 'foxit-reader', 'adamrehn/wine-foxitreader:latest')
