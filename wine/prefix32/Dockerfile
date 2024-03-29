ARG WINE_VERSION
FROM adamrehn/wine-base:${WINE_VERSION}

# Install the 32-bit version of the PulseAudio command line tools package
RUN --mount=type=cache,target=/var/cache/apt --mount=type=cache,target=/var/lib/apt \
	apt-get update && apt-get install -y --no-install-recommends pulseaudio-utils:i386

# Create a new 32-bit Wine prefix for our non-root user
USER nonroot
ENV WINEARCH=win32
ENV WINEPREFIX=/home/nonroot/.local/share/wineprefixes/prefix
RUN mkdir -p "$WINEPREFIX"
RUN wineboot && wineserver --wait

# Configure Wine to use PulseAudio for audio output
RUN winetricks --unattended settings sound=pulse && wineserver --wait

# Preinstall the 32-bit version of Wine Gecko
RUN curl -fSL 'https://dl.winehq.org/wine/wine-gecko/2.47.2/wine-gecko-2.47.2-x86.msi' -o /tmp/wine-gecko-x86.msi && \
	xvfb-run -a wine msiexec /i /tmp/wine-gecko-x86.msi && \
	wineserver --wait && \
	rm /tmp/wine-gecko-x86.msi

# Install the Windows version of Python 3.9
RUN xvfb-run -a winetricks --unattended dlls corefonts && xvfb-run -a winetricks --unattended settings win10
RUN curl -fSL 'https://www.python.org/ftp/python/3.9.9/python-3.9.9.exe' -o /tmp/python.exe && \
	xvfb-run -a wine /tmp/python.exe /quiet InstallAllUsers=1 PrependPath=1 TargetDir=C:/Python39 && \
	wineserver --wait && \
	rm /tmp/python.exe && \
	sudo generate-tool-alias --outfile /usr/bin/wine-pip3 --command "WINEDEBUG=-all wine '$WINEPREFIX/drive_c/Python39/Scripts/pip3.exe'"

# Install the dll-diagnostics tool
RUN wine-pip3 install setuptools wheel && \
	wine-pip3 install dll-diagnostics && \
	wineserver --wait && \
	sudo generate-tool-alias --outfile /usr/bin/dlldiag --command "WINEDEBUG=-all wine '$WINEPREFIX/drive_c/Python39/Scripts/dlldiag.exe'"
