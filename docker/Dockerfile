FROM python

WORKDIR /app

EXPOSE 5000

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

COPY BudgetManager /app/

COPY pyproject.toml uv.lock /app/

RUN uv sync --frozen

CMD ["uv", "run", "app.py"]