from sqlalchemy import Engine, StaticPool, create_engine


def engine_factory(
    database_url: str, check_same_thread: bool = True, staticpool: bool = False
) -> Engine:
    engine = create_engine(
        url=database_url,
        connect_args={"check_same_thread": check_same_thread},
        poolclass=StaticPool if staticpool else None,
    )

    return engine
