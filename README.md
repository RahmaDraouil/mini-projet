# Employee Management System

[![Tests](https://github.com/username/repo/workflows/Tests/badge.svg)](https://github.com/username/repo/actions)
[![CI/CD](https://github.com/username/repo/workflows/CI%2FCD%20Pipeline/badge.svg)](https://github.com/username/repo/actions)
[![Docker](https://github.com/username/repo/workflows/Docker%20Build%20%26%20Push/badge.svg)](https://github.com/username/repo/actions)

A complete full-stack web application for managing employees built with Python Flask, MySQL, and Bootstrap.

## Features

- **CRUD Operations**: Create, Read, Update, and Delete employees
- **Modern UI**: Responsive dashboard with Bootstrap 5
- **RESTful API**: JSON endpoints for integration
- **Input Validation**: Server-side validation with error handling
- **Docker Support**: Containerized deployment with Docker Compose
- **CI/CD**: GitHub Actions pipelines for automated testing and deployment
- **Unit Tests**: Comprehensive test coverage with pytest

## Tech Stack

- **Backend**: Python Flask
- **Database**: MySQL 8.0
- **ORM**: SQLAlchemy
- **Frontend**: HTML, CSS, Bootstrap 5
- **Containerization**: Docker & Docker Compose
- **Testing**: pytest
- **Security**: Bandit

## Project Structure

```
project/
│── app.py                 # Application entry point
│── config.py              # Configuration settings
│── requirements.txt       # Python dependencies
│── Dockerfile             # Docker configuration
│── docker-compose.yml     # Multi-container setup
│── deploy.sh              # Deployment script
│── .gitlab-ci.yml         # CI/CD pipeline
│── .env.example           # Environment template
│── models/
│   │── __init__.py
│   │── database.py        # Database initialization
│   └── employee.py        # Employee model
│── routes/
│   │── __init__.py
│   └── employee_routes.py # Employee routes
│── templates/
│   │── base.html          # Base template
│   │── index.html         # Dashboard
│   │── add_employee.html  # Add form
│   └── edit_employee.html # Edit form
│── static/
│   │── css/
│   │   └── style.css      # Custom styles
│   └── js/
│       └── script.js      # JavaScript
└── tests/
    │── __init__.py
    │── conftest.py        # Test fixtures
    └── test_employee.py   # Employee tests
```

## Quick Start

### Using Docker (Recommended)

1. Clone the repository:
```bash
git clone <repository-url>
cd project
```

2. Create environment file:
```bash
cp .env.example .env
```

3. Start the application:
```bash
docker-compose up -d
```

4. Access the application at `http://localhost:5000`

### Manual Setup

1. Install Python 3.11+

2. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up MySQL database:
```sql
CREATE DATABASE employee_db;
CREATE USER 'user'@'localhost' IDENTIFIED BY 'password';
GRANT ALL PRIVILEGES ON employee_db.* TO 'user'@'localhost';
```

5. Configure environment variables:
```bash
cp .env.example .env
# Edit .env with your database credentials
```

6. Run the application:
```bash
python app.py
```

## API Endpoints

- `GET /` - Dashboard with employee list
- `GET /employee/add` - Add employee form
- `POST /employee/add` - Create new employee
- `GET /employee/edit/<id>` - Edit employee form
- `POST /employee/edit/<id>` - Update employee
- `POST /employee/delete/<id>` - Delete employee
- `GET /api/employees` - Get all employees (JSON)
- `GET /api/employee/<id>` - Get single employee (JSON)

## Running Tests

```bash
pytest tests/ -v
```

## Security Scan

```bash
bandit -r . -f txt
```

## CI/CD Pipeline

### GitHub Actions Workflows

The project includes three GitHub Actions workflows:

#### 1. Complete CI/CD Pipeline (`ci-cd.yml`)
Runs on push to main/master/develop branches and pull requests:
- **Test Job**: Linting, unit tests, coverage reports
- **Build Job**: Docker image build and push to GitHub Container Registry
- **Deploy Job**: Automated deployment via SSH (requires secrets)
- **Security Job**: Vulnerability scanning with Trivy and Safety

#### 2. Simple Tests (`tests.yml`)
Fast test execution across multiple Python versions (3.10, 3.11, 3.12)

#### 3. Docker Build (`docker.yml`)
Multi-platform Docker image builds (amd64, arm64) with automatic tagging

### Setting Up CI/CD

1. **Enable GitHub Actions** (enabled by default for public repos)

2. **Configure Deployment Secrets** (Settings → Secrets → Actions):
   - `SERVER_HOST`: Your server hostname
   - `SERVER_USER`: SSH username  
   - `SSH_PRIVATE_KEY`: SSH private key
   - `SERVER_PORT`: SSH port (optional)

3. **Pull Docker Images**:
```bash
docker pull ghcr.io/<username>/<repo>:latest
```

4. **View Workflow Status**: Check the Actions tab in your repository

For detailed CI/CD documentation, see [`.github/workflows/README.md`](.github/workflows/README.md)

## Legacy CI/CD (GitLab)

The GitLab CI/CD pipeline (`.gitlab-ci.yml`) includes:

1. **Build Stage**: Install dependencies
2. **Test Stage**: Run pytest
3. **Security Stage**: Run Bandit security scan
4. **Deploy Stage**: Deploy to production (manual trigger)

## Environment Variables

- `SECRET_KEY`: Flask secret key
- `DATABASE_URL`: MySQL connection string
- `DEBUG`: Debug mode (True/False)

## Production Deployment

1. Update `.env` with production values
2. Run deployment script:
```bash
chmod +x deploy.sh
./deploy.sh
```

## License

MIT License

## Contributing

Pull requests are welcome. For major changes, please open an issue first.
