ARG WINE_VERSION
FROM adamrehn/wine-dotnet32:${WINE_VERSION}

# Install Foxit PDF Reader
# (Note that the installer requires GUI support even in silent mode, so we create a temporary virtual display with Xvfb)
RUN curl -fSL 'https://cdn06.foxitsoftware.com/product/reader/desktop/win/11.1.0/FoxitPDFReader111_L10N_Setup_Prom.exe' -o /tmp/foxit-installer.exe && \
	xvfb-run -a wine /tmp/foxit-installer.exe /verysilent /MERGETASKS='!desktopicon,!startmenufolder,!quicklaunchicon,!setdefaultreader,!setcollectdata,!displayinbrowser' /COMPONENTS='*pdfviewer,!ffse,!ffaddin,!ffspellcheck' && \
	wineserver --wait

# Prevent the host system's window manager from decorating Foxit Reader's windows, since this interferes with the custom window decorations
RUN wine-reg-add 'HKCU/Software/Wine/AppDefaults/FoxitPDFReader.exe/X11 Driver' /v Decorated /t REG_SZ /d 'N' /f

# Generate an entrypoint script for Foxit Reader
RUN generate-application-entrypoint \
	--wine \
	--architecture 32 \
	--application "C:/Program Files/Foxit Software/Foxit PDF Reader/FoxitPDFReader.exe" \
	--configDir "$WINEPREFIX/drive_c/users/nonroot/AppData/Roaming/Foxit Software" \
	--outfile /home/nonroot/foxitreader.py

# Set our entrypoint script as the container's entrypoint
ENTRYPOINT ["/home/nonroot/foxitreader.py"]

# Configure a bind-mount for Foxit Reader's persistent configuraton data
LABEL docker-shell.mounts.wine-foxitreader.1="~/.config/FoxitReader:/home/nonroot/.local/share/wineprefixes/prefix/drive_c/users/nonroot/AppData/Roaming/Foxit Software:rw"

# Configure the application name for use when generating a desktop entry
LABEL application-images.name="Foxit PDF Reader"
