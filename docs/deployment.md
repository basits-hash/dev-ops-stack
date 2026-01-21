# Deployment Guide

## Prerequisites

Before deploying the Task Manager application, ensure you have:

- Docker and Docker Compose installed
- kubectl (for Kubernetes deployment)
- Access to a Kubernetes cluster (optional)
- AWS account (for cloud deployment)
- Terraform (for infrastructure provisioning)

## Local Development Deployment

### Option 1: Docker Compose (Recommended)

This is the easiest way to run the application locally.

```bash
# Clone the repository
git clone <repository-url>
cd dev-ops-basit-

# Run the deployment script
chmod +x scripts/deploy.sh
./scripts/deploy.sh
```

Or manually:

```bash
# Build and start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

**Access the application:**
- Frontend: http://localhost:3000
- Backend API: http://localhost:5000
- Prometheus: http://localhost:9090
- Grafana: http://localhost:3001

### Option 2: Local Development

Run frontend and backend separately for development.

**Terminal 1 - Backend:**
```bash
cd backend
npm install
npm run dev
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm install
npm start
```

**Terminal 3 - MongoDB:**
```bash
docker run -d -p 27017:27017 \
  -e MONGO_INITDB_ROOT_USERNAME=admin \
  -e MONGO_INITDB_ROOT_PASSWORD=password123 \
  mongo:7.0
```

## Kubernetes Deployment

### Prerequisites

```bash
# Verify kubectl is configured
kubectl cluster-info

# Create namespace
kubectl create namespace task-manager
```

### Deploy to Kubernetes

```bash
# Apply all manifests
kubectl apply -f k8s/

# Check deployment status
kubectl get pods -n task-manager
kubectl get services -n task-manager

# View logs
kubectl logs -f deployment/backend-deployment -n task-manager
kubectl logs -f deployment/frontend-deployment -n task-manager
```

### Access the Application

```bash
# Get the LoadBalancer IP/hostname
kubectl get service frontend-service -n task-manager

# For local clusters (minikube/kind)
kubectl port-forward -n task-manager service/frontend-service 3000:80
```

### Update Deployment

```bash
# Update image
kubectl set image deployment/backend-deployment \
  backend=your-registry/task-manager-backend:new-tag \
  -n task-manager

# Check rollout status
kubectl rollout status deployment/backend-deployment -n task-manager

# Rollback if needed
kubectl rollout undo deployment/backend-deployment -n task-manager
```

### Scaling

```bash
# Manual scaling
kubectl scale deployment backend-deployment --replicas=5 -n task-manager

# Auto-scaling is configured via HPA
kubectl get hpa -n task-manager
```

## AWS Deployment with Terraform

### Prerequisites

```bash
# Configure AWS credentials
aws configure

# Initialize Terraform
cd terraform
terraform init
```

### Deploy Infrastructure

```bash
# Plan changes
terraform plan

# Apply changes
terraform apply

# Get outputs
terraform output
```

### Deploy Application to ECS

After infrastructure is provisioned:

```bash
# Build and push Docker images
docker build -t your-registry/task-manager-backend:latest ./backend
docker build -t your-registry/task-manager-frontend:latest ./frontend

docker push your-registry/task-manager-backend:latest
docker push your-registry/task-manager-frontend:latest

# Update ECS service (handled by CI/CD)
```

## CI/CD Deployment

### GitHub Actions Setup

1. **Configure Secrets:**

Go to GitHub repository → Settings → Secrets and add:

```
DOCKER_USERNAME=your-dockerhub-username
DOCKER_PASSWORD=your-dockerhub-password
KUBECONFIG=<base64-encoded-kubeconfig>
AWS_ACCESS_KEY_ID=your-aws-key
AWS_SECRET_ACCESS_KEY=your-aws-secret
```

2. **Trigger Deployment:**

```bash
# Push to main branch
git push origin main

# Or manually trigger
# GitHub → Actions → Deploy → Run workflow
```

3. **Monitor Deployment:**

- Check GitHub Actions tab for pipeline status
- View logs for each step
- Receive notifications on completion

## Production Deployment Checklist

### Before Deployment

- [ ] Update environment variables
- [ ] Configure secrets properly
- [ ] Set up monitoring and alerting
- [ ] Configure backup strategy
- [ ] Test in staging environment
- [ ] Review security settings
- [ ] Set up SSL certificates
- [ ] Configure DNS records

### Security Configuration

```bash
# Create secrets in Kubernetes
kubectl create secret generic app-secrets \
  --from-literal=mongodb-username=admin \
  --from-literal=mongodb-password=<secure-password> \
  -n task-manager

