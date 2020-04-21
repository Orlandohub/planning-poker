# planning-poker <span role="img" aria-label="Joker">🃏</span>

A collaborative planning app - Inspired by Polly, a Slack third party app for creating polls all integrated on chat channels.


## Run Project

**Backend**
```bash
docker-compose up -d --build
```

**Tests**
```bash
docker-compose exec backend python run_tests.py
```

**Frontend**
```bash
cd frontend/app
yarn install
yarn start
```

## Docs

```
http://localhost:8000/docs
```

This will display an interactive api powered by openapi. All endpoints are avaible with
necessary info on what data schemas each requires.
It's also possible to create user and auth to access protected endpoints

```
http://localhost:8000/redoc
```

A less interactive API documentation but usefull to understand what are the
available endpoints and data schemas


## Tech Stack

- Backend
    - FastApi (Flask like ASGI Python server)
    - MongoDB
- Frontend
    - React


## To Do's

- Frontend tests (E2E, Integration, Unit)
- Set env variables more securely over .env files
- Improve UI on poll view


## Usage

1. Register a user
2. Register a second user on a different browser
3. Message each other on main Home chat
4. Interact with tasks and votes with the slash commands
5. Create a new poll
