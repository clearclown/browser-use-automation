# IEEE Paper Search Tool Container
# Based on browser-use with IEEE Xplore integration

FROM python:3.12-slim

# Install system dependencies for Chromium and browser automation
RUN apt-get update && apt-get install -y \
	chromium \
	chromium-driver \
	curl \
	git \
	&& rm -rf /var/lib/apt/lists/*

# Install uv package manager
RUN curl -LsSf https://astral.sh/uv/install.sh | sh
ENV PATH="/root/.local/bin:$PATH"

# Set working directory
WORKDIR /app

# Copy project files
COPY pyproject.toml uv.lock ./
COPY browser_use ./browser_use
COPY README.md ./

# Install dependencies
RUN uv sync

# Set environment variables for browser
ENV CHROME_BIN=/usr/bin/chromium
ENV CHROME_PATH=/usr/bin/chromium

# Default command: run Python shell with browser-use available
CMD ["uv", "run", "python"]
