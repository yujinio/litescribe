# --- Builder stage ---
    FROM python:3.12 as builder

    RUN pip install --no-cache poetry

    WORKDIR /backend/worker

    ENV PYTHONUNBUFFERED=1 \
        PYTHONDONTWRITEBYTECODE=1 \
        PYTHONFAULTHANDLER=1 \
        POETRY_NO_INTERACTION=1 \
        POETRY_VIRTUALENVS_IN_PROJECT=1 \
        POETRY_VIRTUALENVS_CREATE=1 \
        POETRY_CACHE_DIR=/tmp/poetry_cache

    COPY pyproject.toml poetry.lock ./
    COPY ./src/litescriber_worker ./src/litescriber_worker
    COPY ./src/litescriber_shared ./src/litescriber_shared

    RUN --mount=type=cache,target=$POETRY_CACHE_DIR poetry install --only main --no-root

    # --- Runtime stage ---
    FROM python:3.12-slim as runtime

    ENV VIRTUAL_ENV=/backend/worker/src/litescriber_worker/.venv \
        PATH="/backend/worker/src/litescriber_worker/.venv/bin:$PATH"

    RUN useradd -u 1000 backend

    COPY --chown=1000 --from=builder ${VIRTUAL_ENV} ${VIRTUAL_ENV}
    COPY --chown=1000 ./src/litescriber_worker /backend/worker/src/litescriber_worker
    COPY --chown=1000 ./src/litescriber_shared /backend/worker/src/litescriber_shared
    RUN mkdir /data && chown -R 1000:1000 /data

    USER 1000

    WORKDIR /backend/worker/src/litescriber_worker

    CMD [ "python", "-m", "litescriber_worker" ]
