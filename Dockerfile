# ==== base image ====
FROM ghcr.io/astral-sh/uv:debian-slim AS base
ENV UV_LINK_MODE=copy

RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# ==== runtime image ====
FROM base AS runtime
COPY . /workspace
WORKDIR /workspace
CMD ["uv","run", "src/main.py"]

# ==== dev image ====
FROM base AS dev
WORKDIR /workspace
RUN apt-get update && apt-get install -y --no-install-recommends \
    git curl openssh-client \
    && rm -rf /var/lib/apt/lists/*

RUN useradd -m vscode && usermod -aG sudo vscode
USER vscode
