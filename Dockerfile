FROM python:3.12-slim-bookworm

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

ADD . /app

WORKDIR /app

RUN uv sync --frozen

COPY ./main.py /code/app/main.py

CMD ["fastapi", "run", "app/main.py", "--port", "80"]