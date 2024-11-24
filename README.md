# FastAPI Blog Application with Authentication

The **FastAPI** blog application supports core features like creating, reading, updating, and deleting posts. Additionally, it includes user authentication with **OAuth2** using **JWT tokens**. Here's a breakdown of how each part works:

### Application Setup

- The FastAPI application is initialized in `main.py`, where it includes routers for authentication (`auth`), user management (`users`), and blog posts (`blog`).
- `models.Base.metadata.create_all(engine)` creates the necessary database tables based on the defined **SQLAlchemy** models.

### OAuth2 Authentication

- The application uses `OAuth2PasswordBearer` for token-based authentication.
- The `get_current_user` function validates incoming JWT tokens and retrieves the user associated with the token.
- The `verify_access_token` function decodes the JWT and checks its validity, ensuring the token contains a valid user ID and email.

### Schemas

- **Pydantic models** are used for input validation and serialization of data. Models like `BlogBase`, `ShowBlog`, and `User` define the structure of blog and user data.
- The `Token` and `TokenData` models are used for generating and returning JWT tokens during login.

### Token Generation

- The application uses the `jwt` library to generate access tokens.
- The `create_access_token` function creates a JWT token, encoding it with a secret key and setting an expiration time (30 minutes in this case).
- The token contains the user ID and email, and it is used for authenticating subsequent requests to the API.

### Password Hashing

- The application uses **bcrypt** to securely hash and verify passwords.
- The `Hasher` class provides methods for hashing passwords and checking them against stored hashes.

### Login Logic

- The `login` function verifies the user's credentials by checking the email and password against the database.
- If the credentials are valid, a JWT token is generated and returned. If invalid, an HTTP 401 Unauthorized error is raised.

### How It All Ties Together

- When a user logs in, the application checks the provided credentials, and if they're correct, it generates and returns a JWT token.
- This token is used for authenticating future requests, ensuring secure access to blog functionalities like creating, updating, or deleting blog posts.
- This setup effectively combines user management and blog functionality with secure authentication via JWT, ensuring that only authenticated users can perform certain actions.
- The use of **Docker** for containerization and **environment variables** for sensitive data adds to the application's scalability and security.

 
## Table of Contents

