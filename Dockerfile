FROM ghcr.io/astral-sh/uv:python3.12-trixie-slim

WORKDIR /app

VOLUME [ "/data" ]
ENV POKI_DATA_DIR="/data"

COPY ./pyproject.toml .
COPY ./uv.lock .

RUN uv sync --locked

COPY ./poki ./poki

EXPOSE 8000

CMD [ "uv", "run", "uvicorn", "poki:app", "--host", "0.0.0.0" ]