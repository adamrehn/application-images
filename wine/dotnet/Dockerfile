FROM adamrehn/wine-base:latest

# TEMPORARY: patch Winetricks with the correct URLs and SHA256 checksums for the .NET Framework 4.7.2 installation files
COPY ./patch-winetricks.py /tmp/patch-winetricks.py
USER root
RUN python3 /tmp/patch-winetricks.py /usr/bin/winetricks
USER nonroot

# Set our DLL overrides to ensure the .NET Framework libraries are used
ENV WINEDLLOVERRIDES="mscoree=n"

# Install .NET Framework 4.0, since it acts as a prerequisite for the subsequent .NET Framework versions
# (See: <https://www.reddit.com/r/wine_gaming/comments/8r6low/guide_how_to_install_net_45_on_64bit_prefixes/>)
RUN winetricks --unattended dlls dotnet40 && /usr/bin/wait-for-wineserver.py

# Install each of the newer versions of the .NET Framework that we want in separate filesystem layers
# (Note that if we wanted these in a single filesystem layer then we could simply install 4.7.2 here and the others would be automatically installed as dependencies)
RUN winetricks --unattended dlls dotnet452 && /usr/bin/wait-for-wineserver.py
RUN winetricks --unattended dlls dotnet46 && /usr/bin/wait-for-wineserver.py
RUN winetricks --unattended dlls dotnet461 && /usr/bin/wait-for-wineserver.py
RUN winetricks --unattended dlls dotnet462 && /usr/bin/wait-for-wineserver.py
RUN winetricks --unattended dlls dotnet472 && /usr/bin/wait-for-wineserver.py
