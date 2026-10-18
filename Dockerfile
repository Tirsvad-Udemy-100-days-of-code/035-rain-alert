# Rain Alert: a daily WhatsApp alert when rain is expected.
#
# Build and run with Docker Compose (see compose.yaml). The image holds only the
# program; config.env (API key, phone number, Twilio values) is passed at run time
# and is never copied into the image (.dockerignore).
FROM python:3.13-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Time zone data for the alert time; a user without a shell or a home for secrets.
RUN apt-get update \
    && apt-get install -y --no-install-recommends tzdata \
    && rm -rf /var/lib/apt/lists/* \
    && useradd --uid 10001 --no-create-home --shell /usr/sbin/nologin rainalert

WORKDIR /app
COPY pyproject.toml README.md LICENSE ./
COPY src ./src
RUN pip install .

USER rainalert
CMD ["python", "-m", "rain_alert"]
