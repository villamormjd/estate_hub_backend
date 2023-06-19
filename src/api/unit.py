import datetime

from src.config.constant import Cons, Role
from src.config.db import conn
from bson import ObjectId
from src.utils import *
from src.models.unit import Unit, UnitAttributes
from src.models.users import UserResident
from src.schemas.unit import unitEntity, unitAttributes, unitEntities, userUnitRole, userUnitRoles
from src.api.property import PropertyManager
from src.api.user import AccountManager


class UnitManager:
    def __init__(self):
        self.conn = conn.estatehub
        self.db = self.conn['unit']
        self.unit_attrs_db = self.conn['unit_attributes']
        self.user_unit_role_db = self.conn['user_unit_role']

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

    def add_user_unit_role(self, property_id: str, unit_id: str, user: UserResident):
        try:
            _user = AccountManager().get_user_by_email(user.email)
            if _user["error"]:
                return _user

            uurs = userUnitRoles(self.user_unit_role_db.find({"unit_id": unit_id,
                                                    "user_id": _user["data"]["id"]}))

            if len(uurs) > 0:
                return result_builder("Resident already exists.", is_error=True)

            uur_obj = dict()
            uur_obj["unit_id"] = unit_id
            uur_obj["user_id"] = _user["data"]["id"]
            uur_obj["property_id"] = property_id
            if user.is_homeowner:
                uur_obj["role_id"] = Role.HOMEOWNER.value
            else:
                uur_obj["role_id"] = Role.RELATIVE.value

            uur = self.user_unit_role_db.insert_one(uur_obj)
            results = userUnitRole(self.user_unit_role_db.find_one({"_id": uur.inserted_id}))
            return result_builder("Created", data=results)

        except Exception as e:
            return result_builder(str(e), is_error=True)

    def get_unit_residents(self, propd_id: str, unit_id: str):
        try:
            uurs = userUnitRoles(self.user_unit_role_db.find({"unit_id": unit_id,
                                                              "property_id": propd_id}))

            for uur in uurs:
                uur['user'] = AccountManager().get_user_profile(uur['user_id'])['data']

            return result_builder("Retrieved", data=uurs)

        except Exception as e:
            return result_builder(str(e), is_error=True)
