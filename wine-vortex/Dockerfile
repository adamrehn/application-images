ARG WINE_VERSION
FROM adamrehn/wine-dotnet64:${WINE_VERSION}

# Set our DLL overrides to disable libglesv2.dll, which fixes rendering issues when running Electron applications such as Vortex
# (See: <https://gitlab.freedesktop.org/mesa/mesa/-/issues/3683>, <https://bugs.winehq.org/show_bug.cgi?id=44985>, <https://forum.winehq.org/viewtopic.php?t=33878>)
ENV WINEDLLOVERRIDES="${WINEDLLOVERRIDES};libglesv2=d"

# Install the Vortex mod manager
COPY --chown=nonroot:nonroot install-vortex.py /tmp/install-vortex.py
RUN curl -fSL 'https://github.com/Nexus-Mods/Vortex/releases/download/v1.4.16/vortex-setup-1.4.16.exe' -o /tmp/vortex-setup.exe && \
	python3 /tmp/install-vortex.py /tmp/vortex-setup.exe

# Generate an entrypoint script for Vortex, prepending our custom startup logic
COPY --chown=nonroot:nonroot entrypoint-extra-logic.py /tmp/entrypoint-extra-logic.py
RUN generate-application-entrypoint \
	--wine \
	--architecture 64 \
	--application "C:/Program Files/Black Tree Gaming Ltd/Vortex/Vortex.exe" \
	--configDir "/home/hostuser/.config/Vortex" \
	--outfile /tmp/entrypoint-main.py && \
	cat /tmp/entrypoint-extra-logic.py /tmp/entrypoint-main.py > /home/nonroot/vortex.py && \
	chmod +x /home/nonroot/vortex.py

# Set our entrypoint script as the container's entrypoint
ENTRYPOINT ["/home/nonroot/vortex.py"]

# Configure our bind-mounts, symlinks and registry keys to allow Vortex to manage Steam games
# (Note that Vortex relies on hardlinking to deploy mods and this doesn't work across separate bind-mounts, so we expose a single mount here and symlink into it)
LABEL docker-shell.mounts.wine-vortex.1="\$HOME:/home/hostuser:rw"
RUN ln -s /home/hostuser/.config/Vortex "$WINEPREFIX/drive_c/users/nonroot/AppData/Roaming/Vortex"
RUN ln -s /home/hostuser/.local/share/Steam "$WINEPREFIX/drive_c/Program Files (x86)/Steam"
RUN wine-reg-add 'HKCU/Software/Valve/Steam' /v SteamPath /t REG_SZ /d 'C:\Program Files (x86)\Steam' /f

# Configure the application name for use when generating a desktop entry
LABEL application-images.name="Vortex"
