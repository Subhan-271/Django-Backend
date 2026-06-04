# Smart Assessment AI - User Registration & Authentication Guide

## Overview
This guide will help you set up and test user registration for students and teachers in your Django backend.

## What Was Added

### New API Endpoints
1. **Register Student**: `POST /api/accounts/auth/register/student/`
2. **Register Teacher**: `POST /api/accounts/auth/register/teacher/`
3. **Login**: `POST /api/accounts/auth/login/`
4. **Get Current User**: `GET /api/accounts/me/`
5. **List All Users**: `GET /api/accounts/users/` (Admin only)
6. **Refresh Token**: `POST /api/auth/refresh/`

### User Model
Users now have role-based access:
- **STUDENT**: Student role
- **TEACHER**: Teacher role
- **ADMIN**: Administrator role

## Setup Instructions

### 1. Run Migrations
```bash
python manage.py migrate
```

### 2. Start Development Server
```bash
python manage.py runserver
```

## Testing in Postman

### Step 1: Import Collection
1. Open Postman
2. Click **Import** (top-left corner)
3. Select **Upload Files**
4. Choose `Smart_Assessment_AI.postman_collection.json`

### Step 2: Register a Student
1. Go to **Authentication** → **Register Student**
2. Click **Send**
3. You should get a `201 Created` response with the user data

**Sample Request:**
```json
{
  "username": "john_student",
  "email": "john@student.com",
  "password": "SecurePass123",
  "password_confirm": "SecurePass123",
  "first_name": "John",
  "last_name": "Doe"
}
```

### Step 3: Register a Teacher
1. Go to **Authentication** → **Register Teacher**
2. Modify the request body with different credentials
3. Click **Send**

**Sample Request:**
```json
{
  "username": "jane_teacher",
  "email": "jane@teacher.com",
  "password": "SecurePass123",
  "password_confirm": "SecurePass123",
  "first_name": "Jane",
  "last_name": "Smith"
}
```

### Step 4: Login
1. Go to **Authentication** → **Login**
2. Use credentials from a registered user
3. Click **Send**
4. Copy the `access` token from response

**Sample Request:**
```json
{
  "username": "john_student",
  "password": "SecurePass123"
}
```

**Response Example:**
```json
{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "user": {
    "id": 1,
    "username": "john_student",
    "email": "john@student.com",
    "role": "STUDENT",
    "first_name": "John",
    "last_name": "Doe"
  }
}
```

### Step 5: Get Current User
1. Go to **Users** → **Get Current User**
2. Update the Authorization header with your access token:
   - Header: `Authorization`
   - Value: `Bearer YOUR_ACCESS_TOKEN`
3. Click **Send**

### Step 6: Using Variables in Postman

For easier testing, use Postman variables:

1. After login, copy the `access` token
2. Go to **Variables** tab (top-right)
3. Set `access_token` = your token
4. In requests, use: `{{access_token}}` in Authorization header

## Response Codes

| Code | Meaning |
|------|---------|
| 201 | User created successfully |
| 200 | Request successful |
| 400 | Invalid data (validation error) |
| 401 | Unauthorized (missing/invalid token) |
| 403 | Forbidden (insufficient permissions) |
| 404 | Not found |

## Error Examples

### Password Mismatch
```json
{
  "password": ["Passwords must match."]
}
```

### Missing Required Fields
```json
{
  "username": ["This field is required."],
  "email": ["This field is required."]
}
```

### Invalid Login
```json
{
  "detail": "Please enter the correct username and password for a staff account."
}
```

## Files Modified

1. **accounts/serializers.py** - Added registration serializers
2. **accounts/views.py** - Added registration views
3. **accounts/urls.py** - Added registration routes
4. **config/urls.py** - Updated main URL configuration
5. **Smart_Assessment_AI.postman_collection.json** - New Postman collection

## Next Steps for React Integration

### Install Dependencies
```bash
npm install axios
```

### Create API Service
```javascript
import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000/api';

const api = axios.create({
  baseURL: API_BASE_URL,
});

// Add token to requests
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export const authAPI = {
  registerStudent: (data) => api.post('/accounts/auth/register/student/', data),
  registerTeacher: (data) => api.post('/accounts/auth/register/teacher/', data),
  login: (username, password) => api.post('/accounts/auth/login/', { username, password }),
  getCurrentUser: () => api.get('/accounts/me/'),
  refreshToken: (refresh) => api.post('/auth/refresh/', { refresh }),
};

export default api;
```

### Store Tokens
```javascript
// After successful login
const response = await authAPI.login(username, password);
localStorage.setItem('access_token', response.data.access);
localStorage.setItem('refresh_token', response.data.refresh);
```

## Troubleshooting

### CORS Issues
- Ensure `CORS_ALLOW_ALL_ORIGINS = True` in settings.py (already set)

### 401 Unauthorized
- Token may have expired - use refresh endpoint
- Ensure token is in correct format: `Bearer YOUR_TOKEN`

### 404 Not Found
- Check Django server is running: `python manage.py runserver`
- Verify URL paths match

## Support
For any issues, check Django logs in the terminal where you started the server.
