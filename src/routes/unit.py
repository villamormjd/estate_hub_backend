from fastapi import APIRouter, Depends
from src.models.unit import Unit, UnitAttributes
from src.schemas.unit import unitEntity, unitAttributes
from src.api.unit import UnitManager
from src.config.auth import jwtBearer

unit = APIRouter()
unit_mngr = UnitManager()


@unit.post("/property/{prop_id}/units", dependencies=[Depends(jwtBearer())], tags=["Unit"])
def create_property_unit(prop_id: str, unit: Unit, attrs: UnitAttributes):
    return unit_mngr.create_unit_property(prop_id, unit, attrs)


@unit.get("/property/{prop_id}/units", dependencies=[Depends(jwtBearer())], tags=["Unit"])
def retrieve_property_units(property_id: str):
    return unit_mngr.get_property_units(property_id)


@unit.get("/property/{prop_id}/units/{unit_id}", tags=["Unit"])
def retrieve_unit(prop_id: str, unit_id: str):
    return unit_mngr.get_unit_by_id(prop_id, unit_id)