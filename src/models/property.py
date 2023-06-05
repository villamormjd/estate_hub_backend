from pydantic import BaseModel


class Property(BaseModel):
    property_name: str


class PropertyAttributes(BaseModel):
    property_id: str
    address1: str
    city: str
    state: str
    zip: str
