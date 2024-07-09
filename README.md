# HNG Stage Two Backend Task With Django

## Setup

---

## Prerequisites

- Python (3.x recommended)
- Django
- Django REST Framework
- Virtual environment (optional but recommended)

## Installation

1. Clone the repository:

- git clone <repository_url>
- cd employment_contracts

2. Set up a virtual environment (optional but recommended):

- python -m venv venv
- source venv/bin/activate

3. Install dependencies:

- pip install -r requirements.txt

## Database Setup

Using postgresql database

---

- python manage.py makemigrations
- python manage.py migrate

## Running the Server

- python manage.py runserver

## API Endpoints

- create a new user in order to get authorization token to access the api endpoints
- access each endpoint by adding Authorization to your header "Bearer _your_token_"

---

## Access API Endpoints

### Employment Agreements

- List/Create: /api/organisations/
- Retrieve: /api/organisations/<orgId>
- Add user to organisation: /api/organisations/<orgId>/users/
- Retrieve user: /api/users/<userId>

### Authentication

- Signup: /auth/register/
- Login: /auth/login/

## Unit Testing

- python manage.py test
