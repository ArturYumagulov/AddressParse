from pydantic import BaseModel


class AddressUrlSchema(BaseModel):

    point_id: int
    clean_url: str
    city: str
    city_slug: str
