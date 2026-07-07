# GitHub Actions CI/CD - Quick Reference

## 📁 Files Created

### Workflow Files (`.github/workflows/`)
1. **ci-cd.yml** - Complete CI/CD pipeline with testing, building, deployment, and security
2. **tests.yml** - Simple test runner for multiple Python versions
3. **docker.yml** - Docker image build and push to GitHub Container Registry

### Documentation
4. **README.md** (in workflows/) - Detailed workflow documentation
5. **SETUP.md** - Complete setup guide for GitHub Actions
6. **CI-CD-SUMMARY.md** - This quick reference

### Configuration Files
7. **docker-compose.prod.yml** - Production Docker Compose configuration
8. **nginx.conf** - Nginx reverse proxy configuration
9. **.env.example** - Updated environment variables template
10. **requirements.txt** - Cleaned up Python dependencies

### Scripts
11. **deploy.sh** - Automated deployment script
12. **setup.sh** - Quick setup script for local development

### Contributing
13. **CONTRIBUTING.md** - Contribution guidelines

## 🚀 Quick Start

### 1. Push to GitHub
```bash
git add .
git commit -m "ci: add GitHub Actions CI/CD"
git push origin main
```

### 2. Configure Secrets
Go to **Settings** → **Secrets and variables** → **Actions**

Add these secrets:
- `SERVER_HOST` - Your server IP/hostname
- `SERVER_USER` - SSH username
- `SSH_PRIVATE_KEY` - SSH private key content
- `SERVER_PORT` - SSH port (default: 22)

### 3. Update Workflow
Edit `.github/workflows/ci-cd.yml` line 139:
```yaml
script: |
  cd /path/to/your/app  # ← Change this
```

### 4. View Results
Go to **Actions** tab in your GitHub repository

## 📊 Workflow Overview

| Workflow | Trigger | Purpose |
|----------|---------|---------|
| **CI/CD Pipeline** | Push to main/develop, PRs | Full pipeline with deploy |
| **Tests** | Push, PRs | Quick test feedback |
| **Docker Build** | Push to main, tags | Build & push images |

## 🔧 Common Commands

### View Workflow Status
```bash
# Install GitHub CLI
gh auth login

# List workflows
gh workflow list

# View runs
gh run list

# View specific run
gh run view <run-id>
```

### Manual Trigger
```bash
# Trigger workflow manually
gh workflow run "Docker Build & Push"

# Trigger with inputs
gh workflow run ci-cd.yml --ref main
```

### Pull Docker Images
```bash
# Login to GitHub Container Registry
echo $GITHUB_TOKEN | docker login ghcr.io -u USERNAME --password-stdin

# Pull image
docker pull ghcr.io/USERNAME/REPO:latest

# Run locally
docker run -p 5000:5000 ghcr.io/USERNAME/REPO:latest
```

## 🎯 What Happens on Push

### To `main` or `master` Branch
1. ✅ Run tests (pytest)
2. ✅ Run linting (flake8)
3. ✅ Security scan (Trivy, Safety)
4. ✅ Build Docker image
5. ✅ Push to GitHub Container Registry
6. ✅ Deploy to server (if secrets configured)

### To `develop` Branch
1. ✅ Run tests
2. ✅ Security scan
3. ❌ No build
4. ❌ No deploy

### Pull Requests
1. ✅ Run tests
2. ✅ Security scan
3. ❌ No build
4. ❌ No deploy

## 🔐 Required Secrets (for Deployment)

| Secret | Description | Example |
|--------|-------------|---------|
| `SERVER_HOST` | Server hostname | `192.168.1.100` |
| `SERVER_USER` | SSH user | `ubuntu` |
| `SSH_PRIVATE_KEY` | SSH key | Content of `id_rsa` |
| `SERVER_PORT` | SSH port | `22` (optional) |

## 🐳 Docker Images

Images are automatically tagged:
- `latest` - Latest main branch
- `main` - Main branch
- `sha-<commit>` - Specific commit
- `v1.0.0` - Version tags

## 📝 Status Badges

Add to your README.md:
```markdown
[![Tests](https://github.com/USERNAME/REPO/workflows/Tests/badge.svg)](https://github.com/USERNAME/REPO/actions)
[![CI/CD](https://github.com/USERNAME/REPO/workflows/CI%2FCD%20Pipeline/badge.svg)](https://github.com/USERNAME/REPO/actions)
[![Docker](https://github.com/USERNAME/REPO/workflows/Docker%20Build%20%26%20Push/badge.svg)](https://github.com/USERNAME/REPO/actions)
```

## 🛠️ Customization

### Change Python Version
Edit workflow files:
```yaml
env:
  PYTHON_VERSION: '3.12'  # Change this
```

### Add More Tests
Edit `.github/workflows/ci-cd.yml`:
```yaml
- name: Run integration tests
  run: |
    python -m pytest tests/integration/ -v
```

### Change Deployment Method
Edit deployment job in `ci-cd.yml`:
```yaml
- name: Deploy to Cloud
  # Add your cloud deployment action
  # Examples: aws-actions, azure/webapps-deploy, etc.
```

## 🔍 Troubleshooting

### Tests Failing
```bash
# Run tests locally
python -m pytest tests/ -v

# Check for import errors
python -m pytest tests/ -v --tb=short
```

### Docker Build Failing
```bash
# Test build locally
docker build -t test-app .

# Check Dockerfile syntax
docker build --no-cache -t test-app .
```

### Deployment Failing
```bash
# Test SSH connection
ssh -i ~/.ssh/id_rsa user@server

# Check server logs
ssh user@server "docker-compose logs"
```

## 📚 Resources

- [GitHub Actions Docs](https://docs.github.com/en/actions)
- [Docker Documentation](https://docs.docker.com/)
- [Flask Deployment](https://flask.palletsprojects.com/en/latest/deploying/)
- [Setup Guide](.github/SETUP.md)
- [Contributing](../CONTRIBUTING.md)

## 🎉 Next Steps

- [ ] Configure GitHub Secrets
- [ ] Test workflows with a push
- [ ] Add status badges to README
- [ ] Set up branch protection rules
- [ ] Configure code coverage reporting
- [ ] Add Slack/Discord notifications
- [ ] Set up staging environment
- [ ] Configure monitoring

## 💡 Tips

1. **Test locally first** - Use `act` to run workflows locally
2. **Small commits** - Easier to debug CI failures
3. **Check logs** - Actions tab shows detailed execution logs
4. **Use caching** - Workflows already cache pip dependencies
5. **Branch protection** - Require passing tests before merge
