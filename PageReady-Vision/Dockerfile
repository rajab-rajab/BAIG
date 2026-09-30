# Build with --platform linux/arm64 when validating the AWS Graviton path.
# This development image deliberately does not claim to contain COOL. Replace
# the OpenCV dependency only after the licensed COOL runtime is verified.
FROM python:3.12-slim

WORKDIR /app
COPY pyproject.toml README.md ./
COPY src ./src

RUN pip install --no-cache-dir .

ENTRYPOINT ["python", "-m", "pageready.cli"]