# Update secrets.yaml with proper values
# DO NOT commit actual secrets to git
```

### SSL/TLS Configuration

```bash
# Install cert-manager for automatic SSL
kubectl apply -f https://github.com/cert-manager/cert-manager/releases/download/v1.13.0/cert-manager.yaml

# Create ClusterIssuer for Let's Encrypt
kubectl apply -f k8s/cert-issuer.yaml

# Update ingress.yaml with your domain
```

### Database Configuration

```bash
# For production, use managed database service
# Update connection string in backend deployment

# Enable authentication
# Configure backup strategy
# Set up monitoring
```

## Monitoring Setup

### Prometheus and Grafana

```bash
# Access Grafana
kubectl port-forward -n task-manager service/grafana 3001:3000

# Login with admin/admin
# Add Prometheus datasource: http://prometheus:9090
# Import dashboards from monitoring/grafana/dashboards/
```

### CloudWatch (AWS)

```bash
# Logs are automatically sent to CloudWatch
# View in AWS Console → CloudWatch → Log Groups

# Create alarms
aws cloudwatch put-metric-alarm \
  --alarm-name high-cpu \
  --alarm-description "Alert when CPU exceeds 80%" \
  --metric-name CPUUtilization \
  --namespace AWS/ECS \
  --statistic Average \
  --period 300 \
  --threshold 80 \
  --comparison-operator GreaterThanThreshold
```

## Troubleshooting

### Common Issues

**Pods not starting:**
```bash
kubectl describe pod <pod-name> -n task-manager
kubectl logs <pod-name> -n task-manager
```

**Service not accessible:**
```bash
kubectl get endpoints -n task-manager
kubectl get ingress -n task-manager
```

**Database connection issues:**
```bash
# Check MongoDB pod
kubectl exec -it mongodb-deployment-xxx -n task-manager -- mongosh

# Test connection from backend pod
kubectl exec -it backend-deployment-xxx -n task-manager -- sh
# Inside pod:
curl mongodb-service:27017
```

**Image pull errors:**
```bash
# Check image name and tag
# Verify registry credentials
kubectl get events -n task-manager
```

### Health Checks

```bash
# Backend health
curl http://localhost:5000/health

# Kubernetes health
kubectl get --raw /healthz

# Database health
docker exec mongodb mongosh --eval "db.adminCommand('ping')"
```

## Rollback Procedures

### Kubernetes Rollback
```bash
# View revision history
kubectl rollout history deployment/backend-deployment -n task-manager

# Rollback to previous version
kubectl rollout undo deployment/backend-deployment -n task-manager

# Rollback to specific revision
kubectl rollout undo deployment/backend-deployment --to-revision=2 -n task-manager
```

### Docker Compose Rollback
```bash
# Stop current version
docker-compose down

# Checkout previous version
git checkout <previous-commit>

# Rebuild and start
docker-compose up -d --build
```

## Performance Tuning

### Resource Limits

Update resource limits in deployment manifests:

```yaml
resources:
  requests:
    memory: "256Mi"
    cpu: "250m"
  limits:
    memory: "512Mi"
    cpu: "500m"
```

### Database Optimization

```javascript
// Add indexes
db.tasks.createIndex({ createdAt: -1 })
db.tasks.createIndex({ completed: 1 })
```

## Maintenance

### Regular Updates

```bash
# Update dependencies
npm audit fix

# Update Docker images
docker-compose pull
docker-compose up -d

# Update Kubernetes components
kubectl apply -f k8s/
```

### Backup

```bash
# MongoDB backup
docker exec mongodb mongodump --out /backup

# Kubernetes resources backup
kubectl get all -n task-manager -o yaml > backup.yaml
```

## Support

For issues and questions:
- Check logs: `docker-compose logs` or `kubectl logs`
- Review documentation in `/docs`
- Create GitHub issue
- Contact: basit@example.com
