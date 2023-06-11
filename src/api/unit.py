import datetime

from src.config.constant import Cons, Role
from src.config.db import conn
from bson import ObjectId
from src.utils import *
from src.models.unit import Unit, UnitAttributes
from src.schemas.unit import unitEntity, unitAttributes, unitEntities
from src.api.property import PropertyManager


class UnitManager:
    def __init__(self):
        self.conn = conn.estatehub
        self.db = self.conn['unit']
        self.unit_attrs_db = self.conn['unit_attributes']

    def create_unit_property(self, prop_id: str, unit: Unit, attrs: UnitAttributes):
        try:
            q = unitEntities(self.db.find({"name": unit.name}))
            if len(q) > 0:
                return result_builder("Unit already exists.", is_error=True)

            property = PropertyManager().get_property_by_id(prop_id)
            unit_obj = dict(unit)
            unit_obj["opaque_id"] = generate_opaque_id()
            unit_obj["property_id"] = property["id"]
            unit_obj["created_at"] = datetime.datetime.utcnow()
            unit_obj["updated_at"] = datetime.datetime.utcnow()
            unit_obj["is_active"] = True

            unit = self.db.insert_one(unit_obj)
            unit_result = unitEntity(self.db.find_one({"_id": unit.inserted_id}))
            unit_result["attributes"] = self.create_unit_attributes(unit_result["id"], attrs)

            return result_builder("Unit Created", data=unit_result)
        except Exception as e:
            return result_builder(str(e), is_error=True)

    def get_property_units(self, property_id: str):
        try:
            units = self.db.find({"property_id": property_id})
            results = unitEntities(units)

            return result_builder("Units retrieved", data=results)

        except Exception as e:
            return result_builder(str(e), is_error=True)

    def get_unit_by_id(self, property_id: str, unit_id: str):
        try:
            prop = PropertyManager().get_property_by_id(property_id)
            unit = unitEntity(self.db.find_one({"property_id": prop["id"], "_id": ObjectId(unit_id)}))
            unit["attributes"] = self.get_unit_attributes(unit["id"])

            return result_builder("Unit retrieved", data=unit)

        except Exception as e:
            return result_builder(str(e), is_error=True)

    def create_unit_attributes(self, unit_id: str, attrs: UnitAttributes):
        try:
            attrs_obj = dict(attrs)
            attrs_obj["unit_id"] = unit_id
            attrs_obj["created_at"] = datetime.datetime.utcnow()
            attrs_obj["updated_at"] = datetime.datetime.utcnow()

            attrs = self.unit_attrs_db.insert_one(attrs_obj)
            attrs_results = unitAttributes(self.unit_attrs_db.find_one({"_id": attrs.inserted_id}))
            return attrs_results

        except Exception as e:
            return result_builder(str(e), is_error=True)

    def get_unit_attributes(self, unit_id: str):
        try:
            attrs = self.unit_attrs_db.find_one({"unit_id": unit_id})
            attrs = unitAttributes(attrs)

            return attrs

        except Exception as e:
            return result_builder(str(e), is_error=True)
