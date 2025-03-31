from datetime import datetime, timedelta, timezone
from flask import jsonify

def json_respond(data, message="Success", token=None):
    res = jsonify(
        {"isBase64Encoded": False, "statusCode": 200, "body": message, "data": data}
    )
    res.status = "200 %s" % message
    res.message = message

    if token:
        expires = datetime.now(timezone.utc) + timedelta(days=30)
        res.headers[
            "Set-Cookie"
        ] = "token=%s; expires=%s; path=/; samesite=None" % (
            token,
            expires.strftime("%a, %d %b %Y %H:%M:%S GMT"),
        )
    return res

def json_status(status_code, message):
    res = jsonify(
        {"isBase64Encoded": False, "statusCode": status_code, "body": message}
    )
    res.status = "%s %s" % (status_code, message)
    res.message = message
    return res

def json_unauthorized(message="Invalid credentials"):
    res = jsonify({"isBase64Encoded": False, "statusCode": 401, "body": message})
    res.status = "%s %s" % (401, message)
    res.message = message
    res.headers["WWW-Authenticate"] = None
    return res