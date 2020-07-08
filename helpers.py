import uuid


def generate_slug(length=6):
    return str(uuid.uuid4())[:length]
