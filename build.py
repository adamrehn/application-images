#!/usr/bin/env python3
from subprocess import run


# Builds the specified container image
def build(tag, context):
	run(['docker', 'buildx', 'build', '--progress=plain', '-t', tag, context], check=True)


# Build all available container images
build('adamrehn/common-base:latest', './common-base')
build('adamrehn/wine-base:latest', './wine/base')
build('adamrehn/wine-dotnet:latest', './wine/dotnet')
build('adamrehn/wine-foxitreader:latest', './wine-foxitreader')
