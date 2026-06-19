FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim

WORKDIR /app

COPY pyproject.toml uv.lock ./
RUN uv sync --no-dev --frozen --no-install-project

COPY src/ ./src/
COPY alembic/ ./alembic/
COPY alembic.ini ./

RUN uv sync --no-dev --frozen

ENV PATH="/app/.venv/bin:$PATH"

EXPOSE 8000

CMD ["decision-engine", "run"]
