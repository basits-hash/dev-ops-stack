# DevOps Task Manager — Python + Azure DevOps

A production-ready Task Management application demonstrating modern DevOps practices on **Azure**, with a **Python FastAPI** backend, Azure DevOps CI/CD pipelines, AKS orchestration, and full observability.

![Python](https://img.shields.io/badge/Python-3.12-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.111-green)
![Azure DevOps](https://img.shields.io/badge/Azure%20DevOps-Pipeline-0078D4)
![Docker](https://img.shields.io/badge/Docker-Ready-blue)
![AKS](https://img.shields.io/badge/AKS-Kubernetes-326CE5)
![Terraform](https://img.shields.io/badge/Terraform-Azure-7B42BC)

## Project Overview

| Layer | Technology |
|---|---|
| Frontend | React.js (nginx) |
| Backend API | Python 3.12 + FastAPI + Motor (async MongoDB) |
| Database | MongoDB 7 |
| Containerization | Docker / Docker Compose |
| Orchestration | Azure Kubernetes Service (AKS) |
| CI/CD | **Azure DevOps Pipelines** |
| Infrastructure as Code | Terraform (Azure provider) |
| Container Registry | Azure Container Registry (ACR) |
| Monitoring | Prometheus + Grafana |
| Logging | Azure Monitor / Log Analytics |

## Architecture

```
┌─────────────────┐     ┌──────────────────┐     ┌─────────────┐
│  React Frontend │────▶│  FastAPI Backend  │────▶│   MongoDB   │
│   (nginx:80)    │     │  (uvicorn:8000)   │     │             │
└─────────────────┘     └──────────────────┘     └─────────────┘
         │                        │
         └──────── AKS Cluster ───┘
                        │
          ┌─────────────┴─────────────┐
          │                           │
   Azure DevOps               Azure Container
     Pipelines                  Registry (ACR)
          │
   ┌──────┴──────┐
   │  Terraform  │
   │  (Azure)    │
   └─────────────┘
```

## CI/CD Pipeline (Azure DevOps)

`azure-pipelines.yml` defines 4 stages:

| Stage | Trigger | What happens |
|---|---|---|
| **Test** | every push / PR | pytest + flake8 for Python backend; Jest + build for frontend |
| **Security Scan** | after Test | `safety` dependency audit + Trivy filesystem scan |
| **Build** | `main` branch only | Builds & pushes Docker images to ACR (tagged with `BuildId` + `latest`) |
| **Deploy Dev** | after Build | Deploys to AKS `task-manager` namespace via `KubernetesManifest` task |
| **Deploy Prod** | after Dev | Deploys to AKS `task-manager-prod` namespace — **requires manual approval gate** |

### Azure DevOps Setup

1. Create a new Azure DevOps project and import this repo.
2. Create a **Service Connection** named `AzureServiceConnection` (Azure Resource Manager, subscription scope).
3. Create a **Service Connection** named `AzureContainerRegistry` (Docker Registry → ACR).
4. Add an **approval gate** on the `production` environment in Azure DevOps Environments.
5. Create the pipeline from `azure-pipelines.yml`.

## Quick Start (Docker Compose)

```bash
docker-compose up -d
```

| Service | URL |
|---|---|
| Frontend | http://localhost:3000 |
| Backend API | http://localhost:8000 |
| API Docs (Swagger) | http://localhost:8000/docs |
| Metrics | http://localhost:8000/metrics |
| Health | http://localhost:8000/health |
| Prometheus | http://localhost:9090 |
| Grafana | http://localhost:3001 (admin/admin) |

## Local Backend Development

```bash
cd backend
pip install -r requirements-dev.txt

# Run tests
pytest -v

# Start dev server (auto-reload)
uvicorn main:app --reload --port 8000
```

## API Endpoints

| Method | Path | Description |
|---|---|---|
| GET | `/health` | Health check + MongoDB status |
| GET | `/metrics` | Prometheus metrics |
| GET | `/api/tasks` | List all tasks |
| POST | `/api/tasks` | Create task `{"title": "..."}` |
| PUT | `/api/tasks/{id}` | Update task `{"completed": true}` |
| DELETE | `/api/tasks/{id}` | Delete task |

Interactive docs at `GET /docs` (Swagger UI) and `GET /redoc`.

## Kubernetes (AKS)

```bash
# Apply all manifests
kubectl apply -f k8s/

# Check status
kubectl get pods -n task-manager
kubectl get svc -n task-manager
```

## Infrastructure (Terraform → Azure)

```bash
cd terraform
terraform init        # pulls azurerm provider, configures Azure Blob backend
terraform plan
terraform apply       # provisions RG, ACR, VNet, AKS, Log Analytics
```

### Resources created

- Resource Group
- Azure Container Registry (Standard SKU)
- Virtual Network + AKS subnet
- AKS cluster (SystemAssigned identity, Azure CNI)
- ACR pull role assignment for AKS kubelet
- Log Analytics Workspace

## Project Structure

```
dev-ops-basit-/
├── azure-pipelines.yml       # Azure DevOps CI/CD pipeline
├── docker-compose.yml        # Local dev stack
├── backend/                  # Python FastAPI service
│   ├── main.py               # App: routes, models, metrics
│   ├── requirements.txt      # Production deps
│   ├── requirements-dev.txt  # Test deps
│   ├── pytest.ini
│   ├── Dockerfile
│   └── tests/
│       └── test_main.py
├── frontend/                 # React + nginx
├── k8s/                      # Kubernetes manifests (AKS)
│   ├── namespace.yaml
│   ├── backend-deployment.yaml
│   ├── frontend-deployment.yaml
│   ├── mongodb-deployment.yaml
│   ├── ingress.yaml
│   ├── hpa.yaml
│   └── secrets.yaml
├── terraform/                # Azure IaC
│   ├── main.tf               # ACR, AKS, VNet, Log Analytics
│   ├── variables.tf
│   └── outputs.tf
└── monitoring/               # Prometheus + Grafana config
```

## Security

- Non-root user in Docker images
- ACR pull access via managed identity (no passwords)
- Kubernetes Secrets for MongoDB credentials
- Trivy + `safety` scans on every pipeline run
- FastAPI input validation via Pydantic

## Author

**Basit Sherazi** — [@BasitS-hash](https://github.com/BasitS-hash)

---

*Built to demonstrate Azure DevOps + Python DevOps practices.*
