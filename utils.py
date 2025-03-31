import logger
import json

def xstr(s):
    if s is None:
        return ''
    return str(s)

def load_db():
    try:
        with open("fake_db/db.json", "r") as file:
            db_data = json.load(file)
            return db_data
    except FileNotFoundError:
        logger.error("db.json file not found")
        return None
    except json.JSONDecodeError as e:
        logger.error(f"Error decoding db.json: {e}")
        return None