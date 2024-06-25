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
    COPY ./src/litescribe_worker ./src/litescribe_worker
    COPY ./src/litescribe_shared ./src/litescribe_shared

    RUN --mount=type=cache,target=$POETRY_CACHE_DIR poetry install --only main --no-root

    # --- Runtime stage ---
    FROM python:3.12-slim as runtime

    ENV VIRTUAL_ENV=/backend/worker/src/litescribe_worker/.venv \
        PATH="/backend/worker/src/litescribe_worker/.venv/bin:$PATH"

    RUN useradd -u 1000 backend

    COPY --chown=1000 --from=builder ${VIRTUAL_ENV} ${VIRTUAL_ENV}
    COPY --chown=1000 ./src/litescribe_worker /backend/worker/src/litescribe_worker
    COPY --chown=1000 ./src/litescribe_shared /backend/worker/src/litescribe_shared
    RUN mkdir /data && chown -R 1000:1000 /data

    USER 1000

    WORKDIR /backend/worker/src/litescribe_worker

    CMD [ "python", "-m", "litescribe_worker" ]
