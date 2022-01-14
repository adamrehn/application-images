#!/usr/bin/env python3
from application_images_helpers.common import EntrypointHelpers
from os.path import dirname, exists, join
import os


# Creates a symlink from source to target if source exists
def symlink_if_exists(source, target):
	if exists(source):
		EntrypointHelpers._log('Creating symlink for directory {} at {}...'.format(source, target))
		os.makedirs(dirname(target), exist_ok=True)
		os.symlink(source, target)


# If the host user has a "GOG Games" directory, symlink it into our Wine prefix
hostUserDir = '/home/hostuser'
hostGogDir = join(hostUserDir, 'GOG Games')
symlink_if_exists(hostGogDir, join(os.environ['WINEPREFIX'], 'drive_c', 'GOG Games'))

# If the host user has Steam installed, symlink the steamapps directory into our Wine prefix
hostSteamappsDir = join(hostUserDir, '.local', 'share', 'Steam', 'steamapps')
symlink_if_exists(hostSteamappsDir, join(os.environ['WINEPREFIX'], 'drive_c', 'Program Files (x86)', 'Steam', 'steamapps'))
