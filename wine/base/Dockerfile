FROM adamrehn/application-image-base:latest

# Install our prerequisites and useful tools
RUN --mount=type=cache,target=/var/cache/apt --mount=type=cache,target=/var/lib/apt \
	apt-get update && apt-get install -y --no-install-recommends \
		cabextract \
		p7zip \
		unzip \
		winbind \
		xvfb

# Enable the installation of 32-bit packages
RUN dpkg --add-architecture i386

# Install Wine
ARG WINE_VERSION
RUN --mount=type=cache,target=/var/cache/apt --mount=type=cache,target=/var/lib/apt \
	curl -fsSL 'https://dl.winehq.org/wine-builds/winehq.key' | apt-key add - && \
	add-apt-repository 'deb https://dl.winehq.org/wine-builds/ubuntu/ jammy main' && \
	apt-get update && apt-get install -y --install-recommends \
		winehq-devel=${WINE_VERSION}~jammy-1 \
		wine-devel=${WINE_VERSION}~jammy-1 \
		wine-devel-amd64=${WINE_VERSION}~jammy-1 \
		wine-devel-i386=${WINE_VERSION}~jammy-1

# Install Winetricks
ARG WINETRICKS_VERSION
RUN curl -fsSL "https://raw.githubusercontent.com/Winetricks/winetricks/${WINETRICKS_VERSION}/src/winetricks" -o /usr/bin/winetricks && \
	chmod +x /usr/bin/winetricks

# Configure the PulseAudio client to connect to the host system's server using a bind-mounted UNIX socket
# (Note that the relevant 32-bit or 64-bit PulseAudio packages are installed in the relevant Dockerfile for that prefix type)
COPY pulseaudio-client.conf /etc/pulse/client.conf

# Configure docker-shell with the required bind-mounts and environment variables, and enable shared memory and IPC namespace sharing with the host (which improves PulseAudio and X11 performance)
LABEL docker-shell.args.wine-base.1="--ipc=host"
LABEL docker-shell.args.wine-base.2="-e"
LABEL docker-shell.args.wine-base.3="DISPLAY"
LABEL docker-shell.args.wine-base.4="-e"
LABEL docker-shell.args.wine-base.5="WINESCALE"
LABEL docker-shell.mounts.wine-base.1="/dev/shm:/dev/shm"
LABEL docker-shell.mounts.wine-base.2="/tmp/.X11-unix:/tmp/.X11-unix:rw"
LABEL docker-shell.mounts.wine-base.3="\$XDG_RUNTIME_DIR/pulse:/run/user/1000/pulse"
LABEL docker-shell.mounts.wine-base.4="~/Desktop:/home/nonroot/Desktop"
LABEL docker-shell.mounts.wine-base.5="~/Documents:/home/nonroot/Documents"
LABEL docker-shell.mounts.wine-base.6="~/Downloads:/home/nonroot/Downloads"
LABEL docker-shell.mounts.wine-base.7="~/Music:/home/nonroot/Music"
LABEL docker-shell.mounts.wine-base.8="~/Pictures:/home/nonroot/Pictures"
LABEL docker-shell.mounts.wine-base.9="~/Videos:/home/nonroot/Videos"
LABEL docker-shell.mounts.wine-base.10="/:/host"
