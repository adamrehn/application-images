#!/usr/bin/env python3
from os.path import join
from pathlib import Path
from subprocess import run
import argparse, docker


# Our list of application images
APPLICATIONS = {
	
	'foobar2000': {
		'image': 'adamrehn/wine-foobar2000:latest'
	},
	
	'foxit-reader': {
		'image': 'adamrehn/wine-foxitreader:latest'
	},
	
	'vortex': {
		'image': 'adamrehn/wine-vortex:latest',
		
		# Vortex handles nxm:// URLs
		'handles-urls': ['nxm']
	}
	
}

# The template code for our alias scripts
ALIAS_TEMPLATE = '''#!/usr/bin/env bash

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

# The template code for desktop entries
DESKTOP_TEMPLATE = '''[Desktop Entry]
Name={name}
Exec={alias} {param}
Terminal=true
Type=Application
{extra}
'''


# Generates an alias for the specified container image
def generate_alias(client, outdir, name, image):
	
	# Attempt to retrieve the container image entrypoint
	details = client.images.get(image)
	entrypoint = details.attrs.get('Config', {}).get('Entrypoint', None)
	if entrypoint is None:
		raise RuntimeError('failed to retrieve entrypoint for image "{}"!'.format(image))
	
	# Generate the alias script
	alias = join(outdir, name)
	Path(alias).write_bytes(ALIAS_TEMPLATE.format(name=name, image=image, entrypoint=' '.join(entrypoint)).encode('utf-8'))
	run(['chmod', '+x', alias], check=True)
	print('Generated alias "{}"'.format(alias))

# Generates an XDG desktop entry for the specified container image
def generate_desktop_entry(client, outdir, alias, image, handlesURLs):
	
	# Attempt to retrieve the required metadata from the container image
	details = client.images.get(image)
	labels = details.attrs['Config']['Labels'] if details.attrs['Config']['Labels'] is not None else {}
	candidates = list([labels[key] for key in labels if key == 'application-images.name'])
	name = candidates[0] if len(candidates) > 0 else None
	if name is None:
		raise RuntimeError('failed to retrieve application name metadata for image "{}"!'.format(image))
	
	# Generate the desktop entry
	entry = join(outdir, '{}.desktop'.format(name))
	Path(entry).write_bytes(DESKTOP_TEMPLATE.format(
		name = name,
		alias = alias,
		param = '%u' if handlesURLs is not None else '%F',
		extra = 'MimeType={};'.format(';'.join(['x-scheme-handler/{}'.format(scheme) for scheme in handlesURLs])) if handlesURLs is not None else ''
	).encode('utf-8'))
	run(['chmod', '+x', entry], check=True)
	print('Generated desktop entry "{}"'.format(entry))


# Our supported command-line arguments
parser = argparse.ArgumentParser()
parser.add_argument('--alias-dir', default='/usr/local/bin', help="The output directory for generated alias scripts (defaults to /usr/local/bin)")
parser.add_argument('--desktop-dir', default='/usr/share/applications', help="The output directory for generated desktop entries (defaults to /usr/share/applications)")
parser.add_argument('--desktop', action='store_true', help="Generate XDG desktop entries in addition to aliases")

# Parse our command-line arguments
args = parser.parse_args()

# Generate aliases for all available applications
client = docker.from_env()
for alias, details in APPLICATIONS.items():
	generate_alias(client, args.alias_dir, alias, details['image'])

# Generate desktop entries if requested
if args.desktop == True:
	for alias, details in APPLICATIONS.items():
		generate_desktop_entry(client, args.desktop_dir, alias, details['image'], details.get('handles-urls', None))
	run(['update-desktop-database'], check=True)
