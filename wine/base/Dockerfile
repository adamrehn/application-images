FROM adamrehn/common-base:latest

# Install our prerequisites and useful tools
RUN --mount=type=cache,target=/var/cache/apt --mount=type=cache,target=/var/lib/apt \
	apt-get update && apt-get install -y --no-install-recommends \
		cabextract \
		p7zip \
		winbind \
		xvfb

# Enable the installation of 32-bit packages
RUN dpkg --add-architecture i386

# Install Wine
ARG WINE_VERSION
RUN --mount=type=cache,target=/var/cache/apt --mount=type=cache,target=/var/lib/apt \
	curl -fsSL 'https://dl.winehq.org/wine-builds/winehq.key' | apt-key add - && \
	add-apt-repository 'deb https://dl.winehq.org/wine-builds/ubuntu/ focal main' && \
	apt-get update && apt-get install -y --install-recommends \
		winehq-devel=${WINE_VERSION}~focal-1 \
		wine-devel=${WINE_VERSION}~focal-1 \
		wine-devel-amd64=${WINE_VERSION}~focal-1 \
		wine-devel-i386=${WINE_VERSION}~focal-1

# Install Winetricks
ARG WINETRICKS_VERSION
RUN curl -fsSL "https://raw.githubusercontent.com/Winetricks/winetricks/${WINETRICKS_VERSION}/src/winetricks" -o /usr/bin/winetricks && \
	chmod +x /usr/bin/winetricks

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
