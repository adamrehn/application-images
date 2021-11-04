FROM adamrehn/wine-dotnet:latest

# Install Foxit PDF Reader
# (Note that the installer requires GUI support even in silent mode, so we create a temporary virtual display with Xvfb)
RUN curl -fSL 'https://cdn06.foxitsoftware.com/product/reader/desktop/win/11.1.0/FoxitPDFReader111_L10N_Setup_Prom.exe' -o /tmp/foxit-installer.exe && \
	xvfb-run -a wine /tmp/foxit-installer.exe /verysilent /MERGETASKS='!desktopicon,!startmenufolder,!quicklaunchicon,!setdefaultreader,!setcollectdata,!displayinbrowser' /COMPONENTS='*pdfviewer,!ffse,!ffaddin,!ffspellcheck' && \
	/usr/bin/wait-for-wineserver.py

# Prevent the host system's window manager from decorating Foxit Reader's windows, since this interferes with the custom window decorations
RUN /usr/bin/reg-add.py 'HKCU/Software/Wine/AppDefaults/FoxitPDFReader.exe/X11 Driver' /v Decorated /t REG_SZ /d 'N' /f

# Generate a wrapper script to run Foxit Reader
RUN /usr/bin/generate-wrapper.py \
	--application "C:/Program Files (x86)/Foxit Software/Foxit PDF Reader/FoxitPDFReader.exe" \
	--appdataDir "$WINEPREFIX/drive_c/users/nonroot/AppData/Roaming/Foxit Software" \
	--registryKey 'HKCU/Software/Foxit Software' \
	--outfile /home/nonroot/foxitreader.sh

# Set our wrapper script as the container's default entrypoint
ENTRYPOINT ["/home/nonroot/foxitreader.sh"]

# Configure a bind-mount for Foxit Reader's persistent configuraton data
LABEL docker-shell.mounts.wine-foxitreader.1="~/.config/FoxitReader:/home/nonroot/.local/share/wineprefixes/prefix/drive_c/users/nonroot/AppData/Roaming/Foxit Software:rw"
