
def unitEntity(item) -> dict:
    return {
        "id": str(item['_id']),
        "name": item["name"],
        "opaque_id": item['opaque_id'],
        "property_id": item["property_id"],
        "is_active": item['is_active'],
        "created_at": item['created_at'],
        "updated_at": item['updated_at']
    }


def unitEntities(entity):
    return [unitEntity(item) for item in entity]


def unitAttributes(item) -> dict:
    return {
        "id": str(item['_id']),
        "block": item["block"],
        "lot": item["lot"],
        "phase": item["phase"],
        "street": item["street"],
        "lot_size": item["lot_size"],
    }
