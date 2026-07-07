# Contributing to Employee Management System

Thank you for considering contributing to this project! This document outlines the process for contributing.

## Code of Conduct

- Be respectful and inclusive
- Welcome newcomers and help them learn
- Focus on constructive feedback
- Respect differing viewpoints and experiences

## How to Contribute

### Reporting Bugs

Before creating a bug report:
1. Check existing issues to avoid duplicates
2. Collect information about the bug (OS, Python version, error messages)
3. Create a minimal reproducible example

When filing a bug report, include:
- Clear, descriptive title
- Steps to reproduce
- Expected vs actual behavior
- Screenshots (if applicable)
- Environment details

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues:
1. Use a clear, descriptive title
2. Provide detailed description of the proposed feature
3. Explain why this enhancement would be useful
4. Provide examples of how it would work

### Pull Requests

1. **Fork the repository**
```bash
gh repo fork username/repository
```

2. **Create a feature branch**
```bash
git checkout -b feature/amazing-feature
```

3. **Make your changes**
   - Follow the code style guidelines
   - Add tests for new functionality
   - Update documentation as needed

4. **Test your changes**
```bash
# Run tests
python -m pytest tests/ -v

# Run linting
flake8 .

# Check code formatting
black --check .
```

5. **Commit your changes**
```bash
git commit -m "feat: add amazing feature"
```

Follow [Conventional Commits](https://www.conventionalcommits.org/):
- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation changes
- `style:` Code style changes (formatting)
- `refactor:` Code refactoring
- `test:` Test changes
- `chore:` Build process or auxiliary tool changes

6. **Push to your fork**
```bash
git push origin feature/amazing-feature
```

7. **Open a Pull Request**
   - Fill in the PR template
   - Link related issues
   - Request review from maintainers

## Development Setup

### Prerequisites
- Python 3.11+
- Docker & Docker Compose (optional)
- Git

### Setup Development Environment

```bash
# Clone repository
git clone https://github.com/username/repository.git
cd repository

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install development dependencies
pip install pytest pytest-cov flake8 black isort

# Setup pre-commit hooks (optional)
pip install pre-commit
pre-commit install

# Run tests
python -m pytest tests/ -v
```

### Using Docker

```bash
# Build and run
docker-compose up --build

# Run tests in container
docker-compose exec web python -m pytest tests/ -v
```

## Code Style Guidelines

### Python Style
- Follow [PEP 8](https://pep8.org/)
- Use 4 spaces for indentation
- Maximum line length: 127 characters
- Use meaningful variable names
- Add docstrings to functions and classes

### Code Formatting
```bash
# Format code with Black
black .

# Sort imports with isort
isort .

# Lint with flake8
flake8 .
```

### Example Code Style

```python
def calculate_employee_bonus(employee: Employee, performance_rating: float) -> float:
    """
    Calculate bonus for an employee based on performance rating.
    
    Args:
        employee: Employee object
        performance_rating: Rating from 0.0 to 5.0
        
    Returns:
        Calculated bonus amount
        
    Raises:
        ValueError: If performance_rating is out of range
    """
    if not 0.0 <= performance_rating <= 5.0:
        raise ValueError("Performance rating must be between 0.0 and 5.0")
    
    base_bonus = employee.salary * 0.1
    return base_bonus * (performance_rating / 5.0)
```

## Testing Guidelines

### Writing Tests
- Write tests for all new features
- Maintain or improve code coverage
- Use descriptive test names
- Follow AAA pattern: Arrange, Act, Assert

### Test Structure
```python
def test_employee_creation_success():
    """Test successful employee creation with valid data."""
    # Arrange
    employee_data = {
        'full_name': 'John Doe',
        'email': 'john@example.com',
        'department': 'Engineering',
        'salary': 75000.00
    }
    
    # Act
    employee = Employee(**employee_data)
    
    # Assert
    assert employee.full_name == 'John Doe'
    assert employee.email == 'john@example.com'
```

### Running Tests
```bash
# Run all tests
python -m pytest tests/ -v

# Run specific test file
python -m pytest tests/test_employee.py -v

# Run with coverage
python -m pytest tests/ --cov=. --cov-report=html

# View coverage report
open htmlcov/index.html
```

## Documentation

### Code Comments
- Comment complex logic
- Avoid obvious comments
- Keep comments up-to-date with code changes

### Docstrings
Use Google-style docstrings:

```python
def process_employee_data(data: dict) -> Employee:
    """
    Process and validate employee data.
    
    Args:
        data: Dictionary containing employee information
              with keys: full_name, email, department, salary
    
    Returns:
        Employee object with validated data
    
    Raises:
        ValidationError: If data validation fails
        
    Example:
        >>> data = {'full_name': 'Jane Doe', ...}
        >>> employee = process_employee_data(data)
    """
    pass
```

### README Updates
Update README.md when adding:
- New features
- New dependencies
- Configuration changes
- API endpoint changes

## Git Workflow

### Branch Naming
- `feature/description` - New features
- `bugfix/description` - Bug fixes
- `hotfix/description` - Urgent fixes
- `docs/description` - Documentation updates
- `refactor/description` - Code refactoring

### Commit Messages
Good commit message:
```
feat: add employee search functionality

- Add search endpoint to API
- Implement search form in UI
- Add tests for search feature

Closes #123
```

Bad commit message:
```
fixed stuff
```

## Review Process

### For Contributors
- Be patient and responsive to feedback
- Be open to suggestions
- Make requested changes promptly
- Ask questions if feedback is unclear

### For Reviewers
- Review code promptly
- Be constructive and respectful
- Explain the reasoning behind suggestions
- Approve when all concerns are addressed

## CI/CD Pipeline

All pull requests trigger:
1. **Automated tests** - Must pass
2. **Code linting** - Should pass
3. **Security scan** - Review warnings
4. **Build check** - Must succeed

Failed checks will block merging.

## Release Process

1. Update version in `app.py` or `__init__.py`
2. Update CHANGELOG.md
3. Create release PR
4. Tag release: `git tag -a v1.0.0 -m "Release v1.0.0"`
5. Push tag: `git push origin v1.0.0`
6. GitHub Actions will build and deploy

## Getting Help

- **Questions**: Open a discussion on GitHub
- **Bugs**: File an issue with details
- **Chat**: Join our Discord/Slack (if available)
- **Email**: contact@example.com

## Recognition

Contributors will be:
- Listed in CONTRIBUTORS.md
- Mentioned in release notes
- Given credit in the README

Thank you for contributing! 🎉
