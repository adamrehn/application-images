#!/usr/bin/env python3
from pathlib import Path
import sys

DOTNET_PATCHES = [
	
	# .NET Framework 4.7.2
	{
		'OldURL': 'https://download.microsoft.com/download/6/E/4/6E48E8AB-DC00-419E-9704-06DD46E5F81D/NDP472-KB4054530-x86-x64-AllOS-ENU.exe',
		'OldHash': 'c908f0a5bea4be282e35acba307d0061b71b8b66ca9894943d3cbb53cad019bc',
		'OldFile': 'NDP472-KB4054530-x86-x64-AllOS-ENU.exe',
		
		'NewURL': 'https://download.visualstudio.microsoft.com/download/pr/1f5af042-d0e4-4002-9c59-9ba66bcf15f6/089f837de42708daacaae7c04b7494db/ndp472-kb4054530-x86-x64-allos-enu.exe',
		'NewHash': '5cb624b97f9fd6d3895644c52231c9471cd88aacb57d6e198d3024a1839139f6',
		'NewFile': 'ndp472-kb4054530-x86-x64-allos-enu.exe'
	}
]

# Read the existing contents of the Winetricks script
winetricks = Path(sys.argv[1])
code = winetricks.read_bytes().decode('utf-8')

# Patch the download URL, installer checksum, and installer filename for each version of the .NET Framework
for version in DOTNET_PATCHES:
	code = code.replace(version['OldURL'], version['NewURL'])
	code = code.replace(version['OldHash'], version['NewHash'])
	code = code.replace(version['OldFile'], version['NewFile'])

# Write the changes back to disk
winetricks.write_bytes(code.encode('utf-8'))
