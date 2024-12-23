from sqlalchemy import Column, Text, String, Boolean, INTEGER, DATE, TIME, TIMESTAMP, func
from sqlalchemy.orm import declarative_base, Mapped, mapped_column
from sqlalchemy.dialects.postgresql import VARCHAR
from datetime import date, time, datetime

Base = declarative_base()


class Zapis(Base):
    __tablename__ = "zapis"

    stomatology: Mapped[str] = mapped_column(String, index=True, default="adilstom")
    zapis_id: Mapped[int] = mapped_column(INTEGER, primary_key=True)
    is_active: Mapped[bool] = mapped_column(Boolean(create_constraint=True), default=True)
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP, server_default=func.now())

    phone: Mapped[str] = mapped_column(VARCHAR(19), index=True)
    date: Mapped[date] = mapped_column(DATE)
    time: Mapped[time] = mapped_column(TIME)
    doctor_id: Mapped[int] = mapped_column(INTEGER)
    patient_name: Mapped[str] = mapped_column(String)
    comment: Mapped[str] = mapped_column(String, nullable=True)
    zhaloba: Mapped[str] = mapped_column(String, nullable=True)


class Log(Base):
    __tablename__ = "logs"

    id: Mapped[int] = mapped_column(INTEGER, primary_key=True, index=True, autoincrement=True)
    stomatology: Mapped[str] = mapped_column(VARCHAR(30), index=True, default="adilstom")
    url: Mapped[str] = mapped_column(VARCHAR(100))
    method: Mapped[str] = mapped_column(VARCHAR(6))
    request_body: Mapped[str] = mapped_column(Text, nullable=True)
    response_body: Mapped[str] = mapped_column(Text)
    status_code: Mapped[int] = mapped_column(INTEGER)


class Stomatology(Base):
    __tablename__ = "stomatology"

    name: Mapped[str] = mapped_column(Text, primary_key=True)
    token: Mapped[str] = mapped_column(Text, nullable=False)
