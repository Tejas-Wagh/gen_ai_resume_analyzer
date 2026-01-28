# Backend AI Resume Analyzer

A FastAPI-based backend service for analyzing resumes using generative AI capabilities. The project uses Redis for caching and async task processing with a worker service.

## Project Structure

```
.
├── backend/           # FastAPI application
├── worker/            # Async task worker
├── docker-compose.yml # Docker Compose configuration
└── README.md         # This file
```

## Prerequisites

- Python 3.13+
- Docker & Docker Compose
- Redis 7+

## Installation

### Local Development

1. Clone the repository
```bash
git clone <repo-url>
cd generative-ai
```

2. Create virtual environment for backend
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies
```bash
pip install -e .
```

4. Set up environment variables
```bash
cp .env.example .env
# Edit .env with your configuration
```

### Using Docker Compose

1. Build and start services
```bash
docker-compose up --build
```

2. Services will be available at:
   - API: `http://localhost:8000`
   - Redis: `localhost:6379`

## Configuration

### Environment Variables

Create a `.env` file in the backend directory:

```env
# Database
DATABASE_URL=postgresql://user:password@localhost/dbname

# AWS S3 (if using)
AWS_ACCESS_KEY_ID=your_key
AWS_SECRET_ACCESS_KEY=your_secret
AWS_REGION=us-east-1

# Redis
REDIS_HOST=localhost
REDIS_PORT=6379

# JWT
SECRET_KEY=your_secret_key_here
ALGORITHM=HS256
```

## Running the Application

### Development

```bash
cd backend
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Production (Docker)

```bash
docker-compose up -d
```

## API Documentation

Once the application is running, visit:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Dependencies

- **FastAPI** - Modern web framework
- **SQLAlchemy** - ORM for database operations
- **Alembic** - Database migrations
- **Redis** - Caching & async task queue
- **Boto3** - AWS S3 integration
- **python-jose** - JWT token handling
- **Pydantic** - Data validation

## Development

### Running Tests

```bash
cd backend
pytest
```

### Database Migrations

```bash
alembic upgrade head  # Apply migrations
alembic revision --autogenerate -m "Description"  # Create new migration
```

## Docker Services

### API Service
- Port: 8000
- Built from: `./backend`
- Dependencies: Redis

### Worker Service
- Built from: `./worker`
- Dependencies: Redis

### Redis Service
- Image: redis:7
- Port: 6379

## Troubleshooting

### uvicorn spawn error
If you get "Failed to spawn: uvicorn" error:
1. Ensure all dependencies are installed
2. Use `python -m uvicorn` instead of just `uvicorn`
3. Check Docker build logs: `docker-compose logs app`

### Redis connection issues
1. Verify Redis is running: `docker-compose ps`
2. Check environment variables are set correctly
3. Ensure REDIS_HOST and REDIS_PORT match service configuration

## Contributing

1. Create a feature branch
2. Make your changes
3. Submit a pull request

## License

[Add your license here]
