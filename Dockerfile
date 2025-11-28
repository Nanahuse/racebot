# ==== base image ====
FROM ghcr.io/astral-sh/uv:debian-slim AS base
ENV UV_LINK_MODE=copy
ENV UV_CACHE_DIR=/workspace/.uv_cache/cache
ENV UV_PYTHON_CACHE_DIR=/workspace/.uv_cache/python-cache

WORKDIR /workspace

LABEL org.opencontainers.image.title="racebot" \
    org.opencontainers.image.description="A Discord race countdown bot" \
    org.opencontainers.image.url="https://github.com/Nanahuse/racebot" \
    org.opencontainers.image.source="https://github.com/Nanahuse/racebot" \
    org.opencontainers.image.licenses="GPLv3"

RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# ===================================
# ========== runtime image ==========
# ===================================
FROM base AS runtime

RUN useradd -m appuser
RUN chown -R appuser:appuser /workspace

USER appuser

# Setup uv
COPY pyproject.toml ./
COPY uv.lock ./
RUN uv sync

# Copy application files
COPY sound ./sound
COPY src ./src

CMD ["uv", "run", "src/main.py"]

# ===============================
# ========== dev image ==========
# ===============================
FROM base AS dev

# Install dev tools
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    curl \
    openssh-client \
    && rm -rf /var/lib/apt/lists/*

RUN useradd -m vscode
USER vscode