- [FastAPI Blog Application with Authentication](#fastapi-blog-application-with-authentication)
    - [Application Setup](#application-setup)
    - [OAuth2 Authentication](#oauth2-authentication)
    - [Schemas](#schemas)
    - [Token Generation](#token-generation)
    - [Password Hashing](#password-hashing)
    - [Login Logic](#login-logic)
    - [How It All Ties Together](#how-it-all-ties-together)
  - [Table of Contents](#table-of-contents)
  - [Project Setup](#project-setup)
    - [Prerequisites](#prerequisites)
    - [Setting Up the Environment](#setting-up-the-environment)
    - [Install Dependencies](#install-dependencies)
    - [Running the Application Locally](#running-the-application-locally)
  - [Docker Setup](#docker-setup)
    - [Build and Run with Docker](#build-and-run-with-docker)
    - [Using Docker Compose](#using-docker-compose)
    - [Additional Docker Commands](#additional-docker-commands)
  - [Project Structure and Files Explanation](#project-structure-and-files-explanation)
    - [`blog` Directory](#blog-directory)
      - [`repository` Directory](#repository-directory)
      - [`routers` Directory](#routers-directory)
      - [Other Project Files](#other-project-files)
  - [Environment Variables](#environment-variables)
  - [Contributing](#contributing)
  - [License](#license)

---

## Project Setup

### Prerequisites

Ensure you have the following installed on your machine:

- **Python 3.8+**
- **Docker**
- **Docker Compose**

### Setting Up the Environment

1. Clone this repository:

    ```bash
    git clone https://github.com/Khailas12/FAST-API-Learning.git
    cd FAST-API-Learning
    ```

2. Create a `.env` file in the project root directory. This file will contain sensitive environment variables like `SECRET_KEY`.

    Example `.env` file:

    ```
    SECRET_KEY=your-secret-key-here
    ```

    **Generate a Secret Key**:
    Use the following Python command to generate a random 24-byte hexadecimal string for your `SECRET_KEY`:

    ```bash
    python -c "import os; print(os.urandom(24).hex())"
    ```

    Copy the generated key and paste it into the `SECRET_KEY` field in your `.env` file.

3. **.env is ignored by Git**. You don't need to add this file to GitHub, as it's included in the `.gitignore` file to ensure sensitive data is not shared publicly.

### Install Dependencies

If you are setting up the project locally (without Docker), use the following commands:

1. **Create a virtual environment** (optional but recommended):

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

2. **Install required Python dependencies**:

    ```bash
    pip install -r requirements.txt
    ```

---

### Running the Application Locally

1. **Start the FastAPI application** with Uvicorn:

    ```bash
    uvicorn main.blog:app --reload
    ```

2. Visit `http://localhost:8000` in your browser to view the app. You can access the API documentation at `http://localhost:8000/docs`.

---

## Docker Setup

### Build and Run with Docker

1. **Build the Docker image**:

    To build the Docker image, use the following command:

    ```bash
    sudo docker build -t fastapi-learning:v1.1 .
    ```

    - The `-t` flag tags the image with a name and version. In this case, `fastapi-learning` is the name of the image, and `v1.1` is the version tag. The version tag helps you track different versions of your image, making it easier to manage and update. You can change the version (e.g., `v1.2`, `v2.0`, etc.) to indicate new changes or improvements to your app. Versioning is useful for managing deployments, especially when pushing updates or maintaining multiple environments (like production and staging).
    - The `.` at the end indicates the current directory as the build context, meaning the Docker build will look for the `Dockerfile` and all the necessary files in this directory.

2. **Run the Docker container**:

    Once the image is built, you can run the container using:

    ```bash
    sudo docker run -p 8080:8080 fastapi-learning
    ```

    This command runs the Docker container based on the `fastapi-learning` image, mapping port `8080` on the host to port `8080` in the container. You can access the app by visiting `http://localhost:8080` in your browser.

    **Note**: The container will only reflect the latest state of your code if you rebuild the Docker image using the `docker build` command. If you're actively developing, consider using volume mounting (explained below) to reflect code changes in real-time without rebuilding the image.

---

### Using Docker Compose

You can also use **Docker Compose** to simplify the process of managing your containers. Docker Compose allows you to define and run multi-container Docker applications, making it easier to manage complex setups.

1. **Create a `docker-compose.yml` file** in the project root directory (already provided in the repository).

2. **Start the services with Docker Compose**:

    To build and start the container using Docker Compose, run:

    ```bash
    sudo docker-compose up --build -d
    ```

    - The `--build` flag forces a rebuild of the Docker image before starting the container.
    - The `-d` flag runs the container in detached mode (in the background).
    - This command will use the `docker-compose.yml` file to configure the services and spin up the container, accessible at `http://localhost:8080`.

3. **Stopping the Services**:

    To stop the containers, run:

    ```bash
    sudo docker-compose down
    ```

For a detailed guide on how to containerize your FastAPI application using Docker, I followed the instructions from [this comprehensive guide](https://medium.com/@alidu143/containerizing-fastapi-app-with-docker-a-comprehensive-guide-416521b2457c) on Medium. It covers everything from setting up Dockerfiles to running and managing your application in containers.

Feel free to refer to the article for additional insights and best practices.

---

### Additional Docker Commands

Here are some useful commands for managing Docker containers and images:

- **List running containers**:

    ```bash
    sudo docker ps
    ```

    This command shows a list of currently running containers along with their container IDs, image names, status, and ports.

- **View logs of a specific container**:

    ```bash
    sudo docker logs <app-name>
    ```

    Replace `<app-name>` with the name or container ID of the application you want to view logs for. This helps you monitor the container’s output, including error logs and application logs.

- **Remove unused Docker images**:

    ```bash
    sudo docker image prune
    ```

    This command removes any dangling (unused) images, helping you clean up space on your system. It is safe to run if you want to clear out unused images that are not being referenced by any containers.

---

## Project Structure and Files Explanation

This section provides an overview of the key files and directories in the project. Below is the breakdown of the contents within the `blog` directory and other important project files.

### `blog` Directory

The `blog` directory contains the core application code, including database configuration, models, routes, and utility functions.

- **`database.py`**: Contains the database connection and configuration logic, typically using an ORM like SQLAlchemy to set up the database connection.
- **`hashing.py`**: Handles password hashing and verification using secure hashing algorithms like bcrypt or Argon2.
- **`__init__.py`**: Initializes the `blog` module, making it importable in other parts of the project.
- **`main.py`**: The entry point for the FastAPI application, where the main FastAPI app instance is created and configured.
- **`models.py`**: Defines the database models (SQLAlchemy ORM models), representing the tables in the database (e.g., User, BlogPost).
- **`oauth.py`**: Manages OAuth2 authentication logic, including generating and validating tokens for user authentication.
  
#### `repository` Directory

This directory contains files responsible for interacting with the database models.

- **`auth_repo.py`**: Defines methods to interact with authentication-related database models (e.g., users).
- **`blog_repo.py`**: Contains methods to interact with blog-related database models (e.g., blog posts).
- **`user_repo.py`**: Contains methods to interact with user-related database models.

#### `routers` Directory

The `routers` directory contains the route-handling logic, defining the endpoints for various operations.

- **`auth.py`**: Contains routes for authentication, such as login, registration, and token generation.
- **`blog.py`**: Defines routes for blog-related actions like creating, updating, deleting, and fetching blog posts.
- **`users.py`**: Includes routes related to user management, such as fetching user details or updating user information.

- **`schemas.py`**: Defines the Pydantic schemas used for request validation and response serialization in FastAPI.
- **`utils.py`**: Contains utility functions like token creation, password hashing, and other reusable functions across the project.

---

#### Other Project Files

- **`blog.db`**: SQLite database file that stores all blog-related data, including user information and blog posts.
- **`docker-compose.yml`**: Configuration file for Docker Compose, used to build and run the multi-container Docker application.
- **`Dockerfile`**: Used to build the Docker image for the FastAPI application, specifying the environment and dependencies needed to run the app.
- **`README.md`**: This file, which contains documentation about the project, setup instructions, and usage guidelines.
- **`requirements.txt`**: A file that lists all the Python dependencies needed to run the project, such as FastAPI, SQLAlchemy, and others.

---

## Environment Variables

- `SECRET_KEY`: A secret key used for signing tokens. You should generate a new one and store it in the `.env` file.

---

## Contributing

Feel free to fork the project, make changes, and submit pull requests. All contributions are welcome! Please follow the **PEP 8** guidelines and add tests for new features.

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.