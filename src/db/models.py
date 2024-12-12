from sqlalchemy import Column, Text, Integer, String
from sqlalchemy.orm import declarative_base, Mapped, mapped_column


Base = declarative_base()


class Zapis(Base):
    __tablename__ = "zapis"

    phone: Mapped[str] = mapped_column(String, primary_key=True)
    date: Mapped[str] = mapped_column(String, primary_key=True)
    zapis_id: Mapped[int] = mapped_column(Integer)


class Log(Base):
    __tablename__ = "logs"

    id = Column(Integer, primary_key=True, index=True)
    request_url = Column(Text, nullable=False)
    request_method = Column(Text, nullable=False)
    request_body = Column(Text, nullable=False)
    response_body = Column(Text, nullable=True)
    response_status = Column(Integer, nullable=False)
