ARG WINE_ARCH
ARG WINE_VERSION
FROM adamrehn/wine-prefix${WINE_ARCH}:${WINE_VERSION}

# Preinstall Wine Mono
RUN curl -fSL 'https://dl.winehq.org/wine/wine-mono/7.0.0/wine-mono-7.0.0-x86.msi' -o /tmp/wine-mono-x86.msi && \
	xvfb-run -a wine msiexec /i /tmp/wine-mono-x86.msi && \
	wineserver --wait && \
	rm /tmp/wine-mono-x86.msi
