ARG WINE_ARCH
ARG WINE_VERSION
FROM adamrehn/wine-prefix${WINE_ARCH}:${WINE_VERSION}

# TEMPORARY: patch Winetricks with the correct URLs and SHA256 checksums for the .NET Framework 4.7.2 installation files
COPY ./patch-winetricks.py /tmp/patch-winetricks.py
USER root
RUN python3 /tmp/patch-winetricks.py /usr/bin/winetricks
USER nonroot

# Set our DLL overrides to ensure the .NET Framework libraries are used
ENV WINEDLLOVERRIDES="mscoree=n"

# Install the newest available version of the .NET Framework
RUN xvfb-run -a winetricks --unattended dlls dotnet48 && wineserver --wait
