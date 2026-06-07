FROM python:3.12-slim

WORKDIR /app

COPY pyproject.toml LICENSE README.md ./
COPY src/ ./src

RUN pip install --no-cache-dir .

ENTRYPOINT ["t2s"]