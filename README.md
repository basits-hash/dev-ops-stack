# DevOps Task Manager - Full Stack Application

A production-ready Task Management application demonstrating modern DevOps practices, CI/CD pipelines, containerization, orchestration, and monitoring.

**🌐 Live Demo**: [https://basitsherazi.github.io/dev-ops-basit-/](https://basitsherazi.github.io/dev-ops-basit-/)

![DevOps](https://img.shields.io/badge/DevOps-Enabled-blue)
![Docker](https://img.shields.io/badge/Docker-Ready-blue)
![Kubernetes](https://img.shields.io/badge/Kubernetes-Ready-blue)
![CI/CD](https://img.shields.io/badge/CI%2FCD-GitHub%20Actions-green)
![Live](https://img.shields.io/badge/Live-GitHub%20Pages-success)

## 🚀 Project Overview

This project showcases a complete DevOps workflow for a full-stack application:

- **Frontend**: React.js with responsive design
- **Backend**: Node.js/Express REST API
- **Database**: MongoDB (containerized)
- **Containerization**: Docker & Docker Compose
- **Orchestration**: Kubernetes manifests
- **CI/CD**: GitHub Actions pipelines
- **Infrastructure as Code**: Terraform
- **Monitoring**: Prometheus & Grafana
- **Logging**: ELK Stack configuration

## 📋 Table of Contents

- [Features](#features)
- [Architecture](#architecture)
- [Getting Started](#getting-started)
- [Deployment Options](#deployment-options)
- [CI/CD Pipeline](#cicd-pipeline)
- [Monitoring](#monitoring)
- [Project Structure](#project-structure)

## ✨ Features

### Application Features
- ✅ Create, read, update, and delete tasks
- ✅ Mark tasks as complete/incomplete
- ✅ Filter tasks by status
- ✅ Responsive UI design
- ✅ RESTful API architecture

### DevOps Features
- 🐳 Full Docker containerization
- ☸️ Kubernetes deployment manifests
- 🔄 Automated CI/CD with GitHub Actions
- 📊 Prometheus metrics and Grafana dashboards
- 📝 Centralized logging with ELK Stack
- 🏗️ Infrastructure as Code with Terraform
- 🧪 Automated testing (unit & integration)
- 🔒 Security scanning and best practices

## 🏗️ Architecture

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   React     │────▶│   Express   │────▶│   MongoDB   │
│  Frontend   │     │   Backend   │     │  Database   │
└─────────────┘     └─────────────┘     └─────────────┘
       │                    │                    │
       └────────────────────┴────────────────────┘
                           │
                    Docker Containers
                           │
                    Kubernetes Cluster
                           │
              ┌────────────┴────────────┐
              │                         │
         Prometheus              GitHub Actions
         Grafana                   CI/CD
```

## 🚀 Getting Started

### 🌐 Try it Live!

**No installation needed!** Visit the live demo:
👉 **[https://basitsherazi.github.io/dev-ops-basit-/](https://basitsherazi.github.io/dev-ops-basit-/)**

The live demo runs in **Demo Mode** with data saved in your browser - fully functional without a backend!

### 📋 Quick Deploy to GitHub Pages

Want your own live version? Just 3 steps:

```bash
# 1. Push to GitHub
git add .
git commit -m "Deploy to GitHub Pages"
git push origin main

# 2. Enable GitHub Pages in repository Settings → Pages
# 3. Wait 2-3 minutes - your site is live!
```

See [GITHUB_PAGES_DEPLOY.md](GITHUB_PAGES_DEPLOY.md) for detailed instructions.

### Prerequisites

- Docker & Docker Compose
- Node.js (v18+)
- npm or yarn
- kubectl (for Kubernetes)
- Terraform (optional, for IaC)

### Quick Start with Docker Compose

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd dev-ops-basit-
   ```

2. **Start all services**
   ```bash
   docker-compose up -d
   ```

3. **Access the application**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:5000
   - MongoDB: localhost:27017

4. **Stop services**
   ```bash
   docker-compose down
   ```

### Local Development Setup

#### Backend Setup
```bash
cd backend
npm install
npm run dev
```

#### Frontend Setup
```bash
cd frontend
npm install
npm start
```

## 🚢 Deployment Options

### 1. Docker Compose (Development)
```bash
docker-compose up -d
```

### 2. Kubernetes (Production)
```bash
# Apply all manifests
kubectl apply -f k8s/

# Check deployment status
kubectl get pods
kubectl get services
```

### 3. Cloud Deployment with Terraform
```bash
cd terraform
terraform init
terraform plan
terraform apply
```

## 🔄 CI/CD Pipeline

The project includes GitHub Actions workflows for:

1. **Build & Test** (`.github/workflows/ci.yml`)
   - Runs on every push and PR
   - Executes unit and integration tests
   - Builds Docker images
   - Performs security scans

2. **Deploy** (`.github/workflows/deploy.yml`)
   - Triggers on main branch merge
   - Builds and pushes Docker images
   - Deploys to Kubernetes
   - Runs smoke tests

3. **Infrastructure** (`.github/workflows/terraform.yml`)
   - Validates Terraform configurations
   - Plans infrastructure changes
   - Applies changes on approval

## 📊 Monitoring

### Prometheus Metrics
- Application health checks
- Request rate and latency
- Error rates
- Custom business metrics

Access Prometheus: `http://localhost:9090`

### Grafana Dashboards
- Pre-configured dashboards for application monitoring
- System resource monitoring
- Custom alerts

Access Grafana: `http://localhost:3001`
- Username: `admin`
- Password: `admin`

## 📁 Project Structure

```
dev-ops-basit-/
├── frontend/                 # React application
│   ├── src/
│   ├── public/
│   ├── Dockerfile
│   └── package.json
├── backend/                  # Express API
│   ├── src/
│   ├── tests/
│   ├── Dockerfile
│   └── package.json
├── k8s/                      # Kubernetes manifests
│   ├── frontend-deployment.yaml
│   ├── backend-deployment.yaml
│   ├── mongodb-deployment.yaml
│   └── ingress.yaml
├── terraform/                # Infrastructure as Code
│   ├── main.tf
│   ├── variables.tf
│   └── outputs.tf
├── monitoring/               # Monitoring configuration
│   ├── prometheus/
│   └── grafana/
├── .github/
│   └── workflows/           # CI/CD pipelines
├── docker-compose.yml
└── README.md
```

## 🧪 Testing

### Run Backend Tests
```bash
cd backend
npm test
npm run test:integration
```

### Run Frontend Tests
```bash
cd frontend
npm test
```

### Run E2E Tests
```bash
npm run test:e2e
```

## 🔒 Security

- Docker image scanning with Trivy
- Dependency vulnerability scanning
- Secret management with Kubernetes secrets
- HTTPS/TLS configuration
- Security headers implementation

## 📚 Documentation

- [Architecture Design](docs/architecture.md)
- [API Documentation](docs/api.md)
- [Deployment Guide](docs/deployment.md)
- [Monitoring Guide](docs/monitoring.md)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Author

**Basit Sherazi**
- GitHub: [@basitsherazi](https://github.com/basitsherazi)

## 🙏 Acknowledgments

This project demonstrates production-ready DevOps practices suitable for enterprise applications.

---

**Made with ❤️ for IT Majors and DevOps Enthusiasts**
