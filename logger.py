import os
import re
import sys
import json
import time
import logging
import inspect


class JSONFormatter(logging.Formatter):
    def format(self, record):
        string_formatted_time = time.strftime("%Y-%m-%dT%H:%M:%S", time.gmtime(record.created))
        obj = {}
        if (type(record.msg) is dict):
            obj["message"] = json.dumps(record.msg)
        else:
            obj["message"] = record.msg

        obj['caller'] = inspect.stack()[-2].function

        obj["level"] = record.levelname
        obj["time"] = f"{string_formatted_time}.{record.msecs:3.0f}Z"
        obj["epoch_time"] = record.created
        if hasattr(record, "custom_logging"):
            for key, value in record.custom_logging.items():
                obj[key] = value
        return json.dumps(obj)

def format_api_response(func):
    def wrapper(response):
        payload = {
            'method': response.method,
            'url': response.url,
            'status': response.status_code,
            'message': response.message,
            'elapsed': response.elapsed
        }

        func(payload)
    return wrapper

def striplines(m):
    m = re.compile(r'[\t]').sub(' ', str(m))
    return re.compile(r'[\r\n]').sub('', str(m))

def ex(e):
    logger.exception(striplines(e))

@format_api_response
def rex(resp):
    logger.exception(resp)

def info(msg):
    logger.info(msg)

@format_api_response
def rinfo(resp):
    logger.info(resp)

def err(msg):
    logger.error(msg)

def debug(msg):
    logger.debug(msg)


logger = logging.getLogger(__name__)
logger.propagate = False  # remove default logger
if logger.handlers:
    for handler in logger.handlers:
        logger.removeHandler(handler)

handler = logging.StreamHandler(sys.stdout)
formatter = JSONFormatter()
handler.setFormatter(formatter)

logger.addHandler(handler)

logger.setLevel(logging.INFO)
