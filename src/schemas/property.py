

def propertyEntity(item) -> dict:
    return {
        "id": str(item['_id']),
        "property_name": item['property_name'],
        "opaque_id": item['opaque_id'],
        "is_active": item['is_active'],
        "created_at": item['created_at'],
        "updated_at": item['updated_at']
    }


def propertyEntities(entity) -> list:
    return [propertyEntity(item) for item in entity]


def propertyAttributes(item) -> dict():
    return {
        "id": str(item['_id']),
        "property_id": item['property_id'],
        "address1": item['address1'],
        "city": item['city'],
        "state": item['state'],
        "zip": item['zip'],
        "created_at": item['created_at'],
        "updated_at": item['updated_at']
    }