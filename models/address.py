from datetime import datetime

from sqlalchemy import Column, Integer, String, BigInteger, Date
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped

from sqlalchemy_utils import URLType


class Base(DeclarativeBase):
    pass


class AddressUrl(Base):
    __tablename__ = 'address_url'

    point_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    clean_url: Mapped[str] = mapped_column(URLType)
    city: Mapped[str] = mapped_column(String)
    slug: Mapped[str] = mapped_column(String)


class Address(Base):
    __tablename__ = 'addresses'

    id: Mapped[int] = Column(Integer, primary_key=True, autoincrement=True)
    code: Mapped[str] = mapped_column(String, nullable=True)
    chicago_code: Mapped[int] = mapped_column(BigInteger, nullable=True)
    point_id: Mapped[str] = mapped_column(String, nullable=True)
    name: Mapped[str] = mapped_column(String)
    ya_name: Mapped[str] = mapped_column(String, nullable=True)
    category: Mapped[str] = mapped_column(String)
    address: Mapped[str] = mapped_column(String)
    full_address: Mapped[str] = mapped_column(String)
    phone: Mapped[str] = mapped_column(String, nullable=True)
    email: Mapped[str] = mapped_column(String, nullable=True)
    type: Mapped[str] = mapped_column(String, nullable=True)
    department: Mapped[str] = mapped_column(String, nullable=True)
    request_address: Mapped[str] = mapped_column(String)
    country_code: Mapped[str] = mapped_column(String(10), nullable=True)
    formatted: Mapped[str] = mapped_column(String)
    zip_code: Mapped[str] = mapped_column(String, nullable=True)
    country: Mapped[str] = mapped_column(String, nullable=True)
    province: Mapped[str] = mapped_column(String, nullable=True)
    area: Mapped[str] = mapped_column(String, nullable=True)
    city: Mapped[str] = mapped_column(String, nullable=True)
    street: Mapped[str] = mapped_column(String, nullable=True)
    house_number: Mapped[str] = mapped_column(String, nullable=True)
    latitude: Mapped[str] = mapped_column(String, nullable=True)
    longitude: Mapped[str] = mapped_column(String, nullable=True)
    source_url: Mapped[str] = mapped_column(String, nullable=True)


class ResponseCount(Base):
    __tablename__ = "response_count"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    date: Mapped[datetime] = mapped_column(Date)
    count: Mapped[int] = mapped_column(Integer, default=0)


metadata = Base.metadata
