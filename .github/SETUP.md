# GitHub Actions CI/CD Setup Guide

Complete guide for setting up continuous integration and deployment using GitHub Actions.

## Prerequisites

- GitHub repository with the project code
- Server with SSH access (for deployment)
- Docker and Docker Compose installed on deployment server
- GitHub account with repository admin access

## Step-by-Step Setup

### Step 1: Enable GitHub Actions

1. Go to your repository on GitHub
2. Click **Settings** → **Actions** → **General**
3. Under "Actions permissions", select **Allow all actions and reusable workflows**
4. Click **Save**

### Step 2: Configure Repository Secrets

Secrets are required for deployment. Add them in your repository:

1. Go to **Settings** → **Secrets and variables** → **Actions**
2. Click **New repository secret**
3. Add the following secrets:

| Secret Name | Description | Example |
|-------------|-------------|---------|
| `SERVER_HOST` | Your server IP or hostname | `192.168.1.100` or `example.com` |
| `SERVER_USER` | SSH username | `ubuntu` or `deploy` |
| `SSH_PRIVATE_KEY` | SSH private key content | Content of `~/.ssh/id_rsa` |
| `SERVER_PORT` | SSH port (optional) | `22` |

#### Generating SSH Keys

If you don't have SSH keys:

```bash
# On your local machine
ssh-keygen -t ed25519 -C "github-actions@your-repo"

# Copy the public key to your server
ssh-copy-id -i ~/.ssh/id_ed25519.pub user@server

# Copy private key content for GitHub secret
cat ~/.ssh/id_ed25519
```

### Step 3: Update Deployment Configuration

Edit `.github/workflows/ci-cd.yml` deployment section:

```yaml
- name: Deploy to server via SSH
  uses: appleboy/ssh-action@v1.0.0
  with:
    host: ${{ secrets.SERVER_HOST }}
    username: ${{ secrets.SERVER_USER }}
    key: ${{ secrets.SSH_PRIVATE_KEY }}
    port: ${{ secrets.SERVER_PORT || 22 }}
    script: |
      cd /opt/employee-management  # Update this path
      git pull origin main
      docker-compose down
      docker-compose pull
      docker-compose up -d
```

### Step 4: Prepare Deployment Server

SSH into your server and prepare the environment:

```bash
# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Clone repository
cd /opt
sudo git clone https://github.com/yourusername/yourrepo.git employee-management
cd employee-management

# Create .env file
cp .env.example .env
nano .env  # Edit with your configuration

# Give deployment user permissions
sudo chown -R $USER:$USER /opt/employee-management
```

### Step 5: Test GitHub Actions Locally (Optional)

Install `act` to test workflows locally:

```bash
# macOS
brew install act

# Linux
curl https://raw.githubusercontent.com/nektos/act/master/install.sh | sudo bash

# Windows
choco install act-cli

# Run tests locally
act push
```

### Step 6: Push Code and Trigger Workflow

```bash
git add .
git commit -m "Add GitHub Actions CI/CD"
git push origin main
```

Visit your repository's **Actions** tab to see the workflow running.

## Workflow Behaviors

### Automatic Triggers

| Event | Tests | Build | Deploy | Security |
|-------|-------|-------|--------|----------|
| Push to `main` | ✅ | ✅ | ✅ | ✅ |
| Push to `develop` | ✅ | ❌ | ❌ | ✅ |
| Pull Request | ✅ | ❌ | ❌ | ✅ |
| Manual | ✅ | ✅ | ✅ | ✅ |

### Manual Workflow Dispatch

Run workflows manually:

1. Go to **Actions** tab
2. Select workflow (e.g., "Docker Build & Push")
3. Click **Run workflow**
4. Select branch and click **Run workflow**

## Using Docker Images

### Pull from GitHub Container Registry

