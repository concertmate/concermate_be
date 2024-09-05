# ConcertMate Backend (concermate_be)

Welcome to the backend repository of **ConcertMate**, an app designed to help users find upcoming concerts, and invite friends to go to concerts together. This backend is built with **Python** and **Django**, providing the API and logic that powers the ConcertMate app.

## Table of Contents

- [Installation](#installation)
- [Technologies Used](#technologies-used)
- [Environment Variables](#environment-variables)
- [Database Setup](#database-setup)
- [Running the Application](#running-the-application)
- [Endpoints](#endpoints)
- [Deployment](#deployment)
- [Testing](#testing)
- [Contributing](#contributing)
- [License](#license)

## Installation

To get started, follow the instructions below to set up the backend locally:

1. **Clone the repository**:

    ```bash
    git clone https://github.com/concertmate/concermate_be.git
    cd concermate_be
    ```

2. **Set up a virtual environment**:

    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3. **Install dependencies**:

    ```bash
    pip install -r requirements.txt
    ```

## Technologies Used

- **Django**: The web framework used to build the backend of ConcertMate.
- **SQLite**: The lightweight database used for local development.

## Database Setup

 **Apply Migrations**:

  ```bash
  python manage.py migrate
  ```


## Running the Application

To run the server locally, execute the following command:

```bash
python manage.py runserver
```

This will start the backend server at `http://127.0.0.1:8000/`.

## Endpoints

### 1. **Create Event**

- **Endpoint**: `api/users/:user_id/events/create`
- **Method**: `POST`
- **Description**: Create new event for a user.

#### Example Request:

```bash
POST api/users/1/events/create

{
    "event_name": "Bluegrass Week",
    "venue_name": "San Antonio Fair",
    "date_time": "2024-12-31T20:00:00Z",
    "artist": "Marty Robbins",
    "location": "San Antonio, TX",
    "spotify_artist_id": "2341",
    "ticketmaster_event_id": "921"
}
```

#### Example Response:

```json
{
    "data": {
        "event_id": 3,
        "event_name": "Bluegrass Week",
        "venue_name": "San Antonio Fair",
        "date_time": "2024-12-31T20:00:00Z",
        "artist": "Marty Robbins",
        "location": "San Antonio, TX",
        "spotify_artist_id": "2341",
        "ticketmaster_event_id": "921",
        "owner": "newuser"
    }
}
```

### 2. **User Join Event**

- **Endpoint**: `api/users/:user_id/events/:event_id/join`
- **Method**: `POST`
- **Description**: User to join an event.

#### Example Request:

```bash
POST api/users/1/events/2/join
```

#### Example Response:

```json
{
    "data": {
        "event_id": 2,
        "event_name": "Bluegrass Week",
        "venue_name": "San Antonio Fair",
        "date_time": "2024-12-31T20:00:00Z",
        "artist": "Marty Robbins",
        "location": "San Antonio, TX",
        "spotify_artist_id": "2341",
        "ticketmaster_event_id": "921",
        "owner": "newuser"
    }
}
```

### 3. **All Users Attending Event**

- **Endpoint**: `api/events/:event_id/attendees`
- **Method**: `GET`
- **Description**: Get all users attending specific event.

#### Example Request:

```bash
GET api/events/2/attendees
```

#### Example Response:

```json
{
    "data": [
    {
        "user_id": 3,
        "username": "usernamegood",
        "email": "usernamegood@yesgoodemail.com"
    }
  ]
}
```

### 4. **User Leave Event**

- **Endpoint**: `api/users/:user_id/events/:event_id/leave`
- **Method**: `POST`
- **Description**: Leave event.

#### Example Request:

```bash
POST api/users/1/events/2/leave
```

#### Example Response:

```json
{'message': 'User has left the event'}
```

### 5. **Get All User's Events**

- **Endpoint**: `/api/users/:user_id/events`
- **Method**: `GET`
- **Description**: Retrieves a list of the user's events.

#### Example Request:

```bash
GET /api/users/1/events
```

#### Example Response:

```json
{
    "events": [
        {
            "event_id": 3,
            "event_name": "Bluegrass Week",
            "venue_name": "San Antonio Fair",
            "date_time": "2024-12-31T20:00:00Z",
            "artist": "Marty Robbins",
            "location": "San Antonio, TX",
            "spotify_artist_id": "2341",
            "ticketmaster_event_id": "921",
            "owner": "newuser"
        }
    ]
}
```

### 6. **Get One User Event**

- **Endpoint**: `api/users/:user_id/events/:event_id`
- **Method**: `GET`
- **Description**: Retrieves one user event.

#### Example Request:

```bash
GET api/users/1/events/2
```

#### Example Response:

```json
{
    "data": {
        "event_id": 2,
        "event_name": "Bluegrass Week",
        "venue_name": "San Antonio Fair",
        "date_time": "2024-12-31T20:00:00Z",
        "artist": "Marty Robbins",
        "location": "San Antonio, TX",
        "spotify_artist_id": "2341",
        "ticketmaster_event_id": "921",
        "owner": "newuser"
    }
}
```

### 7. **Create User**

- **Endpoint**: `api/users/create`
- **Method**: `POST`
- **Description**: Create new user.

#### Example Request:

```bash
POST api/users/create

{
    "username": "usernamegood",
    "password": "strongpassword",
    "email": "usernamegood@yesgoodemail.com"
}

```

#### Example Response:

```json
{
    "data": {
        "user_id": 4,
        "username": "usernamegood",
        "email": "usernamegood@yesgoodemail.com"
    }
}
```

## Testing

To run the test suite, simply use:

```bash
python manage.py test
```

## Contributors

- **Garrett Bowman**  
  [LinkedIn](https://www.linkedin.com/in/gbowman3/) | [GitHub](https://github.com/GBowman1)

- **Rodrigo Chavez**  
  [LinkedIn](https://www.linkedin.com/in/rodrigo-chavez1/) | [GitHub](https://github.com/RodrigoACG)

- **Clyde Autin**  
  [LinkedIn](https://www.linkedin.com/in/clydeautin/) | [GitHub](https://github.com/clydeautin)

- **Zach Bergman**  
  [LinkedIn](https://www.linkedin.com/in/zacherybergman/) | [GitHub](https://github.com/zach-bergman)
