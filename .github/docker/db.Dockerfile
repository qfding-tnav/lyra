# Test-database image for the PGE loop.
#
# postgis/postgis gives the PostGIS extension the Django GIS models need, but it
# does NOT ship pgvector — and the ai_embedding migration runs
# `CREATE EXTENSION vector`, so building the test DB fails without it.
# This image adds pgvector on top so the FULL migration set applies cleanly.
#
# Build context = repo root (only to keep all images consistent):
#   docker build -f .github/docker/db.Dockerfile -t cygnus-test-db .

FROM postgis/postgis:16-3.4

# postgis/postgis is built on the official postgres:16 image (PGDG apt repo present),
# so the matching pgvector package is available as postgresql-16-pgvector.
RUN apt-get update \
    && apt-get install -y --no-install-recommends postgresql-16-pgvector \
    && rm -rf /var/lib/apt/lists/*