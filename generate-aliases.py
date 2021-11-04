#!/usr/bin/env python3
from os.path import join
from pathlib import Path
from subprocess import run
import argparse, os


# The template code for our alias scripts
TEMPLATE = '''#!/usr/bin/env bash
docker-shell --prefix-paths=/host '' '{}' -- "$@"
'''

# Generates an alias for the specified container image
def generate(alias, image):
	Path(alias).write_bytes(TEMPLATE.format(image).encode('utf-8'))
	run(['chmod', '+x', alias], check=True)


# Our supported command-line arguments
parser = argparse.ArgumentParser()
parser.add_argument('--outdir', default=os.getcwd(), help="The output directory for the generated alias scripts (defaults to the current directory)")

# Parse our command-line arguments
args = parser.parse_args()

# Generate aliases for all available applications
generate(join(args.outdir, 'foxit-reader'), 'adamrehn/wine-foxitreader:latest')
