# MathWS  
  
**MathWS** — asynchronous API for a real-time math solving game.
  
---  
  
## Description  
  
**MathWS** is the backend (server-side) for the game. It allows users to create and participate in math sessions, solve problems, and compete with others in real-time.  
The API is built with FastAPI, featuring asynchronous database access and authentication via JWT and cookies.
  
---  
  
## Features

- **User Registration & Authorization:** Secure login using JWT.
- **WebSocket Authentication:** Cookie-based auth for secure WebSocket connections.
- **Async Database:** Fully asynchronous database operations.
- **Real-time Updates:** Instant data synchronization via WebSockets.
- 
---  
  
## Tech Stack

| Category | Technology |
| :--- | :--- |
| **Backend** | FastAPI, SQLModel, Alembic |
| **Database** | PostgreSQL |
| **Auth** | JWT, OAuth2, Cookies |
| **Async** | asyncio, SQLAlchemy AsyncSession |

---  
  
## Installation and Setup

### 1. Clone the repository
```bash
git clone https://github.com/NayTmk/MathWS
cd backend
```

### 2. Create a .env file
Create a .env file. Copy the example and configure the variables:
```bash
cp env_example .env
```

### 3. (Optional) Local setup without Docker
```bash
python -m venv venv
source venv/bin/activate  # Linux / macOS
venv\Scripts\activate     # Windows
pip install -r requirements.txt
```
> However, I recommend running it via Docker — see the main commands below.

### 4. Check Docker and Docker Compose

Verify Docker installation:
```bash
docker --version
docker compose version   # // docker-compose --version
```

### 5. Running via Docker (Recommended)
In the root directory:
```bash
docker compose up --build
```
Or run in the background:
```bash
docker compose up --build -d
```

### 6. Check status
- OpenAPI Documentation: [http://localhost:8000/docs](http://localhost:8000/docs)
- Game page: [http://localhost:8000/game](http://localhost:8000/game)
- Adminer if enabled in docker-compose: [http://localhost:8080](http://localhost:8080)

### 7. Database Migrations (Local Setup)
```bash
alembic upgrade head
```

### 8. Stopping and Cleanup
```bash
docker compose down
# with volumes and images removal
docker compose down --volumes --rmi local
```