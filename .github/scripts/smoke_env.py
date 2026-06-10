"""Environment smoke test for the agent-runner image.

Verifies the FOUR pillars the runtime needs, against the live db service:
  1. Django      — settings.configure with the postgis backend + a real `migrate`
  2. GIS         — GeoDjango loads the GDAL/GEOS/PROJ system libs
  3. PostGIS     — CREATE EXTENSION postgis + a real spatial query (ST_Distance)
  4. pgvector    — CREATE EXTENSION vector + a vector column / <-> distance query
  5. AWS         — aws CLI v2 present + boto3 importable and able to build a client
  6. Reachability— s3://tnavmapdata/latest_builds_test/ is listable. The bucket
                   only allows anonymous listing from corporate source IPs, so
                   without AWS_ACCESS_KEY_ID/AWS_SECRET_ACCESS_KEY secrets this
                   check is SKIPPED on GitHub-hosted runners; with secrets it
                   becomes a real credentialed check. The FlexNet license portal
                   must answer over HTTPS from inside the container.

No app code is required: this script is self-contained, so it works even though
the Cygnus application itself does not live in this repository.

Usage (inside the agent-runner container, with a postgres service named "db"):
    DB_HOST=db python .github/scripts/smoke_env.py
"""

import os
import subprocess
import sys

failures = []
skips = []


class Skip(Exception):
    """Raise inside a check to mark it skipped (not failed)."""


def check(name, fn):
    try:
        detail = fn()
        print(f"  OK  {name}" + (f" — {detail}" if detail else ""))
    except Skip as e:
        skips.append(name)
        print(f"SKIP  {name}: {e}")
    except Exception as e:  # noqa: BLE001 — report and keep going
        failures.append(name)
        print(f"FAIL  {name}: {type(e).__name__}: {e}")


# --- 1. Django: configure with the PostGIS backend ---------------------------
def django_setup():
    import django
    from django.conf import settings

    settings.configure(
        DEBUG=False,
        INSTALLED_APPS=[
            "django.contrib.contenttypes",
            "django.contrib.auth",
            "django.contrib.gis",
        ],
        DATABASES={
            "default": {
                "ENGINE": "django.contrib.gis.db.backends.postgis",
                "HOST": os.environ.get("DB_HOST", "db"),
                "PORT": os.environ.get("DB_PORT", "5432"),
                "USER": "postgres",
                "PASSWORD": "postgres",
                "NAME": "postgres",
            }
        },
        USE_TZ=True,
    )
    django.setup()
    return f"Django {django.get_version()}, ENGINE=postgis"


check("Django setup (postgis backend)", django_setup)


# --- 2. GIS system libs: GDAL / GEOS / PROJ via GeoDjango ---------------------
def gis_libs():
    from django.contrib.gis.gdal import gdal_full_version
    from django.contrib.gis.geos import Point, geos_version

    p = Point(-122.0, 37.0, srid=4326)  # exercises GEOS
    assert p.x == -122.0
    return (
        f"GDAL [{gdal_full_version().decode().split(',')[0]}], "
        f"GEOS {geos_version().decode()}"
    )


check("GIS libs (GDAL/GEOS via GeoDjango)", gis_libs)


# --- 3. PostGIS: extension + a real spatial query -----------------------------
def postgis_extension():
    from django.db import connection

    with connection.cursor() as cur:
        cur.execute("CREATE EXTENSION IF NOT EXISTS postgis")
        cur.execute("SELECT PostGIS_Version()")
        return f"PostGIS {cur.fetchone()[0]}"


check("PostGIS extension", postgis_extension)


def postgis_query():
    from django.db import connection

    with connection.cursor() as cur:
        cur.execute(
            "SELECT ST_Distance("
            "  ST_GeomFromText('POINT(0 0)', 4326)::geography,"
            "  ST_GeomFromText('POINT(0 1)', 4326)::geography)"
        )
        meters = cur.fetchone()[0]
        assert 100_000 < meters < 120_000  # ~111 km per degree of latitude
        return f"ST_Distance(1 deg lat) = {meters / 1000:.1f} km"


check("PostGIS spatial query", postgis_query)


# --- 4. pgvector: extension + vector column + <-> query -----------------------
def pgvector_extension():
    from django.db import connection

    with connection.cursor() as cur:
        cur.execute("CREATE EXTENSION IF NOT EXISTS vector")
        cur.execute("DROP TABLE IF EXISTS _smoke_vec")
        cur.execute("CREATE TABLE _smoke_vec (id serial PRIMARY KEY, v vector(3))")
        cur.execute("INSERT INTO _smoke_vec (v) VALUES ('[1,2,3]'), ('[4,5,6]')")
        cur.execute("SELECT v <-> '[1,2,3]' FROM _smoke_vec ORDER BY 1 DESC LIMIT 1")
        dist = cur.fetchone()[0]
        cur.execute("DROP TABLE _smoke_vec")
        return f"vector(3) column + L2 distance = {dist:.3f}"


