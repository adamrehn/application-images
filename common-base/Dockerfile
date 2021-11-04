# Extend a base image with OpenGL support for NVIDIA GPUs
FROM nvidia/opengl:1.2-glvnd-runtime-ubuntu20.04

# Disable interactive prompts during package installation
ENV DEBIAN_FRONTEND=noninteractive

# Install our common prerequisites
RUN apt-get update && apt-get install -y --no-install-recommends \
		apt-transport-https \
		ca-certificates \
		curl \
		gnupg-agent \
		libvulkan1 \
		python3 \
		python3-pip \
		software-properties-common \
		sudo \
		tzdata && \
	rm -rf /var/lib/apt/lists/*

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

# Disable the default "lecture" message the first time a user runs a command using sudo
RUN echo 'Defaults lecture="never"' >> /etc/sudoers

# Create a non-root user with no password and allow them to run commands using sudo
RUN useradd --create-home --home /home/nonroot --shell /bin/bash --uid 1000 nonroot && \
	passwd -d nonroot && \
	usermod -a -G sudo nonroot
