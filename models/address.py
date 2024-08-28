from sqlalchemy import Column, Integer, String, BigInteger
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

    id: Mapped[int] = Column(Integer, primary_key=True)
    code: Mapped[str] = mapped_column(String)
    chicago_code: Mapped[int] = mapped_column(BigInteger)
    name: Mapped[str] = mapped_column(String)
    ya_name: Mapped[str] = mapped_column(String)
    category: Mapped[str] = mapped_column(String)
    address: Mapped[str] = mapped_column(String)
    full_address: Mapped[str] = mapped_column(String)
    phone: Mapped[str] = mapped_column(String)
    email: Mapped[str] = mapped_column(String)
    type: Mapped[str] = mapped_column(String)
    department: Mapped[str] = mapped_column(String)
    request_address: Mapped[str] = mapped_column(String)
    country_code: Mapped[str] = mapped_column(String(10))
    formatted: Mapped[str] = mapped_column(String)
    zip_code: Mapped[str] = mapped_column(String)
    country: Mapped[str] = mapped_column(String)
    province1: Mapped[str] = mapped_column(String)
    province2: Mapped[str] = mapped_column(String)
    city: Mapped[str] = mapped_column(String)
    street: Mapped[str] = mapped_column(String)
    house_number: Mapped[str] = mapped_column(String)
    latitude: Mapped[str] = mapped_column(String)
    longitude: Mapped[str] = mapped_column(String)


metadata = Base.metadata
