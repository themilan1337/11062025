# FastAPI Project with AI Assistants, Celery, and Redis

This project is a FastAPI application featuring user authentication, task management, AI assistant integration (OpenAI), background tasks with Celery, and Redis for caching/messaging.

## Features

- **User Authentication**: Secure registration and login using JWT tokens.
- **Task Management**: CRUD operations for tasks.
- **AI Assistants**: Chat interface with OpenAI backend.
- **Background Tasks**: Celery for asynchronous operations, including a daily data fetching task.
- **Database**: PostgreSQL for data storage, with Alembic for migrations.
- **Caching/Messaging**: Redis integration.
- **Containerization**: Docker and Docker Compose for easy setup and deployment.
- **Frontend**: Simple HTML and Tailwind CSS chat interface.

## Prerequisites

- Docker
- Docker Compose
- Git

## Setup and Running the Project

1.  **Clone the repository:**
    ```bash
    git clone <repository-url>
    cd <project-directory>
    ```

2.  **Environment Variables:**
    Create a `.env` file in the project root by copying `.env.example`:
    ```bash
    cp .env.example .env
    ```
    Update the `.env` file with your actual database credentials, secret keys, and API keys for the AI assistants:
    ```env
    DATABASE_URL=postgresql+asyncpg://username:password@db:5432/postgresdb
    SYNC_DATABASE_URL=postgresql://username:password@db:5432/postgresdb
    SECRET_KEY=your_very_secret_key_here
    ALGORITHM=HS256
    ACCESS_TOKEN_EXPIRE_MINUTES=30

    # AI Assistant API Keys (Obtain from OpenAI)
    OPENAI_API_KEY=your_openai_api_key

    # Celery/Redis (using service names from docker-compose)
    CELERY_BROKER_URL=redis://redis:6379/0
    CELERY_RESULT_BACKEND=redis://redis:6379/0
    REDIS_URL=redis://redis:6379/0 # Used by the application for direct Redis access
    ```
    **Note:** The `db` and `redis` hostnames in the URLs refer to the service names in `docker-compose.yml`.

3.  **Build and Run with Docker Compose:**
    From the project root directory, run:
    ```bash
    docker-compose up --build
    ```
    This command will:
    - Build the Docker images for the FastAPI application, Celery worker, and Celery beat.
    - Start the PostgreSQL database and Redis services.
    - Start the FastAPI application, Celery worker, and Celery beat services.

    To run in detached mode (in the background):
    ```bash
    docker-compose up -d --build
    ```

4.  **Database Migrations:**
    Once the services are running, you need to apply database migrations. Open another terminal and run:
    ```bash
    docker-compose exec web alembic upgrade head
    ```
    This command executes the `alembic upgrade head` command inside the `web` (FastAPI application) container.

5.  **Accessing the Application:**
    -   **API**: The FastAPI application will be available at `http://localhost:8000`.
    -   **Swagger UI (API Docs)**: `http://localhost:8000/docs`
    -   **Chat Interface**: `http://localhost:8000/` (serves the `index.html`)
    -   **Flower (Celery Monitor - if added to docker-compose and requirements):** `http://localhost:5555` (default port for Flower)

## Project Structure

```
.env.example        # Example environment variables
.gitattributes
Dockerfile            # Dockerfile for the FastAPI application
README.md             # This file
alembic.ini         # Alembic configuration
docker-compose.yml    # Docker Compose configuration
migrations/           # Alembic migration scripts
requirements.txt      # Python dependencies
src/
├── assitant/         # AI assistant modules (base, openai)
│   ├── __init__.py
│   ├── base.py
│   └── openai.py
├── auth/             # Authentication logic
├── celery.py         # Celery application setup
├── config.py         # Application configuration (settings)
├── database.py       # Database connection and session management
├── main.py           # FastAPI application entry point
├── redis.py          # Redis connection utilities
├── static/           # Static files (e.g., index.html)
│   └── index.html
└── tasks/            # Task management and background Celery tasks
    ├── __init__.py
    ├── api.py
    ├── background_tasks.py # Celery task definitions
    ├── crud.py
    ├── exceptions.py
    ├── models.py
    ├── schema.py
    └── service.py
```

