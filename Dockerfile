FROM python:3.11-slim


ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1


WORKDIR /app


RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    nano \
    && rm -rf /var/lib/apt/lists/*



COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt


COPY ./src /app/src
COPY alembic.ini /app/
COPY migrations /app/migrations
# COPY .env /app/.env # It's generally better to pass sensitive env vars at runtime

# Ensure environment variables for AI assistants are passed or handled
# ARG GEMINI_API_KEY
# ENV GEMINI_API_KEY=${GEMINI_API_KEY}
# ARG OPENAI_API_KEY
# ENV OPENAI_API_KEY=${OPENAI_API_KEY}
# ARG ANTHROPIC_API_KEY
# ENV ANTHROPIC_API_KEY=${ANTHROPIC_API_KEY}

# The .env file will be sourced by docker-compose, so explicit COPY here might be redundant
# if docker-compose handles env_file correctly for the 'web' service.
# However, if building the image standalone and expecting .env to be baked in, then COPY .env is needed.
# For now, assuming docker-compose handles it.

# Set working directory to src for Python imports
WORKDIR /app/src # Setting workdir to src means Python imports will be relative to src

EXPOSE 8000


RUN adduser --disabled-password --gecos '' appuser
USER appuser


CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]