#!/usr/bin/env python3
from pathlib import Path
from subprocess import run
import argparse


# The template wrapper script code
TEMPLATE = '''#!/usr/bin/env bash

# Ensure the bind-mounted AppData directory is writable by the non-root user
APPDATA_DIR="{}"
REGISTRY_FILE="$APPDATA_DIR/registry.reg"
sudo touch "$APPDATA_DIR"
sudo chown 1000:1000 "$APPDATA_DIR"

# Hide all Wine debug messages so they don't flood the output
export WINEDEBUG="-all"

# If there is any saved registry data in the AppData directory then restore it
if [ -f "$REGISTRY_FILE" ]; then
	wine64 reg import "$REGISTRY_FILE"
fi

# Run the application and wait for wineserver to finish execution
/usr/bin/entrypoint.py {} "{}" "$@"
/usr/bin/wait-for-wineserver.py

# Save any updated registry data to the AppData directory
wine64 reg export '{}' "$REGISTRY_FILE" /y
/usr/bin/wait-for-wineserver.py
'''


# Our supported command-line arguments
parser = argparse.ArgumentParser()
parser.add_argument('--architecture', required=True, type=int, choices=[32, 64], help="The architecture of the application (32-bit or 64-bit)")
parser.add_argument('--application', required=True, help='The path to the application that is being wrapped')
parser.add_argument('--appdataDir', required=True, help='The path to the application\'s AppData directory')
parser.add_argument('--registryKey',  required=True, help="The path to the application\'s root registry key")
parser.add_argument('--outfile', required=True, help="The output path for the generated wrapper script")

# Parse our command-line arguments
args = parser.parse_args()

# Fill out the template with the specified values
wrapper = TEMPLATE.format(
	args.appdataDir,
	'wine64' if args.architecture == 64 else 'wine',
	args.application,
	args.registryKey.replace('/', '\\')
)

# Write the completed wrapper script to the output file and mark it as executable
Path(args.outfile).write_bytes(wrapper.encode('utf-8'))
run(['chmod', '+x', args.outfile])
