# Social Media API

This project is a Social Media API designed to handle user authentication, searching for users, sending friend requests and much more. The API is built using modern web development technologies to ensure scalability, performance, and security.

## Use Case

The Social Media API serves as the backend for a social networking platform. It supports features such as user registration, login, searching other users, creating friends by sending friend requests, updating friend request statuses, see friends, etc. This API can be used as the backbone for any social media application, providing all necessary endpoints to support core social media functionalities.

## Features

- User Authentication using JWT
- Searching Users
- Creating Friends
- Sending / Updating Friend Requests
- See Current Friends

## Installation

### Prerequisites

- Docker
- Docker Compose

### Steps

1. **Clone the Repository:**

    ```bash
    git clone https://github.com/Krish2958/Social.git
    cd Social
    ```

2. **Build and Run the Docker Container:**

    Use Docker Compose to build and run the application.

    ```bash
    docker-compose up --build
    ```

3. **Run the Application:**

    To start the application, use:

    ```bash
    docker-compose up
    ```

    The API should now be running on `http://127.0.0.1:8000`.

## API Documentation

### Postman

- **Postman Collection:** [Postman Collection URL](https://api.postman.com/collections/19968073-7ebe3b55-b7f0-44d1-9741-4812a171e518?access_key=PMAT-01J0JWAYYGAWBYDCWHEQYHN9TD)

- **Postman Documentation:** [Postman Collection Docs URL](https://documenter.getpostman.com/view/19968073/2sA3XSA17X) 

### Swagger

To test the API using Swagger, navigate to:

- **Swagger Documentation:** [http://127.0.0.1:8000/documentation/](http://127.0.0.1:8000/documentation/)

## Endpoints

The API exposes various endpoints to handle different functionalities. Here are some of the main endpoints:

- **User Registration:** `POST` `/api/users/register/`
- **User Login:** `POST` `/api/users/login/`
- **Search User** `GET` `/api/users/search/?search="YOUR_SEARCH_KEYWORD"`
- **Show Friends** `GET` `/api/users/friends`
- **See Pending Friend Requests** `GET` `api/users/pending_requests`
- **Send Friend Request** `POST` `api/friend-requests/{USER_ID}/send_request/`
- **Update Friend Request** `POST` `api/friend-requests/{FRIEND_REQUEST_ID}/update_request/`




---

For any questions or issues, please open an issue in the repository or contact [me](https://krishmaheshwari.carrd.co).

---

Thank you for using the Social Media API!