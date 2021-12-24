ARG WINE_VERSION
FROM adamrehn/wine-dotnet64:${WINE_VERSION}

# Set our DLL overrides to disable libglesv2.dll, which fixes rendering issues when running Electron applications such as Vortex
# (See: <https://gitlab.freedesktop.org/mesa/mesa/-/issues/3683>, <https://bugs.winehq.org/show_bug.cgi?id=44985>, <https://forum.winehq.org/viewtopic.php?t=33878>)
ENV WINEDLLOVERRIDES="${WINEDLLOVERRIDES};libglesv2=d"

# TEMPORARY: install the Vortex mod manager from a manually created ZIP file until I figure out how to get the installer to work correctly in a headless environment
COPY --chown=nonroot:nonroot Vortex.zip /tmp/Vortex.zip
RUN unzip /tmp/Vortex.zip -d "$WINEPREFIX/drive_c/Vortex"

# Create a symlink and registry key to ensure Vortex can detect Steam and our games
RUN ln -s ~/.local/share/Steam "$WINEPREFIX/drive_c/Program Files (x86)/Steam"
RUN wine-reg-add 'HKCU/Software/Valve/Steam' /v SteamPath /t REG_SZ /d 'C:\Program Files (x86)\Steam' /f

# Generate an entrypoint script for Vortex, prepending our custom startup logic
COPY --chown=nonroot:nonroot entrypoint-extra-logic.py /tmp/entrypoint-extra-logic.py
RUN generate-application-entrypoint \
	--wine \
	--architecture 64 \
	--application "C:/Vortex/Vortex/Vortex.exe" \
	--configDir "$WINEPREFIX/drive_c/users/nonroot/AppData/Roaming/Vortex" \
	--outfile /tmp/entrypoint-main.py && \
	cat /tmp/entrypoint-extra-logic.py /tmp/entrypoint-main.py > /home/nonroot/vortex.py && \
	chmod +x /home/nonroot/vortex.py

# Set our entrypoint script as the container's entrypoint
ENTRYPOINT ["/home/nonroot/vortex.py"]

# Configure a bind-mount for Vortex's persistent configuraton data
LABEL docker-shell.mounts.wine-vortex.1="~/.config/Vortex:/home/nonroot/.local/share/wineprefixes/prefix/drive_c/users/nonroot/AppData/Roaming/Vortex:rw"

# Bind-mount the user's Steam directory so Vortex can manage Steam games
LABEL docker-shell.mounts.wine-vortex.2="~/.local/share/Steam:/home/nonroot/.local/share/Steam:rw"

# Configure the application name for use when generating a desktop entry
LABEL application-images.name="Vortex"
