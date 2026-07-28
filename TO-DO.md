# TO-DO

## build(docker)

- The image `CMD` runs `decision-engine run`, whose `main.py` executes Alembic migrations at import with no prior `wait-db`; against a cold PostgreSQL (e.g. a freshly provisioned Render database) this can crash on boot. The `mem` deploy path is unaffected. A `docker-entrypoint.sh` chaining `wait-db → run` (mirroring osint-engine) would close this for the postgresql path.
