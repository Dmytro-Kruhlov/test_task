# README for AI-Enhanced Notes Management System

## Project Overview

This project is an AI-Enhanced Notes Management System built using FastAPI, SQLAlchemy, and PostgreSQL. The application allows users to create, read, update, and delete notes, while also providing analytics on the notes created. The system integrates with Google Generative AI for generating summaries of the notes.

## Table of Contents

- [Technologies Used](#technologies-used)
- [Project Structure](#project-structure)
- [Setup Instructions](#setup-instructions)
- [API Endpoints](#api-endpoints)
- [Testing](#testing)
- [Implementation Decisions](#implementation-decisions)

## Technologies Used

- **FastAPI**: A modern web framework for building APIs with Python 3.6+ based on standard Python type hints.
- **SQLAlchemy**: A SQL toolkit and Object-Relational Mapping (ORM) system for Python.
- **PostgreSQL**: A powerful, open-source object-relational database system.
- **Pydantic**: Data validation and settings management using Python type annotations.
- **NLP with NLTK**: Natural Language Processing for tokenization and stopword removal.
- **Google Generative AI**: For generating summaries of notes.
- **Redis**: Used for caching and managing user sessions.
- **Docker**: For containerization of the application.

## Project Structure

/src
├── /Tests # Directory for test cases
├── /database # Database models and connection
├── /repository # Data access layer
├── /routes # API routes
├── /services # Business logic and external service integrations
├── main.py # Entry point for the FastAPI application
├── schemas # Pydantic schemas for data validation
└── conf.py # Configuration settings

### Key Files

- **`main.py`**: The entry point of the application where FastAPI is initialized and routes are included.
- **`db.py`**: Contains the database connection setup and session management.
- **`models.py`**: Defines the database models using SQLAlchemy.
- **`schemas.py`**: Contains Pydantic models for data validation and serialization.
- **`routes/`**: Contains the API endpoints for user authentication, note management, and analytics.
- **`services/`**: Contains business logic, including analytics and AI integration.
- **`Tests/`**: Contains unit tests for various components of the application.

## Setup Instructions

### Prerequisites

- Python 3.11 or higher
- PostgreSQL
- Redis
- Docker (optional, for containerized setup)

### Installation Steps

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd test_task
   ```

2. **Create a virtual environment** (optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install dependencies**:
   ```bash
   pip install poetry
   poetry install
   ```

4. **Set up environment variables**:
   Create a `.env` file in the root directory and add the following:
   ```env
   POSTGRES_DB=postgres
   POSTGRES_USER=postgres
   POSTGRES_PASSWORD=password
   POSTGRES_PORT=5432
   POSTGRES_HOST=localhost
   SQLALCHEMY_DATABASE_URL=postgresql+psycopg2://${POSTGRES_USER}:${POSTGRES_PASSWORD}@${POSTGRES_HOST}:${POSTGRES_PORT}/${POSTGRES_DB}
   SECRET_KEY=your_secret_key
   ALGORITHM=HS256
   REDIS_HOST=localhost
   REDIS_PORT=6379
   GOOGLE_API_KEY=your_google_api_key
   ```

5. **Run the application**:
   You can run the application using:
   ```bash
   poetry run alembic upgrade head
   poetry run uvicorn main:app --host 0.0.0.0 --port 8000 --reload
6. **Using Docker**:
   If you prefer to use Docker, you can build and run the containers using:
   ```bash
   docker-compose up --build
   docker-compose exec web poetry run alembic upgrade head

   ```

## API Endpoints

### User Authentication

- **POST /api/auth/signup**: Create a new user.
- **POST /api/auth/login**: Log in a user and return access and refresh tokens.
- **GET /api/auth/refresh_token**: Refresh the access token.

### Notes Management

- **POST /api/notes/**: Create a new note.
- **GET /api/notes/{note_id}**: Retrieve a specific note by ID.
- **PUT /api/notes/{note_id}**: Update a specific note by ID.
- **DELETE /api/notes/{note_id}**: Delete a specific note by ID.
- **GET /api/notes/user/{user_id}**: Retrieve all notes for a specific user.
- **GET /api/notes/analytics/stats**: Get analytics data for notes.

## Testing

To run the tests, use the following command:
```bash
pytest
```

### Test Structure

- Tests are organized in the `Tests/` directory, with separate files for testing routes, repositories, and services.
- Each test uses fixtures to set up the database state and mock dependencies where necessary.

## Implementation Decisions

1. **Asynchronous Programming**: The application uses asynchronous programming with FastAPI to handle multiple requests concurrently, improving performance and responsiveness.

2. **Database Management**: SQLAlchemy is used for ORM, allowing for easy interaction with the PostgreSQL database. The database models are defined in `models.py`, and the data access layer is separated into the `repository` directory.

3. **Data Validation**: Pydantic schemas are used for data validation and serialization, ensuring that incoming and outgoing data adheres to the expected formats.

4. **AI Integration**: The application integrates with Google Generative AI to provide summaries of notes. This is handled in the `services/ai.py` file, where the AI model is set up and used to generate content.

5. **Analytics**: The `AnalyticsService` class in `services/analytics.py` calculates various statistics about the notes, such as total word count and average note length.

6. **Testing**: The project includes comprehensive unit tests for all major components, ensuring that the application behaves as expected and that changes do not introduce new bugs.

7. **Containerization**: Docker is used to containerize the application, making it easy to deploy and manage dependencies. The `docker-compose.yml` file defines the services required for the application, including PostgreSQL and Redis.

## Conclusion

This AI-Enhanced Notes Management System is designed to be a robust and scalable application for managing notes with integrated AI capabilities. The use of modern technologies and best practices ensures that the application is maintainable and easy to extend in the future.