# 共通ベース
FROM ghcr.io/astral-sh/uv:debian-slim
WORKDIR /workspace

ENV UV_LINK_MODE=copy

# Install Dev tools
RUN apt-get update && apt-get install -y --no-install-recommends \
    git curl openssh-client \
    && rm -rf /var/lib/apt/lists/*

# VSCode remote-user を合わせたい場合
RUN useradd -m vscode && usermod -aG sudo vscode
USER vscode
