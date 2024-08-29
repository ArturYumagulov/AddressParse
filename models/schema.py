from pydantic import BaseModel


class AddressUrlSchema(BaseModel):

    point_id: int
    clean_url: str
    city: str
    city_slug: str


class AddressSchema(BaseModel):
    code: str
    chicago_code: int
    name: str
    ya_name: str
    category: str
    address: str
    full_address: str
    phone: str | None
    email: str | None
    type: str | None
    department: str | None
    request_address: str
    country_code: str
    formatted: str
    zip_code: str
    country: str
    province: str
    area: str
    city: str
    street: str
    house_number: str
    latitude: str
    longitude: str
