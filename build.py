#!/usr/bin/env python3
from subprocess import run
from itertools import chain
import argparse, sys


# Our build settings
TAG_PREFIX = 'adamrehn'
WINE_VERSION = '7.22'
WINETRICKS_COMMIT = 'acef23e09d291453e740584e30d7c2b46dad8a92'

# Our list of applications
APPLICATIONS = {
	
	'foobar2000': {
		'tag': 'wine-foobar2000:latest',
		'context': './wine-foobar2000',
		'dotnet': True
	},
	
	'foxitreader': {
		'tag': 'wine-foxitreader:latest',
		'context': './wine-foxitreader',
		'dotnet': True
	},
	
	'raymancontrolpanel': {
		'tag': 'wine-raymancontrolpanel:latest',
		'context': './wine-raymancontrolpanel',
		'dotnet': True
	},
	
	'vortex': {
		'tag': 'wine-vortex:latest',
		'context': './wine-vortex',
		'dotnet': True
	}
	
}


# Builds the specified container image
def build(dryRun, tag, context, buildArgs={}, options=[]):
	flags = [['--build-arg', '{}={}'.format(k,v)] for k, v in buildArgs.items()] + [options]
	command = ['docker', 'buildx', 'build', '--progress=plain', '-t', '{}/{}'.format(TAG_PREFIX, tag), context] + list(chain.from_iterable(flags))
	print(command, flush=True)
	if not dryRun:
		run(command, check=True)


# Parse our command-line arguments
parser = argparse.ArgumentParser()
parser.add_argument('--applications', default='', help="Only build the specified set of application images (comma-delimited list)")
parser.add_argument('--dry-run', action='store_true', help="Print build commands without running them")
parser.add_argument('--no-applications', action='store_true', help="Don't build any application images, just the base images")
parser.add_argument('--no-dotnet', action='store_true', help="Only build Mono images for Wine, not .NET Framework images")
args = parser.parse_args()

# Build our common base image
build(args.dry_run, 'application-image-base:latest', './common-base')

# Build our base images for running Windows applications with Wine (32-bit and 64-bit prefixes, with Mono and .NET Framework)
wineArgs = {'WINE_VERSION': WINE_VERSION}
build(args.dry_run, 'wine-base:{}'.format(WINE_VERSION), './wine/base', {**wineArgs, 'WINETRICKS_VERSION': WINETRICKS_COMMIT})
for architecture in [32, 64]:
	archFlags = {**wineArgs, 'WINE_ARCH': architecture}
	build(args.dry_run, 'wine-prefix{}:{}'.format(architecture, WINE_VERSION), './wine/prefix{}'.format(architecture), wineArgs)
	build(args.dry_run, 'wine-mono{}:{}'.format(architecture, WINE_VERSION), './wine/mono', archFlags)
	if not args.no_dotnet:
		build(args.dry_run, 'wine-dotnet{}:{}'.format(architecture, WINE_VERSION), './wine/dotnet', archFlags)

# Build the application images
if not args.no_applications:
	
	# Determine which application images we are building
	buildQueue = args.applications.split(',') if len(args.applications) > 0 else list(APPLICATIONS.keys())
	for application in [a for a in buildQueue if len(a) > 0]:
		
		# Verify that the specified application is valid
		details = APPLICATIONS.get(application, None)
		if details is None:
			print('Error: unknown application "{}"'.format(application), file=sys.stderr)
			sys.exit(1)
		
		# If the application is a Windows application that requires the .NET Framework and we're not building .NET images, then skip it
		if args.no_dotnet and details['dotnet'] == True:
			print('Skipping build for .NET Framework application "{}".'.format(application))
			continue
		
		# Build the image for the application
		build(args.dry_run, details['tag'], details['context'], wineArgs)
