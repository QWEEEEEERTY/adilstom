from sqlalchemy import Column, Text, Integer, String
from sqlalchemy.orm import declarative_base, Mapped, mapped_column
from sqlalchemy.dialects.postgresql import VARCHAR

Base = declarative_base()


class Zapis(Base):
    __tablename__ = "zapis"

    phone: Mapped[str] = mapped_column(String, primary_key=True)
    date: Mapped[str] = mapped_column(String, primary_key=True)
    stomatology: Mapped[str] = mapped_column(String, default="adilstom")
    zapis_id: Mapped[int] = mapped_column(Integer)
    is_active: Mapped[bool] = mapped_column(default=True)


class Log(Base):
    __tablename__ = "logs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)
    stomatology: Mapped[str] = mapped_column(VARCHAR(30), index=True, default="adilstom")
    url: Mapped[str] = mapped_column(VARCHAR(100))
    method: Mapped[str] = mapped_column(VARCHAR(6))
    request_body: Mapped[str] = mapped_column(Text, nullable=True)
    response_body: Mapped[str] = mapped_column(Text)
    status_code: Mapped[int] = mapped_column(Integer)


class Stomatology(Base):
    __tablename__ = "stomatology"

    name: Mapped[str] = mapped_column(Text, primary_key=True)
    token: Mapped[str] = mapped_column(Text, nullable=False)
