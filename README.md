# sportsclub-auth

Cree dos endpoints, uno para registrar un usuario y otro para loguearlo. Los dos endpoints retornan un token en forma de cookie.

Para inicializar la app primero hay que instalar las dependencias y despues correr la app, ademas hay que asignar alguna variable de entorno. Para eso usamos estos comandos:

`export CUSTOM_SECRET={secret_key}`

`python3.11 -m venv ./venv && source venv/bin/activate && pip3 install -r requirements.txt`

`python3.11 main.py`

## Register User

### Request
/api/signup
```
curl -X POST -H "Content-Type: application/json" -d '{"nombre": "Juan", "dni": "12345678", "contraseña": "password123", "apellido": "Perez", "estado": "autorizado"}' http://localhost:5404/api/signup
```

### Response
```
{
  "body": "Token issued",
  "data": {
    "apellido": "Perez",
    "dni": "12345671",
    "estado": "autorizado",
    "id": "3",
    "nombre": "Juan"
  },
  "isBase64Encoded": false,
  "statusCode": 200
}
```

## Login User

### Request
/api/signup
```
curl -X POST -H "Content-Type: application/json" -d '{"dni": "12345678", "contraseña": "password123"}' http://localhost:5404/api/acceso
```

### Response
```
{
  "body": "Token issued",
  "data": {
    "apellido": "Perez",
    "dni": "12345678",
    "estado": "autorizado",
    "id": "1",
    "nombre": "Juan"
  },
  "isBase64Encoded": false,
  "statusCode": 200
}
```