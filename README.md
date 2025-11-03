# Ojus Sports Management API

A Django REST API for managing sports events, registrations, and teams.

NOTE: Authentication endpoints are mounted at `/auth/` and sports endpoints are mounted at `/api/` (see project `urls.py`).

## Authentication Endpoints (base: `/auth/`)

### 1. Login
- **URL:** `/auth/login/`
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
- **URL:** `/auth/token/refresh/`
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
- **URL:** `/auth/me/`
- **Method:** `GET`
- **Authentication:** Required
- **Response:**
```json
{
    "moodleID": 123,
    "username": "string",
    "email": "string",
    "first_name": "string",
    "last_name": "string",
    "phone_number": "string",
    "profile_image": "string"
}
```

### 4. Sign Up
- **URL:** `/auth/signup/`
- **Method:** `POST`
- **Request Body:**
```json
{
    "moodleID": 123,
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
- **URL:** `/auth/me/update/`
- **Methods:** `PUT`, `PATCH`
- **Authentication:** Required
- **Content-Type:** `multipart/form-data` or `application/json`
- **Request Body (partial allowed):**
```json
{
    "first_name": "string",
    "last_name": "string",
    "email": "string",
    "phone_number": "string",
    "profile_image": "file"
}
```

## Sports Management Endpoints (base: `/api/`)

### 1. Sports List
- **URL:** `/api/sports/`
- **Methods:** `GET`, `POST`
- **Authentication:** Required
- **GET Response:**
```json
[
    {
        "id": 1,
        "name": "string",
        "description": "string",
        "isTeamBased": true,
        "primary": {
            "moodleID": 123,
            "username": "string",
            "email": "string"
        },
        "secondary": [
            {
                "moodleID": 456,
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
    "isTeamBased": true
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
    "isTeamBased": true
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
        "id": 1,
        "student": {
            "moodleID": 123,
            "username": "string",
            "email": "string"
        },
        "sport": {
            "id": 1,
            "name": "string",
            "description": "string",
            "isTeamBased": true
        },
        "year": 3,
        "branch": "CSE",
        "registered_on": "2025-01-01T12:00:00Z",
        "registration_modified": "2025-01-02T12:00:00Z"
    }
]
```
- **POST Request Body:**
```json
{
    "sport_id": 1,
    "year": 3,
    "branch": "CSE"
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
        "id": 1,
        "name": "Team A",
        "branch": "CSE",
        "sport": {
            "id": 1,
            "name": "string",
            "description": "string",
            "isTeamBased": true
        },
        "members": [
            {
                "moodleID": 123,
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
    "sport_id": 1,
    "member_ids": [123, 456]
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

Error responses include detail messages explaining the error, usually as a JSON object with a `detail` or field-specific errors, e.g.:

```json
{
    "detail": "Error message description"
}
```