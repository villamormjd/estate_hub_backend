
def userEntity(item) -> dict:
    return {
        "id": str(item['_id']),
        "first_name": item['first_name'],
        "last_name": item['last_name'],
        "email": item['email'],
        "username": item['username'],
        "is_active": item['is_active'],
        "created_at": item['created_date'],
        "updated_at": item['updated_at'],
        "activated_at": item['activated_at']
    }


def userLogin(item) -> dict:
    return {
        "username": item['username'],
        "password": item['password'],
        "is_active": item['is_active'],
    }


def userLoginEntities(entity) -> list:
    return [userLogin(item) for item in entity]


def usersEntity(entity) -> list:
    return [userEntity(item) for item in entity]


def userProfileEntity(item) -> dict:
    print(item)
    return {
        "id": str(item['_id']),
        "user_id": item["user_id"],
        "opaque_id": item["opaque_id"],
        "cell_phone_num": item["cell_phone_num"],
        "created_at": item["created_date"],
        "updated_at": item["updated_at"]
    }