```bash
# Login to GitHub Container Registry
echo $GITHUB_TOKEN | docker login ghcr.io -u USERNAME --password-stdin

# Pull image
docker pull ghcr.io/username/repository:latest

# Run container
docker run -p 5000:5000 ghcr.io/username/repository:latest
```

### Make Package Public

By default, packages are private. To make public:

1. Go to your package page: `https://github.com/users/USERNAME/packages/container/REPO`
2. Click **Package settings**
3. Scroll to **Danger Zone**
4. Click **Change visibility** → **Public**

## Monitoring and Debugging

### View Workflow Runs

1. Go to **Actions** tab
2. Click on a workflow run
3. Click on a job to see detailed logs

### Common Issues

#### SSH Connection Failed
```
Error: ssh: connect to host X.X.X.X port 22: Connection refused
```
**Solution:**
- Verify `SERVER_HOST` is correct
- Check server firewall allows SSH
- Verify SSH service is running: `sudo systemctl status sshd`

#### Permission Denied (publickey)
```
Error: Permission denied (publickey)
```
**Solution:**
- Verify `SSH_PRIVATE_KEY` secret is complete and correct
- Check public key is in server's `~/.ssh/authorized_keys`
- Verify key permissions: `chmod 600 ~/.ssh/authorized_keys`

#### Docker Command Not Found
```
Error: docker: command not found
```
**Solution:**
- Install Docker on deployment server
- Add deployment user to docker group: `sudo usermod -aG docker $USER`

#### Tests Failing
```
Error: ImportError: No module named 'flask'
```
**Solution:**
- Verify `requirements.txt` includes all dependencies
- Check Python version in workflow matches project requirements

## Branch Protection Rules

Protect your main branch:

1. Go to **Settings** → **Branches**
2. Click **Add rule**
3. Branch name pattern: `main`
4. Enable:
   - ✅ Require status checks to pass before merging
   - ✅ Require branches to be up to date
   - Select required status checks: `test`, `build`
   - ✅ Require pull request reviews
5. Click **Create** or **Save changes**

## Adding Status Badges

Add workflow status badges to README:

```markdown
[![Tests](https://github.com/USERNAME/REPO/workflows/Tests/badge.svg)](https://github.com/USERNAME/REPO/actions)
[![CI/CD](https://github.com/USERNAME/REPO/workflows/CI%2FCD%20Pipeline/badge.svg)](https://github.com/USERNAME/REPO/actions)
```

Replace `USERNAME` and `REPO` with your values.

## Alternative Deployment Methods

### Deploy to Cloud Platforms

#### AWS EC2
Use `aws-actions/configure-aws-credentials` action

#### Azure App Service
Use `azure/webapps-deploy` action

#### Google Cloud Run
Use `google-github-actions/deploy-cloudrun` action

#### Heroku
Use `akhileshns/heroku-deploy` action

### Deploy to Kubernetes

```yaml
- name: Deploy to Kubernetes
  uses: azure/k8s-deploy@v4
  with:
    manifests: |
      k8s/deployment.yml
      k8s/service.yml
    images: |
      ghcr.io/${{ github.repository }}:${{ github.sha }}
```

## Security Best Practices

1. **Never commit secrets** - Always use GitHub Secrets
2. **Rotate SSH keys regularly** - Update keys every 90 days
3. **Use SSH key passphrases** - Add extra security layer
4. **Limit secret access** - Only necessary workflows should access secrets
5. **Review workflow logs** - Check for exposed sensitive data
6. **Enable Dependabot** - Automatic dependency updates
7. **Use signed commits** - Verify commit authenticity

## Getting Help

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Docker Documentation](https://docs.docker.com/)
- [Community Forums](https://github.community/)
- Project Issues: Open an issue in this repository

## Next Steps

- [ ] Set up branch protection rules
- [ ] Configure code coverage reporting
- [ ] Add integration tests
- [ ] Set up staging environment
- [ ] Configure monitoring and alerting
- [ ] Enable automated backups
