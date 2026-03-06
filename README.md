# Full-Stack Project

A full-stack web application with a React frontend and a FastAPI backend.

## Tech Stack

### Frontend (`frontend/`)

| Technology   | Purpose              |
| ------------ | -------------------- |
| React 18     | UI library           |
| Vite         | Build tool & dev server |
| TypeScript   | Type safety          |
| Zustand      | State management     |
| React Router | Client-side routing  |
| Axios        | HTTP client          |
| Less         | CSS preprocessor     |
| ESLint       | Linting              |

### Backend (`backend/`)

| Technology | Purpose             |
| ---------- | ------------------- |
| Python 3.12 | Runtime             |
| FastAPI    | Web framework        |
| Pydantic   | Data validation      |
| SQLModel   | ORM (SQLAlchemy)     |
| PyJWT      | JWT authentication   |
| uv         | Package manager      |

## Project Structure

```
.
├── frontend/                # React frontend
│   ├── src/
│   │   ├── components/      # Reusable UI components
│   │   ├── pages/           # Page-level components
│   │   ├── stores/          # Zustand state stores
│   │   ├── styles/          # Global styles & Less variables
│   │   ├── types/           # TypeScript type definitions
│   │   ├── utils/           # Utility functions (axios, etc.)
│   │   ├── App.tsx          # Root component with routing
│   │   └── main.tsx         # Entry point
│   ├── eslint.config.js
│   ├── tsconfig.json
│   ├── vite.config.ts
│   └── package.json
├── backend/                 # FastAPI backend
│   ├── app/
│   │   ├── api/             # API routes
│   │   │   └── endpoints/   # Route handlers
│   │   ├── core/            # Config, database, security, deps
│   │   ├── models/          # SQLModel database models
│   │   ├── schemas/         # Pydantic request/response schemas
│   │   └── services/        # Business logic
│   ├── tests/               # Test suite
│   ├── pyproject.toml       # Python project config & dependencies
│   └── .python-version      # Pinned Python version (3.12.12)
└── README.md
```

## Getting Started

### Prerequisites

- [Node.js](https://nodejs.org/) >= 18
- [uv](https://docs.astral.sh/uv/) (Python package manager)

### Backend

```bash
cd backend

# Install dependencies (uv will auto-create a virtualenv)
uv sync

# Copy environment variables
cp .env.example .env

# Run the development server
uv run uvicorn app.main:app --reload
```

The API will be available at **http://localhost:8000**.
Interactive API docs at **http://localhost:8000/docs**.

### Frontend

```bash
cd frontend

# Install dependencies
npm install

# Run the development server
npm run dev
```

The app will be available at **http://localhost:5173**.
API requests are proxied to the backend via Vite's dev server proxy.

### Running Tests

```bash
# Backend tests
cd backend
uv run pytest

# Frontend lint
cd frontend
npm run lint
```

## API Endpoints

| Method | Path                  | Description         |
| ------ | --------------------- | ------------------- |
| GET    | `/health`             | Health check        |
| POST   | `/api/v1/auth/register` | Register a new user |
| POST   | `/api/v1/auth/login`    | Login & get JWT     |
| GET    | `/api/v1/auth/me`       | Get current user    |

## License

See [LICENSE](./LICENSE) for details.
