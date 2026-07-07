# GitHub Actions Workflows

This directory contains CI/CD workflows for the Employee Management System.

## Available Workflows

### 1. `ci-cd.yml` - Complete CI/CD Pipeline
**Triggers:** Push to main/master/develop, Pull requests to main/master

**Jobs:**
- **Test**: Runs unit tests, linting, and generates coverage reports
- **Build**: Builds and pushes Docker image to GitHub Container Registry
- **Deploy**: Deploys to server via SSH (requires secrets configuration)
- **Security**: Runs security scans (Trivy, Safety)

**Required Secrets for Deployment:**
- `SERVER_HOST`: Your server hostname or IP
- `SERVER_USER`: SSH username
- `SSH_PRIVATE_KEY`: SSH private key for authentication
- `SERVER_PORT`: SSH port (optional, defaults to 22)

### 2. `tests.yml` - Simple Test Runner
**Triggers:** Push to main/master/develop, Pull requests

**Features:**
- Tests against multiple Python versions (3.10, 3.11, 3.12)
- Fast feedback for code changes
- No deployment steps

### 3. `docker.yml` - Docker Build & Push
**Triggers:** Push to main/master, version tags (v*), manual dispatch

**Features:**
- Builds multi-platform images (amd64, arm64)
- Pushes to GitHub Container Registry
- Automatic versioning based on tags/commits
- Build provenance attestation

## Setup Instructions

### 1. Enable GitHub Actions
GitHub Actions is enabled by default for public repositories. For private repos, go to:
Settings → Actions → General → Allow all actions

### 2. Configure Secrets (for deployment)
Go to: Settings → Secrets and variables → Actions → New repository secret

Add the following secrets:
```
SERVER_HOST=your-server.com
SERVER_USER=deploy-user
SSH_PRIVATE_KEY=<your-private-key-content>
SERVER_PORT=22
```

### 3. Enable GitHub Container Registry
The workflows automatically push Docker images to `ghcr.io`. Images will be at:
```
ghcr.io/<your-username>/<your-repo>:latest
```

To pull images locally:
```bash
echo $GITHUB_TOKEN | docker login ghcr.io -u <username> --password-stdin
docker pull ghcr.io/<your-username>/<your-repo>:latest
```

### 4. Customize Deployment (Optional)
Edit the `deploy` job in `ci-cd.yml` to match your deployment method:
- Docker Compose (current setup)
- Kubernetes
- Cloud platforms (AWS, Azure, GCP)
- PaaS (Heroku, Render, etc.)

## Workflow Status Badges

Add these to your main README.md:

```markdown
![Tests](https://github.com/<username>/<repo>/workflows/Tests/badge.svg)
![CI/CD](https://github.com/<username>/<repo>/workflows/CI%2FCD%20Pipeline/badge.svg)
![Docker](https://github.com/<username>/<repo>/workflows/Docker%20Build%20%26%20Push/badge.svg)
```

## Local Testing

Test your workflows locally using [act](https://github.com/nektos/act):

```bash
# Install act
brew install act  # macOS
choco install act-cli  # Windows

# Run workflows locally
act push
act pull_request
```

## Troubleshooting

### Tests failing
- Check Python version compatibility
- Verify all dependencies in requirements.txt
- Review test output in Actions tab

### Docker build failing
- Check Dockerfile syntax
- Verify base image availability
- Review build logs for dependency issues

### Deployment failing
- Verify SSH credentials are correct
- Check server accessibility
- Ensure Docker and Docker Compose are installed on server
- Verify deployment path exists

## Best Practices

1. **Branch Protection**: Enable branch protection rules requiring status checks to pass
2. **Code Review**: Require pull request reviews before merging
3. **Secrets Management**: Never commit secrets, always use GitHub Secrets
4. **Caching**: Workflows use pip caching for faster builds
5. **Security**: Regular security scans help identify vulnerabilities early
