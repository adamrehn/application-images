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


# Build all available container images
wineArgs = {'WINE_VERSION': WINE_VERSION}
build('adamrehn/common-base:latest', './common-base')
build('adamrehn/wine-base:{}'.format(WINE_VERSION), './wine/base', {**wineArgs, 'WINETRICKS_VERSION': '4340f09f0c17566205dcc74e15211ddac7780148'})
build('adamrehn/wine-prefix32:{}'.format(WINE_VERSION), './wine/prefix32', wineArgs)
build('adamrehn/wine-prefix64:{}'.format(WINE_VERSION), './wine/prefix64', wineArgs)
build('adamrehn/wine-dotnet32:{}'.format(WINE_VERSION), './wine/dotnet', {**wineArgs, 'WINE_ARCH': '32'})
build('adamrehn/wine-dotnet64:{}'.format(WINE_VERSION), './wine/dotnet', {**wineArgs, 'WINE_ARCH': '64'})
build('adamrehn/wine-mono32:{}'.format(WINE_VERSION), './wine/mono', {**wineArgs, 'WINE_ARCH': '32'})
build('adamrehn/wine-mono64:{}'.format(WINE_VERSION), './wine/mono', {**wineArgs, 'WINE_ARCH': '64'})
build('adamrehn/wine-foxitreader:latest', './wine-foxitreader', wineArgs)
