#!/usr/bin/env python3
from application_images_helpers.common import EntrypointHelpers, IOHelpers
from os.path import basename, expanduser, expandvars, isdir, join
import glob, itertools, os, re, sys


# Ensures correct casing of a configuration directory name
def fixDirectoryCasing(directory):
	return directory[0:1].upper() + directory[1:]

# Strips leading and trailing whitespace from an application name
def fixManifestName(match):
	return '{}"name"{}"{}"{}'.format(
		match.group(1),
		match.group(2),
		match.group(3).strip(),
		match.group(4),
	)

# Creates a symlink from the source directory to an appropriately-named child directory of dest
def symlinkDirectory(source, dest):
	link = join(dest, fixDirectoryCasing(basename(source)))
	EntrypointHelpers._log('Creating symlink for directory {} at {}...'.format(source, link))
	os.symlink(source, link, target_is_directory=True)


# Run our additional logic when the first instance of Vortex is opened
if '---entrypoint-additional-instance' not in sys.argv:
	
	# Resolve the absolute paths to Steam's `steamapps` and `compatdata` directories
	steamappsDir = expanduser('/home/hostuser/.local/share/Steam/steamapps')
	compatdataDir = join(steamappsDir, 'compatdata')
	
	# If the Wine prefix used by Vortex doesn't have a "My Games" subdirectory in the Documents directory then create it
	myGamesDir = expandvars('$WINEPREFIX/drive_c/users/nonroot/Documents/My Games')
	os.makedirs(myGamesDir, exist_ok=True)
	
	# Iterate over each of Steam's application manifests and remove whitespace issues that prevent Vortex from detecting games correctly
	regex = re.compile(r'^(\s*)"name"(\s*)"(.+)"(\s*)$', re.MULTILINE)
	for manifest in glob.glob(join(steamappsDir, 'appmanifest_*.acf')):
		contents = IOHelpers.read_file(manifest)
		fixed = regex.sub(fixManifestName, contents)
		if fixed != contents:
			EntrypointHelpers._log('Fixing whitespace in manifest file {}...'.format(manifest))
			IOHelpers.write_file('{}.bak'.format(manifest), contents)
			IOHelpers.write_file(manifest, fixed)
	
	# Iterate over each of Steam's Proton prefixes and symlink any local AppData subdirectories into the Wine prefix used by Vortex
	appDataDir = expandvars('$WINEPREFIX/drive_c/users/nonroot/AppData/Local')
	for dataDir in glob.glob(join(compatdataDir, '*', 'pfx/drive_c/users/steamuser/AppData/Local', '*')):
		if isdir(dataDir) and basename(dataDir) not in ['CEF', 'Microsoft']:
			symlinkDirectory(dataDir, appDataDir)
	
	# Iterate over each of Steam's Proton prefixes and symlink any "My Games" subdirectories into the Wine prefix used by Vortex
	documentsDirs = join(compatdataDir, '*', 'pfx/drive_c/users/steamuser/Documents')
	patterns = [join(documentsDirs, 'My Games', '*'), join(documentsDirs, 'my games', '*')]
	for gameDir in itertools.chain.from_iterable([glob.glob(p) for p in patterns]):
		if isdir(gameDir):
			symlinkDirectory(gameDir, myGamesDir)

