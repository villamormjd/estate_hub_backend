from pydantic import BaseModel


class Unit(BaseModel):
    name: str


class UnitAttributes(BaseModel):
    block: str
    lot: str
    phase: str
    street: str
    lot_size: str
