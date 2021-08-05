# Flask messaging back-end
## About
REST messaging back-end written in Python with Flask

Authorization with JWT signed using PBKDF2

SQLite database using SQLAlchemy ORM

## Installation
- Run ``scripts/generate-secret.py``
- Initialize database using Python commandline:
```
from db import init_db
init_db()
```

## Endpoints
### POST /register
Sample request:
```
{
    "username": "Test",
    "password": "123",
    "email": "test@mail.com"
}
```
Sample successful response (200):
```
{
    "success": true,
    "id": 3
}
```
Sample unsuccessful response (400):
```
{
    "success": false,
    "message": "Username or Email already exist"
}
```

### POST /auth
Sample request:
```
{
    "username": "Test", 
    "password": "123"
}
```
Sample successful response (200):
```
{
    "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE2MjkwMzc2MTQsImlhdCI6MTYyODE3MzYxNCwibmJmIjoxNjI4MTczNjE0LCJpZGVudGl0eSI6Mn0.FKsC7fKFXy7d7Xf9RvGpair_Alro8GwTF89HGWiv_vY"
}
```
Sample unsuccessful response (400):
```
{
    "description": "Invalid credentials",
    "error": "Bad Request",
    "status_code": 401
}
```

### POST /messages (Authorization header required)
Sample request:
```
{
    "recipient_id": 2,
    "subject": "some subject",
    "message": "some message"
}
```
Sample successful response (200):
```
{
    "success": true
}
```
Sample unsuccessful response (400):
```
{
    "success": false,
    "error": "Invalid request body, please provide json with [sender_id, recipient_id, message, subject]"
}
```

### GET /messages/:all_or_unread/:sent_or_received (Authorization header required)
- :all_or_unread - "all" will include read messages as well as unread, "unread" will return only unread
- :sent_or_received - "sent" will return sent messages, "received" will return received messages, omitting this argument will return both

Sample response (200):
```
[
    {
        "id": 2,
        "sender_id": 2,
        "recipient_id": 2,
        "message": "some message",
        "subject": "some subject",
        "timestamp": 1628162321.831862
    },
    {
        "id": 3,
        "sender_id": 2,
        "recipient_id": 2,
        "message": "some message",
        "subject": "some subject",
        "timestamp": 1628162902.440958
    }
]
```

### GET /message (Authorization header required)
Sample response (200):
```
{
    "id": 2,
    "sender_id": 2,
    "recipient_id": 2,
    "message": "some message",
    "subject": "some subject",
    "timestamp": 1628163024.465324
}
```
Sample response (404):
```
{
    "error": "No unread messages"
}
```

### DELETE /message/:id (Authorization header required)
Sample response (200):
```
{
    "success": true
}
```
Sample response (404):
```
{
    "success": false,
    "error": "ID does not exist"
}
```