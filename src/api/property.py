import datetime

from src.config.constant import Cons, Role
from src.config.db import conn
from bson import ObjectId
from src.utils import *
from src.models.property import Property, PropertyAttributes
from src.schemas.property import *
from src.api.user import AccountManager


class PropertyManager:

    def __init__(self):
        self.conn = conn.estatehub
        self.db = self.conn['property']
        self.prop_attrs_db = self.conn['property_attributes']

    def create_property(self, prop: Property):
        try:
            if self.get_property_by_name(prop.property_name):
                return result_builder("Property Already Exists", is_error=True)
            prop_obj = dict(prop)
            prop_obj["opaque_id"] = generate_opaque_id()
            prop_obj["created_at"] = datetime.datetime.utcnow()
            prop_obj["updated_at"] = datetime.datetime.utcnow()
            prop_obj["is_active"] = True
            u = self.db.insert_one(prop_obj)
            result = propertyEntities(self.db.find({"_id": u.inserted_id}))

            return result_builder("Created", data=result)

        except Exception as e:
            return result_builder(str(e), is_error=True)

    def create_property_attributes(self, attrs: PropertyAttributes):

        try:
            prop_obj = dict(attrs)
            prop_obj["created_at"] = datetime.datetime.utcnow()
            prop_obj["updated_at"] = datetime.datetime.utcnow()

            u = self.prop_attrs_db.insert_one(prop_obj)
            results = propertyAttributes(self.prop_attrs_db.find_one({"_id": u.inserted_id}))
            return result_builder("Created", data=results)
        except Exception as e:
            return result_builder(str(e), is_error=True)

    def get_property_attributes(self, id: str):

        try:
            prop = propertyEntity(self.db.find_one({"_id": ObjectId(id)}))
            query = self.prop_attrs_db.find_one({"property_id": id})
            prop["attributes"] = propertyAttributes(query)

            return result_builder("Retrieved", data=prop)
        except Exception as e:
            return result_builder(str(e), is_error=True)

    def get_all_properties(self):
        try:
            props = self.db.find()
            results = propertyEntities(props)
            return result_builder("Retrieved", data=results)

        except Exception as e:
            return result_builder(str(e), is_error=True)

    def get_property_by_name(self, property_name):
        prop = propertyEntities(self.db.find({"property_name": property_name}))

        if len(prop) > 0:
            return True
        return False

    def add_staff_property(self, id: str, email: str):
        user = AccountManager().get_user_by_email(email)
        prop = propertyEntities(self.db.find({"_id": ObjectId(id)}))
        role = Role.STAFF

        results = {"user": user, "property": prop, "role": role}
        return result_builder("Added Successfully", data=results)