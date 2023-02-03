# Extend a base image with OpenGL support for NVIDIA GPUs
FROM adamrehn/opengl:glvnd-runtime-ubuntu22.04

# Disable interactive prompts during package installation
ENV DEBIAN_FRONTEND=noninteractive

# Install our common prerequisites
RUN rm -f /etc/apt/apt.conf.d/docker-clean; echo 'Binary::apt::APT::Keep-Downloaded-Packages "true";' > /etc/apt/apt.conf.d/keep-cache
RUN --mount=type=cache,target=/var/cache/apt --mount=type=cache,target=/var/lib/apt \
	apt-get update && apt-get install -y --no-install-recommends \
		apt-transport-https \
		ca-certificates \
		curl \
		gnupg-agent \
		libvulkan1 \
		python3 \
		python3-pip \
		software-properties-common \
		sudo \
		tzdata

# Enable Vulkan support for NVIDIA GPUs
RUN VULKAN_API_VERSION=`dpkg -s libvulkan1 | grep -oP 'Version: [0-9|\.]+' | grep -oP '[0-9|\.]+'` && \
	mkdir -p /etc/vulkan/icd.d/ && \
	echo \
	"{\
		\"file_format_version\" : \"1.0.0\",\
		\"ICD\": {\
			\"library_path\": \"libGLX_nvidia.so.0\",\
			\"api_version\" : \"${VULKAN_API_VERSION}\"\
		}\
	}" > /etc/vulkan/icd.d/nvidia_icd.json

# Install the Python package with our helper functionality and tools
COPY helpers /tmp/helpers
RUN pip3 install /tmp/helpers

# Disable the default "lecture" message the first time a user runs a command using sudo
RUN echo 'Defaults lecture="never"' >> /etc/sudoers

# Create a non-root user with no password and allow them to run commands using sudo
RUN useradd --create-home --home /home/nonroot --shell /bin/bash --uid 1000 nonroot && \
	passwd -d nonroot && \
	usermod -a -G sudo nonroot
