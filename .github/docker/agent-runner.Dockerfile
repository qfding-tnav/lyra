# PGE agent-runner image.
#
# One image shared by BOTH the Generator/Evaluator agents AND the unit-test gate,
# so what an agent runs locally is exactly what the test gate runs (no drift).
#
# Contains:
#   - Python 3.12 + GIS system libs (GDAL/PROJ) + postgres client  -> run Django tests
#   - the app dependency set from artifacts/requirements.txt        -> import the app
#   - Node + Claude Code CLI + git + gh + jq                        -> run the agent loop
#
# The test database is NOT in this image: it is provided at run time by a
# `postgis/postgis` service container (see .github/workflows/agentic.yml).
#
# Build context = repo root:
#   docker build -f .github/docker/agent-runner.Dockerfile -t cygnus-agent-runner .

FROM python:3.12

ENV PYTHONUNBUFFERED=1
ENV TZ="America/Los_Angeles"
ENV DEBIAN_FRONTEND=noninteractive

# --- System deps -----------------------------------------------------------
# GIS libs (binutils/libproj/gdal) are required by django.contrib.gis + PostGIS.
# postgresql-client gives psql for seeding/inspecting the test DB.
RUN apt-get update && apt-get install -y --no-install-recommends \
        binutils libproj-dev gdal-bin \
        postgresql-client \
        git jq curl ca-certificates gnupg unzip \
    && rm -rf /var/lib/apt/lists/*

# --- AWS CLI v2 (matches the production image; boto3 comes from requirements) -
RUN curl -fsSL "https://awscli.amazonaws.com/awscli-exe-linux-$(uname -m).zip" -o /tmp/awscliv2.zip \
    && unzip -q /tmp/awscliv2.zip -d /tmp \
    && /tmp/aws/install \
    && rm -rf /tmp/aws /tmp/awscliv2.zip

# --- Node 20 + Claude Code CLI (the agent loop runs claude -p ...) ----------
RUN curl -fsSL https://deb.nodesource.com/setup_20.x | bash - \
    && apt-get install -y --no-install-recommends nodejs \
    && npm install -g @anthropic-ai/claude-code \
    && rm -rf /var/lib/apt/lists/*

# --- GitHub CLI (the loop posts comments / opens PRs via gh) ----------------
RUN curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg \
        | dd of=/usr/share/keyrings/githubcli-archive-keyring.gpg \
    && chmod go+r /usr/share/keyrings/githubcli-archive-keyring.gpg \
    && echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" \
        > /etc/apt/sources.list.d/github-cli.list \
    && apt-get update && apt-get install -y --no-install-recommends gh \
    && rm -rf /var/lib/apt/lists/*

# --- App dependencies ------------------------------------------------------
# requirements.txt is the single source of truth for app deps.
# If a test reveals a missing import, add the package THERE (not here).
COPY requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt

WORKDIR /workspace