# Database Schema

## Entity Relationship Diagram

```
            +-----------------+       +-----------------+
            |     users       |       |     genres      |
            +-----------------+       +-----------------+
            | id (PK)         |       | id (PK)         |
            | email (UK)      |       | name            |
            | hashed_password |       | description     |
            | is_active       |       | created_at      |
            | is_superuser    |       +-----------------+
            | created_at      |                   |   |   |
            +-----------------+                   |   |   |
                                                  |   |   |
            +-----------------+                   |   v   v   |
            |     titles      |       +-----------------+       |
            +-----------------+       |     platforms   |       |
            | id (PK)           |       +-----------------+       |
            | title             |                   | id (PK)   |
            | original_title    |                   | name        |
            | description       |                   | slug        |
            | release_year      |                   | description |
            | rating            |                   | created_at  |
            | duration_minutes  |                   +-------------+
            | is_featured       |                   |     |         |
            | genre_id (FK)     +--------------------->| TitleGenre  |
            | platform_id (FK)                | title_id(PK)|
            +-----------------+               | genre_id(PK)|
                                                +-------------+

```

## Table Details

### users
- **id**: INTEGER, PRIMARY KEY, AUTOINCREMENT
- **email**: VARCHAR(255), UNIQUE, NOT NULL
- **hashed_password**: VARCHAR(255), NOT NULL
- **is_active**: BOOLEAN, DEFAULT True
- **is_superuser**: BOOLEAN, DEFAULT False
- **created_at**: DATETIME, DEFAULT CURRENT_TIMESTAMP
- **updated_at**: DATETIME, DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP

### genres
- **id**: INTEGER, PRIMARY KEY, AUTOINCREMENT
- **name**: VARCHAR(100), UNIQUE, NOT NULL
- **description**: TEXT, NULLABLE
- **created_at**: DATETIME, DEFAULT CURRENT_TIMESTAMP

### platforms
- **id**: INTEGER, PRIMARY KEY, AUTOINCREMENT
- **name**: VARCHAR(100), UNIQUE, NOT NULL
- **slug**: VARCHAR(100), UNIQUE, NOT NULL
- **description**: TEXT, NULLABLE
- **created_at**: DATETIME, DEFAULT CURRENT_TIMESTAMP

### titles
- **id**: INTEGER, PRIMARY KEY, AUTOINCREMENT
- **title**: VARCHAR(255), NOT NULL
- **original_title**: VARCHAR(255), NULLABLE
- **description**: TEXT, NULLABLE
- **release_year**: INTEGER, NULLABLE (1900-2100)
- **rating**: FLOAT, NULLABLE (0-10)
- **duration_minutes**: INTEGER, NULLABLE
- **is_featured**: BOOLEAN, DEFAULT False
- **genre_id**: INTEGER, FK → genres.id, NULLABLE
- **platform_id**: INTEGER, FK → platforms.id, NULLABLE
- **created_at**: DATETIME, DEFAULT CURRENT_TIMESTAMP
- **updated_at**: DATETIME, DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP

### title_genres (Junction Table - Many-to-Many)
- **title_id**: INTEGER, PK, FK → titles.id
- **genre_id**: INTEGER, PK, FK → genres.id

## Indexes
- `uix_email` on users(email)
- `ix_genres_name` on genres(name)
- `ix_platforms_slug` on platforms(slug)
- `ix_titles_title` on titles(title)
- `ix_titles_release_year` on titles(release_year)
- `ix_titles_is_featured` on titles(is_featured)

## SQLAlchemy 2.0 Async Configuration
- Async engine created with `create_async_engine()`
- Session factory with `sessionmaker(class_=AsyncSession)`
- All model operations use `async with SessionLocal() as session`
- Relationships defined with `relationship()` and `back_populates`
- Foreign keys use `ForeignKey()` constraint