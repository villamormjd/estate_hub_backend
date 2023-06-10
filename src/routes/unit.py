from fastapi import APIRouter
from src.models.unit import Unit, UnitAttributes
from src.schemas.unit import unitEntity, unitAttributes
from src.api.unit import UnitManager

unit = APIRouter()
unit_mngr = UnitManager()


@unit.post("/property/{prop_id}/units", tags=["Unit"])
def create_property_unit(prop_id: str, unit: Unit, attrs: UnitAttributes):
    return unit_mngr.create_unit_property(prop_id, unit, attrs)
