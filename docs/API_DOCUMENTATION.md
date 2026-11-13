# API Documentation

## Planned API Endpoints

### Authentication

#### POST /api/v1/auth/register
- **Request Body**:
  ```json
  {
    "email": "user@example.com",
    "password": "password123"
  }
  ```
- **Response**: `201 Created` - User created with JWT token
- **Authentication**: None (public endpoint)
- **Status Codes**: `201 Created`, `400 Bad Request` (email already registered)

#### POST /api/v1/auth/login
- **Request Body**:
  ```json
  {
    "email": "user@example.com",
    "password": "password123"
  }
  ```
- **Response**: `200 OK` - JWT access token and token type
- **Authentication**: None (public endpoint)
- **Status Codes**: `200 OK`, `401 Unauthorized` (invalid credentials)

---

### Users

#### GET /api/v1/users/me
- **Response**: `200 OK` - Current authenticated user profile
- **Authentication**: Bearer JWT token required
- **Status Codes**: `200 OK`, `401 Unauthorized`

---

### Titles (Movies & TV Shows)

#### POST /api/v1/titles/
- **Request Body**: TitleCreate schema with title, description, release_year, rating, duration_minutes, is_featured, genre_ids, platform_ids
- **Response**: `201 Created` - Created title
- **Authentication**: Bearer JWT token required
- **Status Codes**: `201 Created`, `401 Unauthorized`, `422 Validation Error`

#### GET /api/v1/titles/
- **Response**: `200 OK` - List of titles with pagination
- **Authentication**: Bearer JWT token required
- **Query Parameters**: 
  - `skip`: int (default 0)
  - `limit`: int (default 100)
- **Status Codes**: `200 OK`, `401 Unauthorized`

#### GET /api/v1/titles/{title_id}
- **Response**: `200 OK` - Specific title by ID, `404 Not Found` if not found
- **Authentication**: Bearer JWT token required
- **Status Codes**: `200 OK`, `401 Unauthorized`, `404 Not Found`

#### PUT /api/v1/titles/{title_id}
- **Request Body**: TitleUpdate schema with optional fields
- **Response**: `200 OK` - Updated title, `404 Not Found` if not found
- **Authentication**: Bearer JWT token required
- **Status Codes**: `200 OK`, `401 Unauthorized`, `404 Not Found`, `422 Validation Error`

#### DELETE /api/v1/titles/{title_id}
- **Response**: `204 No Content`, `404 Not Found` if not found
- **Authentication**: Bearer JWT token required
- **Status Codes**: `204 No Content`, `401 Unauthorized`, `404 Not Found`

---

### Genres

#### GET /api/v1/genres/
- **Response**: `200 OK` - List of all genres
- **Authentication**: None (public endpoint) or Bearer token as needed
- **Status Codes**: `200 OK`

---

### Platforms (OTT Platforms)

#### GET /api/v1/platforms/
- **Response**: `200 OK` - List of all OTT platforms
- **Authentication**: None (public endpoint) or Bearer token as needed
- **Status Codes**: `200 OK`

---

### Search

#### GET /api/v1/search/
- **Response**: `200 OK` - List of matching titles
- **Authentication**: None (public endpoint) or Bearer token as needed
- **Query Parameters**:
  - `query`: string (search term, default "")
  - `genre_id`: int (filter by genre, default 0)
  - `platform_id`: int (filter by platform, default 0)
  - `release_year`: int (filter by release year, default 0)
- **Status Codes**: `200 OK`

---

### Background Sync

#### POST /api/v1/sync/
- **Response**: `202 Accepted` - Synchronization started
- **Authentication**: Bearer JWT token required (admin only)
- **Status Codes**: `202 Accepted`, `401 Unauthorized`, `403 Forbidden`

## Response Formats

### Success Response
```json
{
  "success": true,
  "data": { ... }
}
```

### Error Response
```json
{
  "detail": "Specific error message",
  "success": false
}
```

### Pagination Meta
```json
{
  "total": 150,
  "page": 1,
  "per_page": 10,
  "total_pages": 15
}