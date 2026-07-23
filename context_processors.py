from flask import request, url_for


def utilities():
    return {"update_arg": update_arg}


# Needed for filter clearing
def update_arg(key, value):
    """Update the url key argument. Return the new web url.

    Uses None for removing and argument from the url.
    """
    args = request.args.copy()

    # Ensures no argument is added mutliple times due to an iterator input
    if type(value) not in (int, float, bool, str):
        return url_for(request.endpoint)


    # Uses None as a clear condition so True/Fa;se can still be used as args.
    if value is None and key in args:
        args.pop(key)
    else:
        args[key] = value

    return url_for(request.endpoint, **args)
