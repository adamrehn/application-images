FROM adamrehn/common-base:latest

# Install our prerequisites and useful tools
RUN apt-get update && apt-get install -y --no-install-recommends \
		cabextract \
		p7zip \
		winbind \
		xvfb && \
	rm -rf /var/lib/apt/lists/*

# Enable the installation of 32-bit packages
RUN dpkg --add-architecture i386

# Install Wine
RUN curl -fsSL 'https://dl.winehq.org/wine-builds/winehq.key' | apt-key add - && \
	add-apt-repository 'deb https://dl.winehq.org/wine-builds/ubuntu/ focal main' && \
	apt-get update && apt-get install -y --install-recommends winehq-devel && \
	rm -rf /var/lib/apt/lists/*

# Install Winetricks
RUN curl -fsSL 'https://raw.githubusercontent.com/Winetricks/winetricks/master/src/winetricks' -o /usr/bin/winetricks && \
	chmod +x /usr/bin/winetricks

# Copy our helper scripts into the container image and make them all executable
COPY ./scripts/entrypoint.py /usr/bin/entrypoint.py
COPY ./scripts/generate-wrapper.py /usr/bin/generate-wrapper.py
COPY ./scripts/reg-add.py /usr/bin/reg-add.py
COPY ./scripts/wait-for-wineserver.py /usr/bin/wait-for-wineserver.py
RUN chmod +x /usr/bin/entrypoint.py /usr/bin/generate-wrapper.py /usr/bin/reg-add.py /usr/bin/wait-for-wineserver.py

# Create a new Wine prefix for our non-root user
USER nonroot
ENV WINEPREFIX=/home/nonroot/.local/share/wineprefixes/prefix
RUN mkdir -p "$WINEPREFIX"

# Preinstall the 64-bit version of Wine Gecko
RUN curl -fSL 'https://dl.winehq.org/wine/wine-gecko/2.47.2/wine-gecko-2.47.2-x86_64.msi' -o /tmp/wine_gecko-2.47-x86_64.msi && \
	wine64 msiexec /i /tmp/wine_gecko-2.47-x86_64.msi && \
	/usr/bin/wait-for-wineserver.py && \
	rm /tmp/wine_gecko-2.47-x86_64.msi

# Preinstall the 32-bit version of Wine Gecko
RUN curl -fSL 'https://dl.winehq.org/wine/wine-gecko/2.47.2/wine-gecko-2.47.2-x86.msi' -o /tmp/wine-gecko-2.47.2-x86.msi && \
	wine msiexec /i /tmp/wine-gecko-2.47.2-x86.msi && \
	/usr/bin/wait-for-wineserver.py && \
	rm /tmp/wine-gecko-2.47.2-x86.msi

# Set the entrypoint script as the container's default entrypoint
ENTRYPOINT ["/usr/bin/entrypoint.py"]

# Configure docker-shell with the required bind-mounts and environment variables, and enable IPC namespace sharing with the host (which improves X11 performance)
LABEL docker-shell.args.wine-base.1="--ipc=host"
LABEL docker-shell.args.wine-base.2="-e"
LABEL docker-shell.args.wine-base.3="DISPLAY"
LABEL docker-shell.args.wine-base.4="-e"
LABEL docker-shell.args.wine-base.5="WINESCALE"
LABEL docker-shell.mounts.wine-base.1="/tmp/.X11-unix:/tmp/.X11-unix:rw"
LABEL docker-shell.mounts.wine-base.2="~/Desktop:/home/nonroot/Desktop"
LABEL docker-shell.mounts.wine-base.3="~/Documents:/home/nonroot/Documents"
LABEL docker-shell.mounts.wine-base.4="~/Downloads:/home/nonroot/Downloads"
LABEL docker-shell.mounts.wine-base.5="~/Music:/home/nonroot/Music"
LABEL docker-shell.mounts.wine-base.6="~/Pictures:/home/nonroot/Pictures"
LABEL docker-shell.mounts.wine-base.7="~/Videos:/home/nonroot/Videos"
LABEL docker-shell.mounts.wine-base.8="/:/host"
