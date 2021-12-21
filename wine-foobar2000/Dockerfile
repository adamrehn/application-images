ARG WINE_VERSION
FROM adamrehn/wine-dotnet32:${WINE_VERSION}

# Install foobar2000
RUN curl -fSL 'https://www.foobar2000.org/files/foobar2000_v1.6.8.exe' -o /tmp/foobar2000.exe && \
	xvfb-run -a wine /tmp/foobar2000.exe /S && \
	wineserver --wait

# Install the VIOGSF component for foobar2000
RUN curl -fSL 'http://vgmpf.com/Wiki/images/6/6a/VIOGSF_v0.08.16.zip' -o /tmp/VIOGSF.zip && \
	unzip /tmp/VIOGSF.zip -d /tmp/VIOGSF && \
	cp /tmp/VIOGSF/foo_input_viogsf.dll "$WINEPREFIX/drive_c/Program Files/foobar2000/components/" && \
	cp /tmp/VIOGSF/viogsf.bin "$WINEPREFIX/drive_c/Program Files/foobar2000/components/" && \
	rm -rf /tmp/VIOGSF && \
	rm /tmp/VIOGSF.zip

# Install the VIO2SF component for foobar2000
RUN curl -fSL 'https://www.foobar2000.org/getcomponent/f1ec0447dbace81269f75452f6febd3a/foo_input_vio2sf.fb2k-component' -o /tmp/foo_input_vio2sf.fb2k-component && \
	unzip /tmp/foo_input_vio2sf.fb2k-component -d "$WINEPREFIX/drive_c/Program Files/foobar2000/components/" && \
	rm /tmp/foo_input_vio2sf.fb2k-component

# Install the PSF Decoder component for foobar2000 (note that we use a slightly older version here, since the latest release refuses to play certain input files)
RUN curl -fSL 'http://vgmpf.com/Wiki/images/a/ae/PSF_Decoder_v2.0.38.zip' -o /tmp/PSF_Decoder.zip && \
	unzip /tmp/PSF_Decoder.zip -d /tmp && \
	unzip '/tmp/PSF Decoder v2.0.38.fb2k-component' -d "$WINEPREFIX/drive_c/Program Files/foobar2000/components/" && \
	rm '/tmp/PSF Decoder v2.0.38.fb2k-component' && \
	rm /tmp/PSF_Decoder.zip

# Generate an entrypoint script for foobar2000
RUN generate-application-entrypoint \
	--wine \
	--architecture 32 \
	--application "C:/Program Files/foobar2000/foobar2000.exe" \
	--configDir "$WINEPREFIX/drive_c/users/nonroot/AppData/Roaming/foobar2000" \
	--outfile /home/nonroot/foobar2000.py

# Set our entrypoint script as the container's entrypoint
ENTRYPOINT ["/home/nonroot/foobar2000.py"]

# Configure a bind-mount for foobar2000's persistent configuraton data
LABEL docker-shell.mounts.wine-foobar2000.1="~/.config/foobar2000:/home/nonroot/.local/share/wineprefixes/prefix/drive_c/users/nonroot/AppData/Roaming/foobar2000:rw"

# Configure the application name for use when generating a desktop entry
LABEL application-images.name="foobar2000"
