# Ojus Sports Management API

A Django REST API for managing sports events, registrations, and teams.

## Authentication Endpoints

### 1. Login
- **URL:** `/api/login/`
- **Method:** `POST`
- **Request Body:**
```json
{
    "username": "string",
    "password": "string"
}
```
- **Response:**
```json
{
    "access": "string",
    "refresh": "string"
}
```

### 2. Token Refresh
- **URL:** `/api/token/refresh/`
- **Method:** `POST`
- **Request Body:**
```json
{
    "refresh": "string"
}
```
- **Response:**
```json
{
    "access": "string"
}
```

### 3. User Details
- **URL:** `/api/me/`
- **Method:** `GET`
- **Authentication:** Required
- **Response:**
```json
{
    "moodleID": "integer",
    "username": "string",
    "email": "string",
    "first_name": "string",
    "last_name": "string",
    "phone_number": "string",
    "profile_image": "string"
}
```

### 4. Sign Up
- **URL:** `/api/signup/`
- **Method:** `POST`
- **Request Body:**
```json
{
    "moodleID": "integer",
    "username": "string",
    "password": "string",
    "email": "string"
}
```
- **Response:**
```json
{
    "message": "User created successfully."
}
```

### 5. Update Profile
- **URL:** `/api/me/update/`
- **Methods:** `PUT`, `PATCH`
- **Authentication:** Required
- **Content-Type:** `multipart/form-data` or `application/json`
- **Request Body:**
```json
{
    "first_name": "string",
    "last_name": "string",
    "email": "string",
    "phone_number": "string",
    "profile_image": "file"
}
```

## Sports Management Endpoints

### 1. Sports List
- **URL:** `/api/sports/`
- **Methods:** `GET`, `POST`
- **Authentication:** Required
- **GET Response:**
```json
[
    {
        "id": "integer",
        "name": "string",
        "description": "string",
        "isTeamBased": "boolean",
        "primary": {
            "moodleID": "integer",
            "username": "string",
            "email": "string"
        },
        "secondary": [
            {
                "moodleID": "integer",
                "username": "string",
                "email": "string"
            }
        ]
    }
]
```
- **POST Request Body:**
```json
{
    "name": "string",
    "description": "string",
    "isTeamBased": "boolean"
}
```

### 2. Sport Detail
- **URL:** `/api/sports/<id>/`
- **Methods:** `GET`, `PUT`, `DELETE`
- **Authentication:** Required
- **Authorization:** Only primary or secondary coordinators can modify/delete
- **PUT Request Body:**
```json
{
    "name": "string",
    "description": "string",
    "isTeamBased": "boolean"
}
```

### 3. Registrations List
- **URL:** `/api/registrations/`
- **Methods:** `GET`, `POST`
- **Authentication:** Required
- **GET Response:**
```json
[
    {
        "id": "integer",
        "student": {
            "moodleID": "integer",
            "username": "string",
            "email": "string"
        },
        "sport": {
            "id": "integer",
            "name": "string",
            "description": "string",
            "isTeamBased": "boolean"
        },
        "year": "integer",
        "branch": "string",
        "registered_on": "datetime",
        "registration_modified": "datetime"
    }
]
```
- **POST Request Body:**
```json
{
    "sport_id": "integer",
    "year": "integer",
    "branch": "string"
}
```

### 4. Registration Detail
- **URL:** `/api/registrations/<id>/`
- **Methods:** `GET`, `PUT`, `DELETE`
- **Authentication:** Required
- **Authorization:** Only the registered student or sport coordinators can access/modify

### 5. Teams List
- **URL:** `/api/teams/`
- **Methods:** `GET`, `POST`
- **Authentication:** Required
- **GET Response:**
```json
[
    {
        "id": "integer",
        "name": "string",
        "branch": "string",
        "sport": {
            "id": "integer",
            "name": "string",
            "description": "string",
            "isTeamBased": "boolean"
        },
        "members": [
            {
                "moodleID": "integer",
                "username": "string",
                "email": "string"
            }
        ]
    }
]
```
- **POST Request Body:**
```json
{
    "name": "string",
    "branch": "string",
    "sport_id": "integer",
    "member_ids": ["integer"]
}
```

### 6. Team Detail
- **URL:** `/api/teams/<id>/`
- **Methods:** `GET`, `PUT`, `DELETE`
- **Authentication:** Required
- **Authorization:** Team members can view/edit, only coordinators can delete

## Authentication

All endpoints except login and signup require JWT authentication. Include the JWT token in the Authorization header:

```
Authorization: Bearer <access_token>
```

## Error Responses

The API returns appropriate HTTP status codes:

- 200: Success
- 201: Created
- 204: No Content (successful deletion)
- 400: Bad Request
- 401: Unauthorized
- 403: Forbidden
- 404: Not Found
- 500: Server Error

Error responses include detail messages explaining the error:

```json
{
    "error": "Error message description"
}
```