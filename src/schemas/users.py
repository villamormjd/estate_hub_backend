
def userEntity(item) -> dict:
    return {
        "id": str(item['_id']),
        "first_name": item['first_name'],
        "last_name": item['last_name'],
        "email": item['email'],
        "username": item['username'],
        "password": item['password'],
        "is_active": item['is_active'],
        "created_at": item['created_date'],
        "updated_at": item['updated_at'],
        "activated_at": item['activated_at']
    }


def usersEntity(entity) -> list:
    return [userEntity(item) for item in entity]

