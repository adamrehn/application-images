ARG WINE_VERSION
FROM adamrehn/wine-dotnet64:${WINE_VERSION}

# Install DXVK
RUN winetricks --unattended dlls dxvk && wineserver --wait

# Download Rayman Control Panel
RUN curl -fSL 'https://github.com/RayCarrot/RayCarrot.RCP.Metro/releases/download/12.1.0/Rayman.Control.Panel.exe' -o "$WINEPREFIX/drive_c/Rayman.Control.Panel.exe"

# Generate an entrypoint script for Rayman Control Panel, prepending our custom startup logic
COPY --chown=nonroot:nonroot entrypoint-extra-logic.py /tmp/entrypoint-extra-logic.py
RUN generate-application-entrypoint \
	--wine \
	--architecture 64 \
	--application "C:/Rayman.Control.Panel.exe" \
	--configDir "$WINEPREFIX/drive_c/users/nonroot/AppData/Local/Rayman Control Panel" \
	--outfile /tmp/entrypoint-main.py && \
	cat /tmp/entrypoint-extra-logic.py /tmp/entrypoint-main.py > /home/nonroot/raymancontrolpanel.py && \
	chmod +x /home/nonroot/raymancontrolpanel.py

# Set our entrypoint script as the container's entrypoint
ENTRYPOINT ["/home/nonroot/raymancontrolpanel.py"]

# Configure a bind-mount for Rayman Control Panel's persistent configuraton data, and one for the host user's home directory
LABEL docker-shell.mounts.wine-raymancontrolpanel.1="~/.config/Rayman Control Panel:/home/nonroot/.local/share/wineprefixes/prefix/drive_c/users/nonroot/AppData/Local/Rayman Control Panel:rw"
LABEL docker-shell.mounts.wine-raymancontrolpanel.2="\$HOME:/home/hostuser:rw"

# Configure the application name for use when generating a desktop entry
LABEL application-images.name="Rayman Control Panel"
