# syntax=docker/dockerfile:1
# Podman/Docker compatible Containerfile for browser-use with automated research
# Optimized for rootless Podman execution

FROM python:3.12-slim

LABEL name="browser-use-research" \
	maintainer="Research Automation <research@browser-use.com>" \
	description="Automated research system with PRISMA-based literature search" \
	homepage="https://github.com/browser-use/browser-use"

ARG TARGETPLATFORM
ARG TARGETOS
ARG TARGETARCH
ARG TARGETVARIANT

######### Environment Variables #################################

# Global system-level config
ENV TZ=UTC \
	LANGUAGE=en_US:en \
	LC_ALL=C.UTF-8 \
	LANG=C.UTF-8 \
	DEBIAN_FRONTEND=noninteractive \
	APT_KEY_DONT_WARN_ON_DANGEROUS_USAGE=1 \
	PYTHONIOENCODING=UTF-8 \
	PYTHONUNBUFFERED=1 \
	PIP_DISABLE_PIP_VERSION_CHECK=1 \
	UV_LINK_MODE=copy \
	UV_COMPILE_BYTECODE=1 \
	UV_PYTHON_PREFERENCE=only-system \
	npm_config_loglevel=error \
	IN_DOCKER=True

# User config for rootless Podman compatibility
ENV BROWSERUSE_USER="browseruse" \
	DEFAULT_PUID=1000 \
	DEFAULT_PGID=1000

# Paths
ENV CODE_DIR=/app \
	DATA_DIR=/data \
	VENV_DIR=/app/.venv \
	PATH="/app/.venv/bin:$PATH"

# Browser config
ENV CHROME_BIN=/usr/bin/chromium \
	CHROME_PATH=/usr/bin/chromium \
	DISPLAY=:99

# Build shell config
SHELL ["/bin/bash", "-o", "pipefail", "-o", "errexit", "-o", "errtrace", "-o", "nounset", "-c"]

# Force apt to leave downloaded binaries in /var/cache/apt
RUN echo 'Binary::apt::APT::Keep-Downloaded-Packages "1";' > /etc/apt/apt.conf.d/99keep-cache \
	&& echo 'APT::Install-Recommends "0";' > /etc/apt/apt.conf.d/99no-intall-recommends \
	&& echo 'APT::Install-Suggests "0";' > /etc/apt/apt.conf.d/99no-intall-suggests \
	&& rm -f /etc/apt/apt.conf.d/docker-clean

# Create non-privileged user for browseruse and chrome (Podman rootless compatible)
RUN echo "[*] Setting up $BROWSERUSE_USER user uid=${DEFAULT_PUID}..." \
	&& groupadd --system --gid "$DEFAULT_PGID" "$BROWSERUSE_USER" \
	&& useradd --system --create-home --uid "$DEFAULT_PUID" --gid "$BROWSERUSE_USER" --groups audio,video "$BROWSERUSE_USER" \
	&& mkdir -p /data /app \
	&& mkdir -p /home/$BROWSERUSE_USER/.config \
	&& chown -R $BROWSERUSE_USER:$BROWSERUSE_USER /home/$BROWSERUSE_USER /data /app

# Install base apt dependencies
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked,id=apt-$TARGETARCH$TARGETVARIANT \
	echo "[+] Installing APT base system dependencies for $TARGETPLATFORM..." \
	&& mkdir -p /etc/apt/keyrings \
	&& apt-get update -qq \
	&& apt-get install -qq -y --no-install-recommends \
		# 1. packaging dependencies
		apt-transport-https ca-certificates apt-utils gnupg2 unzip curl wget grep \
		# 2. CLI helpers for debugging
		nano iputils-ping dnsutils jq git \
	&& rm -rf /var/lib/apt/lists/*

# Copy uv binary
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Copy only dependency manifest
WORKDIR /app
COPY --chown=$BROWSERUSE_USER:$BROWSERUSE_USER pyproject.toml uv.lock* /app/

# Setup venv as the browseruse user
USER "$BROWSERUSE_USER"

RUN --mount=type=cache,target=/home/$BROWSERUSE_USER/.cache,sharing=locked,id=cache-$TARGETARCH$TARGETVARIANT,uid=$DEFAULT_PUID,gid=$DEFAULT_PGID \
	echo "[+] Setting up venv using uv in $VENV_DIR..." \
	&& uv venv \
	&& which python | grep "$VENV_DIR" \
	&& python --version

# Switch back to root to install chromium
USER root

# Install Chromium browser directly from system packages
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked,id=apt-$TARGETARCH$TARGETVARIANT \
	echo "[+] Installing chromium browser from system packages..." \
	&& apt-get update -qq \
	&& apt-get install -y --no-install-recommends \
		chromium \
		fonts-unifont \
		fonts-liberation \
		fonts-dejavu-core \
		fonts-freefont-ttf \
		fonts-noto-core \
		xvfb \
	&& rm -rf /var/lib/apt/lists/* \
	&& ln -s /usr/bin/chromium /usr/bin/chromium-browser \
	&& ln -s /usr/bin/chromium /app/chromium-browser \
	&& mkdir -p "/home/${BROWSERUSE_USER}/.config/chromium/Crash Reports/pending/" \
	&& chown -R "$BROWSERUSE_USER:$BROWSERUSE_USER" "/home/${BROWSERUSE_USER}/.config"

# Switch back to browseruse user for Python package installation
USER "$BROWSERUSE_USER"

RUN --mount=type=cache,target=/home/$BROWSERUSE_USER/.cache,sharing=locked,id=cache-$TARGETARCH$TARGETVARIANT,uid=$DEFAULT_PUID,gid=$DEFAULT_PGID \
	echo "[+] Installing browser-use pip sub-dependencies..." \
	&& uv sync --all-extras --no-dev --no-install-project

# Copy the rest of the browser-use codebase
COPY --chown=$BROWSERUSE_USER:$BROWSERUSE_USER . /app

# Install the browser-use package and all of its optional dependencies
RUN --mount=type=cache,target=/home/$BROWSERUSE_USER/.cache,sharing=locked,id=cache-$TARGETARCH$TARGETVARIANT,uid=$DEFAULT_PUID,gid=$DEFAULT_PGID \
	echo "[+] Installing browser-use pip library from source..." \
	&& uv sync --all-extras --locked --no-dev \
	&& python -c "import browser_use; print('browser-use installed successfully')"

# Create necessary directories with proper permissions
RUN mkdir -p "$DATA_DIR/profiles/default" \
	&& mkdir -p /app/automated_research/data \
	&& mkdir -p /app/automated_research/reports \
	&& mkdir -p /app/automated_research/logs \
	&& mkdir -p /app/papers

VOLUME "$DATA_DIR"
VOLUME "/app/papers"
VOLUME "/app/automated_research"

EXPOSE 9242
EXPOSE 9222

WORKDIR /app

# Default command runs the automated research system
# Override with: podman run -it <image> bash
ENTRYPOINT ["python", "-m", "automated_research.main"]
CMD ["--headless"]
