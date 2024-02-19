import atexit
import os
import datetime

from sqlalchemy import DateTime, String, create_engine, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker

POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "")
POSTGRES_USER = os.getenv("POSTGRES_USER", "")
POSTGRES_DB = os.getenv("POSTGRES_DB", "ann")
POSTGRES_HOST = os.getenv("POSTGRES_HOST", "127.0.0.1")
POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5432")

PG_DSN = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"

engine = create_engine(PG_DSN)
Session = sessionmaker(bind=engine)

atexit.register(engine.dispose)


class Base(DeclarativeBase):
    pass


class Announcement(Base):
    __tablename__ = "ann"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(
        String(100), index=True, nullable=False
    )
    description: Mapped[str] = mapped_column(String(100), nullable=False)
    create_date: Mapped[datetime.datetime] = mapped_column(
        DateTime, server_default=func.now())
    owner: Mapped[str] = mapped_column(
        String(50), unique=True, index=True, nullable=False
    )

    @property
    def dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'create_date': self.create_date,
            'owner': self.owner
        }


Base.metadata.create_all(bind=engine)
