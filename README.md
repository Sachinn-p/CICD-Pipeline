# Simple FastAPI Application

A basic FastAPI application with SQLite database, comprehensive testing, and complete CI/CD pipeline using GitHub Actions.

## Features

- ✅ FastAPI with SQLAlchemy ORM
- ✅ SQLite database with CRUD operations
- ✅ Comprehensive pytest test suite (12+ tests)
- ✅ GitHub Actions CI/CD pipeline
- ✅ Automated Docker image building and pushing
- ✅ Code quality checks (flake8, black)
- ✅ Security scanning (Bandit)

## Quick Start

### Local Development

1. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`

### Docker

Build and run with Docker:
```bash
docker build -t fastapi-app .
docker run -p 8000:8000 fastapi-app
```

## API Endpoints

- **GET /**: Welcome message
- **GET /items/**: Get all items
- **GET /items/{item_id}**: Get an item by ID
- **POST /items/**: Create a new item
- **PUT /items/{item_id}**: Update an item
- **DELETE /items/{item_id}**: Delete an item
- **GET /health**: Health check endpoint

## Interactive API Documentation

Once the server is running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Testing

Run all tests:
```bash
pytest test.py -v
```

Run specific test:
```bash
pytest test.py::TestItems::test_create_item -v
```

## CI/CD Pipeline

This project includes a complete GitHub Actions CI/CD pipeline that:

1. **Tests** - Runs pytest across Python 3.9, 3.10, 3.11
2. **Security Scan** - Checks code for vulnerabilities
3. **Code Quality** - Validates style with flake8 and black
4. **Build Docker Image** - Creates Docker image after tests pass
5. **Push to Registry** - Pushes image to GitHub Container Registry

See [CI-CD-GUIDE.md](CI-CD-GUIDE.md) for detailed information.

## Docker Image

After pushing to GitHub, Docker images are automatically built and pushed to GitHub Container Registry:

```bash
docker pull ghcr.io/yourusername/cicd-practice:latest
docker run -p 8000:8000 ghcr.io/yourusername/cicd-practice:latest
```

See [DOCKER-GUIDE.md](DOCKER-GUIDE.md) for complete Docker documentation.

## Project Structure

```
CICD-Practice/
├── .github/
│   └── workflows/
│       └── ci-cd.yml          # GitHub Actions workflow
├── main.py                     # FastAPI application
├── test.py                     # Test suite
├── Dockerfile                  # Docker configuration
├── requirements.txt            # Python dependencies
├── .gitignore                  # Git ignore rules
├── .dockerignore               # Docker ignore rules
├── README.md                   # This file
├── CI-CD-GUIDE.md             # CI/CD detailed guide
├── DOCKER-GUIDE.md            # Docker detailed guide
└── QUICKSTART.md              # Quick start guide
```

## Example Usage

### Create an item:
```bash
curl -X POST "http://localhost:8000/items/" \
  -H "Content-Type: application/json" \
  -d '{"name": "Laptop", "price": 999.99, "description": "A powerful laptop"}'
```

### Get all items:
```bash
curl "http://localhost:8000/items/"
```

### Update an item:
```bash
curl -X PUT "http://localhost:8000/items/1" \
  -H "Content-Type: application/json" \
  -d '{"name": "Gaming Laptop", "price": 1299.99, "description": "Updated"}'
```

### Delete an item:
```bash
curl -X DELETE "http://localhost:8000/items/1"
```

## Technologies Used

- **FastAPI** - Modern web framework
- **SQLAlchemy** - ORM for database
- **SQLite** - Lightweight database
- **Pytest** - Testing framework
- **Docker** - Containerization
- **GitHub Actions** - CI/CD automation
- **Flake8** - Code linting
- **Black** - Code formatting
- **Bandit** - Security scanning

## Setup Instructions for GitHub

1. Initialize git:
```bash
git init
git add .
git commit -m "Initial commit"
```

2. Create repository on GitHub

3. Push to GitHub:
```bash
git remote add origin https://github.com/YOUR_USERNAME/CICD-Practice.git
git branch -M main
git push -u origin main
```

4. Watch CI/CD pipeline run in the **Actions** tab

5. After success, Docker image will be available in **Packages** tab

See [QUICKSTART.md](QUICKSTART.md) for step-by-step instructions.

## Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Docker Documentation](https://docs.docker.com/)
- [Pytest Documentation](https://docs.pytest.org/)

## License

MIT License - feel free to use this project as a template

