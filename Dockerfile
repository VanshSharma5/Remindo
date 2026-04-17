# Stage 1: Build stage
FROM astral/uv:python3.14-bookworm-slim AS builder
WORKDIR /app
COPY pyproject.toml uv.lock ./
# Install dependencies without the project itself to cache this layer
RUN uv sync --frozen --no-install-project

# Stage 2: Final runtime stage
FROM python:3.14-slim
WORKDIR /app
# Copy the virtual environment from the builder stage
COPY --from=builder /app/.venv /app/.venv
ENV PATH="/app/.venv/bin:$PATH"
COPY . .
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