## API Endpoints

Refer to the Swagger UI at `http://localhost:8000/docs` for a detailed list of API endpoints and their usage.

Key endpoints include:

-   **Auth** (`/auth`):
    -   `/token`: Login and get access token.
    -   `/register`: Register a new user.
    -   `/me`: Get current user details.
-   **Tasks** (`/tasks`):
    -   CRUD operations for tasks.
-   **Chat** (`/api/chat`):
    - `POST`: Send a message to the OpenAI assistant.

## Celery Tasks

-   **`fetch_data_and_save_to_db`**: A periodic task (defined in `src/celery.py` and implemented in `src/tasks/background_tasks.py`) that runs daily to fetch data (placeholder) and save it to the database.

## Deployment to a Droplet (Conceptual Steps)

Deploying this project to a DigitalOcean Droplet (or any VPS) using Docker would generally involve these steps:

1.  **Provision a Droplet:** Create a new Droplet on DigitalOcean (e.g., Ubuntu with Docker pre-installed or install Docker manually).
2.  **Configure Firewall:** Ensure ports 80 (HTTP), 443 (HTTPS), and any other necessary ports (like your application's port if not using a reverse proxy on standard ports) are open.
3.  **Clone Repository:** SSH into your Droplet and clone your project repository.
4.  **Set Up Environment Variables:** Create the `.env` file on the Droplet with your production settings (especially database credentials, API keys, and a strong `SECRET_KEY`).
    -   Consider using a managed database service (like DigitalOcean Managed PostgreSQL) instead of running PostgreSQL in a Docker container on the same Droplet for production for better scalability and reliability.
    -   Store API keys securely, possibly using environment variables injected by your CI/CD system or a secrets manager.
5.  **Install Docker and Docker Compose:** If not already installed.
6.  **Build and Run Docker Compose:**
    ```bash
    docker-compose -f docker-compose.yml up -d --build
    ```
    (You might have a separate `docker-compose.prod.yml` for production overrides).
7.  **Apply Migrations:**
    ```bash
    docker-compose exec web alembic upgrade head
    ```
8.  **Set Up a Reverse Proxy (Recommended):** Use Nginx or Caddy as a reverse proxy to handle incoming HTTP/S traffic, manage SSL certificates (e.g., with Let's Encrypt), and forward requests to your FastAPI application running in Docker.
    -   Configure Nginx to serve static files directly for better performance.
9.  **Configure DNS:** Point your domain name to the Droplet's IP address.
10. **Monitoring and Logging:** Set up monitoring and logging for your application and services.

**Important Considerations for Production:**

-   **Security:** Regularly update dependencies, use strong secrets, configure firewalls properly, and consider security best practices for FastAPI and Docker.
-   **HTTPS:** Always use HTTPS in production. Let's Encrypt provides free SSL certificates.
-   **Database Backups:** Implement regular backups for your PostgreSQL database.
-   **Resource Management:** Monitor resource usage (CPU, memory, disk space) on your Droplet.
-   **Celery Workers:** Adjust the number of Celery workers based on your workload.

## Original Homework Checklist (Status)

- [x] Connect to redis(docker compose)
- [x] Connect to celery(docker compose)
- [ ] Deploy your project in Droplet(with using docker) - *Conceptual steps provided*
- [x] Add a task for everyday fetching data from the website and save it to the database
- [x] Add directory Assitant and create an assisntant (OpenAI)
- [ ] Use a2a to create a chatbot - *Basic assistant structure is in place, A2A is a more advanced concept*
- [x] Connect chatbot to your Frontend

## TODO / Future Enhancements

-   Implement A2A (Agent-to-Agent) chatbot functionality.
-   More sophisticated session management for chat history.
-   Full implementation of image analysis for all assistants (currently placeholders).
-   Add Flower to `docker-compose.yml` for Celery monitoring and update `requirements.txt`.
-   Unit and integration tests.
-   CI/CD pipeline for automated testing and deployment.
