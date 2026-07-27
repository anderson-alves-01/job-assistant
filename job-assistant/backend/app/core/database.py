from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from app.core.settings import settings


class Base(DeclarativeBase):
    """
    Classe base para todos os modelos SQLAlchemy.
    """

    pass


engine = create_engine(
    settings.database_url,
    pool_pre_ping=True,
    echo=False,
)


SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
    expire_on_commit=False,
)


def get_db() -> Generator[Session, None, None]:
    """
    Cria uma sessão de banco para cada requisição.
    """

    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()