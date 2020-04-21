# planning-poker <span role="img" aria-label="Joker">🃏</span>

A collaborative planning app based on chat polls.


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

## Usage

1. Register a user
2. Register a second user on a different browser
3. Message each other on main Home chat
4. Interact with tasks and votes with the slash commands
5. Create a new poll