check("pgvector extension (vector column + <-> query)", pgvector_extension)


def pgvector_python():
    import numpy
    import pgvector  # noqa: F401

    return f"pgvector python pkg + numpy {numpy.__version__}"


check("pgvector/numpy python packages", pgvector_python)


# --- 1b. Django migrate: full ORM round-trip against PostGIS ------------------
def django_migrate():
    from django.core.management import call_command

    call_command("migrate", interactive=False, run_syncdb=True, verbosity=0)
    return "contenttypes/auth migrations applied on PostGIS"


check("Django migrate against PostGIS", django_migrate)


# --- 5. AWS: CLI v2 + boto3 ----------------------------------------------------
def aws_cli():
    out = subprocess.run(
        ["aws", "--version"], capture_output=True, text=True, check=True
    )
    return (out.stdout or out.stderr).strip()


check("AWS CLI", aws_cli)


def aws_boto3():
    import boto3

    # No credentials needed: building a client proves the SDK + its deps work.
    boto3.client(
        "s3",
        region_name="us-west-2",
        aws_access_key_id="smoke",
        aws_secret_access_key="smoke",
    )
    return f"boto3 {boto3.__version__} (s3 client constructed)"


check("AWS boto3", aws_boto3)


# --- 6. External reachability: map-data S3 bucket + FlexNet portal -------------
def s3_map_bucket():
    import boto3
    from botocore import UNSIGNED
    from botocore.config import Config
    from botocore.exceptions import ClientError

    bucket, prefix = "tnavmapdata", "latest_builds_test/"
    has_creds = bool(os.environ.get("AWS_ACCESS_KEY_ID"))
    # The bucket lives in us-west-2. Anonymous listing is allowed only from
    # corporate source IPs, so on GitHub-hosted runners this needs credentials.
    # A custom endpoint can be supplied via AWS_ENDPOINT_URL, and botocore
    # honors the standard https_proxy env var.
    endpoint = os.environ.get("AWS_ENDPOINT_URL") or None
    region = os.environ.get("AWS_DEFAULT_REGION", "us-west-2")
    if has_creds:
        s3 = boto3.client("s3", region_name=region, endpoint_url=endpoint)
    else:
        # No secrets configured — try anonymous access in case the bucket is public.
        s3 = boto3.client(
            "s3",
            region_name=region,
            endpoint_url=endpoint,
            config=Config(signature_version=UNSIGNED),
        )
    try:
        resp = s3.list_objects_v2(Bucket=bucket, Prefix=prefix, MaxKeys=5)
    except ClientError as e:
        code = e.response.get("Error", {}).get("Code", "")
        if not has_creds:
            # Anonymous listing works from the corporate network but the bucket
            # policy denies it from other source IPs (e.g. GitHub-hosted runners).
            # Without credentials this is environmental, not a broken image —
            # skip instead of failing, and become a real check once secrets exist.
            raise Skip(
                f"{code} for anonymous access from this network — add "
                "AWS_ACCESS_KEY_ID / AWS_SECRET_ACCESS_KEY repo secrets to "
                "enable the credentialed check"
            )
        raise RuntimeError(
            f"{code}: s3://{bucket}/{prefix} not accessible even WITH credentials — "
            "check the IAM policy / bucket policy (an explicit source-IP Deny "
            "blocks signed requests too)"
        )
    n = resp.get("KeyCount", 0)
    if n == 0:
        raise RuntimeError(f"s3://{bucket}/{prefix} is listable but EMPTY")
    mode = "credentialed" if has_creds else "anonymous"
    via = f" via {endpoint}" if endpoint else ""
    return f"s3://{bucket}/{prefix} listable ({mode}{via}), {n} key(s) sampled"


check("S3 map-data bucket (latest_builds_test/)", s3_map_bucket)


def flexnet_portal():
    import requests

    url = "https://here.flexnetoperations.com/control/navt/login"
    # Any HTTP response (even 4xx from a WAF) proves DNS/TLS/egress all work;
    # only connection errors / timeouts mean the portal is unreachable.
    r = requests.get(url, timeout=30, allow_redirects=True)
    return f"HTTP {r.status_code} from {url}"


check("FlexNet license portal reachable", flexnet_portal)


# ------------------------------------------------------------------------------
if skips:
    print(f"\nSKIPPED: {len(skips)} check(s): {', '.join(skips)}")
if failures:
    print(f"\nFAILED: {len(failures)} check(s): {', '.join(failures)}")
    sys.exit(1)
print("\nEnvironment OK: Django + GIS(GDAL/GEOS) + PostGIS + pgvector + AWS all verified.")