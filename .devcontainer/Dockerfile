FROM python:3.12-slim AS base
COPY --from=ghcr.io/astral-sh/uv:0.9 /uv /uvx /bin/
ENV PYTHONUNBUFFERED=1 UV_LINK_MODE=copy


FROM base AS dev

RUN apt-get update \
    && apt-get install -y --no-install-recommends git curl ca-certificates openssh-client \
    && rm -rf /var/lib/apt/lists/*

ARG USERNAME=dev
ARG USER_UID=1000
ARG USER_GID=1000
RUN groupadd --gid ${USER_GID} ${USERNAME} \
    && useradd --uid ${USER_UID} --gid ${USER_GID} --create-home --shell /bin/bash ${USERNAME} \
    && mkdir -p /opt/venv && chown ${USERNAME}:${USERNAME} /opt/venv

ENV UV_PROJECT_ENVIRONMENT=/opt/venv \
    VIRTUAL_ENV=/opt/venv \
    PATH="/opt/venv/bin:${PATH}"

USER ${USERNAME}
CMD ["sleep", "infinity"]


FROM base AS app

ARG SERVICE=client
ARG PORT=4000
ENV SERVICE=${SERVICE} PORT=${PORT}

WORKDIR /app

COPY pyproject.toml uv.lock ./
COPY libs/core-app/pyproject.toml ./libs/core-app/
COPY apps/${SERVICE}/pyproject.toml ./apps/${SERVICE}/

RUN uv sync --frozen --no-cache --no-dev --package ${SERVICE} --no-install-workspace

COPY libs/core-app ./libs/core-app
COPY apps/${SERVICE} ./apps/${SERVICE}

RUN uv sync --frozen --no-cache --no-dev --package ${SERVICE}

EXPOSE ${PORT}

CMD exec uv run --no-sync --package ${SERVICE} python -m ${SERVICE}.main
