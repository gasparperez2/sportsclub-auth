import json
import logger
import os
import time
import jwt
from datetime import datetime, timezone, timedelta
from flask import Flask, request
from utils import xstr, load_db
from reponses import json_respond, json_status, json_unauthorized
from werkzeug.security import check_password_hash, generate_password_hash


app = Flask(__name__)

db = load_db()
if db is None:
    raise Exception("Database not found")

@app.route("/api/signup", methods=["POST"])
def signup():
    ip = request.remote_addr

    # Validaciones de entrada
    json_data = request.get_json()
    if not json_data:
        return json_status("400", "JSON payload es requerido")
    dni = json_data.get("dni")
    if not dni:
        return json_status("400", "DNI es requerido")
    contraseña = json_data.get("contraseña")
    if not contraseña:
        return json_status("400", "La constraseña es requerida") 
    nombre = json_data.get("nombre")
    if not nombre:
        return json_status("400", "El nombre es requerido")
    apellido = json_data.get("apellido")
    if not apellido:
        return json_status("400", "El apellido es requerido")
    estado = json_data.get("estado")
    if not estado:
        return json_status("400", "El estado es requerido")
    if estado not in ["autorizado", "denegado"]:
        return json_status("400", "El estado no es válido")
    logger.info("Creando usuario con DNI: %s" % dni)

    # Valida que el DNI no exista
    try:
        fetched_user = None
        for user in db["Usuarios"]:
            if user["dni"] == dni:
                fetched_user = user

        if fetched_user:
            logger.info("El DNI ya existe: %s" % dni)
            return json_status("400", "El DNI ya existe")
    except Exception as e:
        logger.ex(e)
        return json_status("500", "Error interno del servidor")
    
    try:
        # Creacion del usuario
        new_user = {
            "id": len(db["Usuarios"]) + 1,
            "dni": dni,
            "password_hash": generate_password_hash(contraseña),
            "nombre": nombre,
            "apellido": apellido,
            "estado": estado
        }
        db["Usuarios"].append(new_user)
        with open("fake_db/db.json", "w") as file:
            json.dump(db, file)
        logger.info("Usuario creado con DNI: %s" % dni)

        # Generacion de token
        expires = datetime.now(timezone.utc) + timedelta(minutes=240)
        token = jwt.encode(
            {
                "id": xstr(new_user["id"]),
                "dni": xstr(new_user["dni"]),
                "nombre": xstr(new_user["nombre"]),
                "apellido": xstr(new_user["apellido"]),
                "estado": xstr(new_user["estado"]),
                "exp": expires,
                "iat": datetime.utcnow(),
            },
            os.environ["CUSTOM_SECRET"],
            "HS256",
        ).decode("ascii")

        response = json_respond(
            {
                "id": xstr(new_user["id"]),
                "dni": xstr(new_user["dni"]),
                "nombre": xstr(new_user["nombre"]),
                "apellido": xstr(new_user["apellido"]),
                "estado": xstr(new_user["estado"])
            },
            "Token issued",
            token,
        )

        return response
    except Exception as e:
        logger.ex(e)
        return json_status("500", "Error interno del servidor")


@app.route("/api/acceso", methods=["POST"])
def login():
    ip = request.remote_addr
    
    # Validaciones de entrada
    json_data = request.get_json()
    if not json_data:
        return json_status("400", "JSON payload es requerido")
    dni = json_data.get("dni")
    if not dni:
        return json_status("400", "DNI es requerido")
    contraseña = json_data.get("contraseña")
    if not contraseña:
        return json_status("400", "La constraseña es requerido")
    logger.info("Validando DNI: %s" % dni)

    try:
        # Valida que el DNI exista
        fetched_user = None
        for user in db["Usuarios"]:
            if user["dni"] == dni:
                fetched_user = user

        if not fetched_user:
            logger.info("DNI no encontrado: %s" % dni)
            return json_status("404", "El DNI no fue encontrado")
    except Exception as e:
        logger.ex(e)
        return json_status("500", "Error interno del servidor")
    
    # Valida la contraseña
    if not check_password_hash(fetched_user["password_hash"], contraseña):
        logger.info("Contraseña incorrecta para DNI: %s" % dni)
        return json_unauthorized("Contraseña incorrecta")
    
    # Valida el estado del usuario
    if fetched_user["estado"] != "autorizado":
        logger.info("Acceso denegado para DNI: %s" % dni)
        return json_unauthorized("Usuario denegado")

    expires = datetime.now(timezone.utc) + timedelta(minutes=240)
    token = jwt.encode(
        {
            "id": xstr(fetched_user["id"]),
            "dni": xstr(fetched_user["dni"]),
            "nombre": xstr(fetched_user["nombre"]),
            "apellido": xstr(fetched_user["apellido"]),
            "estado": xstr(fetched_user["estado"]),
            "exp": expires,
            "iat": datetime.utcnow(),
        },
        os.environ["CUSTOM_SECRET"],
        "HS256",
    ).decode("ascii")

    response = json_respond(
        {
            "id": xstr(fetched_user["id"]),
            "dni": xstr(fetched_user["dni"]),
            "nombre": xstr(fetched_user["nombre"]),
            "apellido": xstr(fetched_user["apellido"]),
            "estado": xstr(fetched_user["estado"])
        },
        "Token issued",
        token,
    )

    logger.info("Token issued for DNI: %s" % dni)
    return response

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5404, debug=os.environ["DEBUG"] or False)