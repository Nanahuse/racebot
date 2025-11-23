# 共通ベース
FROM ghcr.io/astral-sh/uv:debian-slim
WORKDIR /workspace

ENV UV_LINK_MODE=copy

# Install Runtime dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Install Dev tools
RUN apt-get update && apt-get install -y --no-install-recommends \
    git curl openssh-client ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# VSCode remote-user を合わせたい場合
RUN useradd -m vscode && usermod -aG sudo vscode
USER vscode
