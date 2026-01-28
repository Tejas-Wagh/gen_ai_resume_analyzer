# STAGE 1: Builder
FROM python:3.13-slim AS builder

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Set working directory
WORKDIR /app

# Install dependencies (using cache for speed)
ENV UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --frozen --no-install-project --no-dev

# Copy the rest of the code and sync project
COPY . .
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev


# STAGE 2: Runtime
FROM python:3.13-slim AS runtime

WORKDIR /app

# 1. Copy the virtual environment from the builder stage
COPY --from=builder /app/.venv /app/.venv

# 2. Copy the application source code from the builder stage
COPY --from=builder /app /app

# Set environment variables
ENV PATH="/app/.venv/bin:$PATH"
ENV PYTHONUNBUFFERED=1

# Expose the port
EXPOSE 8000

# Run the app
# Note: If main.py is in a folder named 'src' or 'app', change the path below
CMD ["fastapi", "run", "main.py", "--port", "8000", "--host", "0.0.0.0"]