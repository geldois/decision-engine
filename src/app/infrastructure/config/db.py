import os


def build_database_url(
    *,
    db_prefix: str | None = None,
    db_user: str | None = None,
    db_pass: str | None = None,
    db_host: str | None = None,
    db_port: str | None = None,
    db_name: str | None = None,
) -> str:
    db_prefix = db_prefix or os.getenv("DB_PREFIX")
    db_user = db_user or os.getenv("DB_USER")
    db_pass = db_pass or os.getenv("DB_PASS")
    db_host = db_host or os.getenv("DB_HOST")
    db_port = db_port or os.getenv("DB_PORT")
    db_name = db_name or os.getenv("DB_NAME")

    if not all([db_prefix, db_user, db_pass, db_host, db_port, db_name]):
        raise RuntimeError("invalid DB config")

    return f"{db_prefix}://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}"
