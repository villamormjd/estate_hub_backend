from fastapi import APIRouter, Depends
from src.models.property import Property, PropertyAttributes
from src.api.property import PropertyManager

prop_mngr = PropertyManager()
prop = APIRouter()


@prop.post("/property", tags=["Properties"])
def add_property(property: Property):
    return prop_mngr.create_property(property)


@prop.post("/property/{id}/add-details", tags=["Properties"])
def add_property_details(id: str, attrs: PropertyAttributes):
    return prop_mngr.create_property_attributes(attrs)


@prop.get("/properties", tags=["Properties"])
def retrieve_properties():
    return prop_mngr.get_all_properties()


@prop.get("/property/{id}/details", tags=["Properties"])
def retrieve_property_details(id: str):
    return prop_mngr.get_property_attributes(id)


@prop.post("/property/{id}/add-staff", tags=["Properties"])
def add_property_staff(id: str, email: str):
    return prop_mngr.add_staff_property(id, email)
