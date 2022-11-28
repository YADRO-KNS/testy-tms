__all__ = (
    'get_boolean',
)


def get_boolean(request, key, method='GET'):
    """
    Gets the value from request and returns it's boolean state
    """
    value = getattr(request, method).get(key, False)
    if value.lower() in ["1", "yes", "true"]:
        return True
    return False
