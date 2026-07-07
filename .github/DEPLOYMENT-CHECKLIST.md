# Deployment Checklist

Use this checklist before deploying your Employee Management System.

## 🔒 Pre-Deployment Security

- [ ] Change `SECRET_KEY` in production `.env`
- [ ] Use strong database passwords
- [ ] Never commit `.env` file to repository
- [ ] Review all exposed ports in `docker-compose.yml`
- [ ] Enable HTTPS/SSL certificates
- [ ] Configure firewall rules on server
- [ ] Disable debug mode (`DEBUG=False`)
- [ ] Review nginx security headers
- [ ] Set up database backups
- [ ] Configure log rotation

## 🔐 GitHub Actions Setup

- [ ] Repository is pushed to GitHub
- [ ] GitHub Actions is enabled
- [ ] Secrets configured in repository:
  - [ ] `SERVER_HOST`
  - [ ] `SERVER_USER`
  - [ ] `SSH_PRIVATE_KEY`
  - [ ] `SERVER_PORT` (optional)
- [ ] Update deployment path in `ci-cd.yml` (line 139)
- [ ] Test workflow runs successfully
- [ ] Docker images build without errors
- [ ] Status badges added to README

## 🖥️ Server Preparation

- [ ] Server has SSH access enabled
- [ ] Docker installed on server
- [ ] Docker Compose installed on server
- [ ] Deployment user has docker permissions
- [ ] Git installed on server
- [ ] Repository cloned to server
- [ ] `.env` file created on server
- [ ] Database initialized
- [ ] Nginx installed (if using)
- [ ] SSL certificates configured (if using HTTPS)
- [ ] Firewall configured (ports 22, 80, 443, 5000)
- [ ] Backup directory created

## 📦 Application Configuration

- [ ] Update `docker-compose.yml` for production
- [ ] Configure database connection string
- [ ] Set proper environment variables
- [ ] Configure static file serving
- [ ] Set up logging
- [ ] Configure error handling
- [ ] Test email functionality (if any)
- [ ] Configure external APIs (if any)

## 🧪 Testing

- [ ] All unit tests passing locally
- [ ] All unit tests passing in CI
- [ ] Manual testing on staging
- [ ] Database migrations tested
- [ ] API endpoints tested
- [ ] UI tested in multiple browsers
- [ ] Mobile responsiveness verified
- [ ] Error handling verified
- [ ] Performance testing completed
- [ ] Security scan passed

## 🚀 Deployment Steps

### Initial Deployment

1. **Prepare Server**
```bash
# SSH into server
ssh user@your-server

# Install Docker
curl -fsSL https://get.docker.com | sh

# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Add user to docker group
sudo usermod -aG docker $USER
```

2. **Clone Repository**
```bash
cd /opt
sudo git clone https://github.com/yourusername/yourrepo.git employee-management
sudo chown -R $USER:$USER employee-management
cd employee-management
```

3. **Configure Environment**
```bash
cp .env.example .env
nano .env  # Edit with production values
```

4. **Start Application**
```bash
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d
```

5. **Verify Deployment**
```bash
# Check containers
docker-compose ps

# Check logs
docker-compose logs -f --tail=50

# Test endpoint
curl http://localhost:5000
```

### Automated Deployment (via GitHub Actions)

1. **Push to Main Branch**
```bash
git add .
git commit -m "deploy: initial deployment"
git push origin main
```

2. **Monitor Deployment**
- Go to GitHub Actions tab
- Watch workflow execution
- Check deployment logs

3. **Verify on Server**
```bash
ssh user@server
cd /opt/employee-management
docker-compose ps
docker-compose logs --tail=50
```

## 🔄 Post-Deployment

- [ ] Application accessible at production URL
- [ ] SSL certificate working (HTTPS)
- [ ] Database connected and working
- [ ] Static files loading
- [ ] Forms submitting correctly
- [ ] API endpoints responding
- [ ] No console errors in browser
- [ ] Server logs clean
- [ ] Email notifications working (if any)
- [ ] Monitoring set up
- [ ] Backups configured and tested
- [ ] Documentation updated

## 📊 Monitoring Setup

- [ ] Set up uptime monitoring (UptimeRobot, Pingdom)
- [ ] Configure application logging
- [ ] Set up error tracking (Sentry, Rollbar)
- [ ] Monitor resource usage (CPU, Memory, Disk)
- [ ] Set up alerts for downtime
- [ ] Configure log aggregation
- [ ] Set up performance monitoring
- [ ] Database monitoring enabled

## 🔧 Maintenance

### Daily
- [ ] Check application status
- [ ] Review error logs
- [ ] Monitor resource usage

### Weekly
- [ ] Review access logs
- [ ] Check backup integrity
- [ ] Update dependencies (if needed)
- [ ] Security updates

### Monthly
- [ ] Full backup verification
- [ ] Security audit
- [ ] Performance review
- [ ] Documentation update

## 🆘 Rollback Plan

If deployment fails:

```bash
# SSH into server
ssh user@server
cd /opt/employee-management

# Rollback to previous version
git reset --hard HEAD~1

# Restart containers
docker-compose down
docker-compose up -d

# Verify
docker-compose ps
docker-compose logs
```

## 📝 Emergency Contacts

| Role | Name | Contact |
|------|------|---------|
| System Admin | | |
| Database Admin | | |
| On-call Developer | | |
| Hosting Provider Support | | |

## 📞 Support Resources

- Server Documentation: 
- API Documentation: 
- Database Schema: 
- Runbook: 
- Incident Response Plan: 

## ✅ Sign-off

- [ ] Development Team Lead: _________________ Date: _____
- [ ] QA Team Lead: _________________ Date: _____
- [ ] DevOps Engineer: _________________ Date: _____
- [ ] Security Officer: _________________ Date: _____
- [ ] Project Manager: _________________ Date: _____

---

**Deployment Date:** _______________  
**Deployed By:** _______________  
**Version:** _______________  
**Notes:** _______________________________________________
