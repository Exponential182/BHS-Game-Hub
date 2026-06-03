from flask import request, url_for


def utilities():
    return {"update_arg": update_arg}


def update_arg(key, value):
    args = request.args.copy()

    if value is None and key in args:
        args.pop(key)
    else:
        args[key] = value

    return url_for(request.endpoint, **args)
