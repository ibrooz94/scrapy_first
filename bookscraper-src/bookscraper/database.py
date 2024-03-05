
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, mapped_column, Mapped, sessionmaker
from typing import Optional


Base = declarative_base()

def db_connect():
    return create_engine("sqlite:///chartadata.sqlite3")

def create_table(engine):
    Base.metadata.create_all(engine)

def create_session():
    return sessionmaker(bind=db_connect())


class ChartaData(Base):
    __tablename__ = "chartadata"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    url: Mapped[Optional[str]]
    signatory: Mapped[Optional[str]]
    organizational_size: Mapped[Optional[str]]
    federal_state: Mapped[Optional[str]]
    segment: Mapped[Optional[str]]
    name: Mapped[Optional[str]]
    position: Mapped[Optional[str]]
    street: Mapped[Optional[str]]
    city: Mapped[Optional[str]]
    phone: Mapped[Optional[str]]
    email: Mapped[Optional[str]]
    website: Mapped[Optional[str]] 