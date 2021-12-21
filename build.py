#!/usr/bin/env python3
from subprocess import run
from itertools import chain


TAG_PREFIX = 'adamrehn'
WINE_VERSION = '6.22'


# Builds the specified container image
def build(tag, context, buildArgs={}, options=[]):
	flags = [['--build-arg', '{}={}'.format(k,v)] for k, v in buildArgs.items()] + [options]
	command = ['docker', 'buildx', 'build', '--progress=plain', '-t', tag, context] + list(chain.from_iterable(flags))
	print(command, flush=True)
	run(command, check=True)


# Build our common base image
build('adamrehn/common-base:latest', './common-base')

# Build our base images for running Windows applications with Wine (32-bit and 64-bit prefixes, with .NET Framework and Mono)
wineArgs = {'WINE_VERSION': WINE_VERSION}
build('adamrehn/wine-base:{}'.format(WINE_VERSION), './wine/base', {**wineArgs, 'WINETRICKS_VERSION': '4340f09f0c17566205dcc74e15211ddac7780148'})
for architecture in [32, 64]:
	build('adamrehn/wine-prefix{}:{}'.format(architecture, WINE_VERSION), './wine/prefix{}'.format(architecture), wineArgs)
	build('adamrehn/wine-dotnet{}:{}'.format(architecture, WINE_VERSION), './wine/dotnet', {**wineArgs, 'WINE_ARCH': architecture})
	build('adamrehn/wine-mono{}:{}'.format(architecture, WINE_VERSION), './wine/mono', {**wineArgs, 'WINE_ARCH': architecture})

# Build our images for Windows applications
build('adamrehn/wine-foobar2000:latest', './wine-foobar2000', wineArgs)
build('adamrehn/wine-foxitreader:latest', './wine-foxitreader', wineArgs)
