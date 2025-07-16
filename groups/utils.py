
def serialize_user(user):
    """
    Serializes a User object into a dictionary format.
    """
    return {
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "is_active": user.is_active,
        "date_joined": user.date_joined.isoformat()
    }

def serialize_group(group):
    """
    Serializes a Group object into a dictionary format.
    """
    return {
        "id": group.id,
        "name": group.name,
        "description": group.description,
        "created_by": serialize_user(group.created_by) if group.created_by else None,
        "created_at": group.created_at.isoformat(),
        "updated_at": group.updated_at.isoformat()
    }