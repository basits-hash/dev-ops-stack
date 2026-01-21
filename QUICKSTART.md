# Quick Start Guide

Welcome to the DevOps Task Manager! This guide will help you get started quickly.

## 🚀 Fastest Way to Run

### Using Docker Compose (Recommended)

```bash
# 1. Make sure Docker is running
docker --version

# 2. Clone and navigate to the project
cd dev-ops-basit-

# 3. Start everything
docker-compose up -d

# 4. Open your browser
# Frontend: http://localhost:3000
# Backend: http://localhost:5000/health
```

That's it! The application is now running.

## 📱 What You'll See

1. **Task Manager Interface** - A beautiful, responsive web app at http://localhost:3000
2. **Add tasks** - Click "Add Task" to create new tasks
3. **Mark complete** - Check the checkbox to mark tasks as done
4. **Filter tasks** - Use All/Active/Completed filters
5. **Statistics** - See your task counts in real-time

## 🛠️ Development Mode

Want to make changes and see them live?

### Backend Development
```bash
cd backend
npm install
npm run dev
```

### Frontend Development
```bash
cd frontend
npm install
npm start
```

## 📊 Monitoring

Access the monitoring dashboards:

- **Prometheus**: http://localhost:9090
- **Grafana**: http://localhost:3001 (admin/admin)

## 🧪 Testing

Run all tests:
```bash
chmod +x scripts/test.sh
./scripts/test.sh
```

## 🛑 Stop Everything

```bash
docker-compose down
```

## 📚 Next Steps

- Read the [Architecture Documentation](docs/architecture.md)
- Check out the [Deployment Guide](docs/deployment.md)
- Explore the Kubernetes manifests in `/k8s`
- Review the CI/CD pipelines in `.github/workflows`

## 🆘 Troubleshooting

### Port Already in Use
```bash
# Stop existing containers
docker-compose down

# Or use different ports by editing docker-compose.yml
```

### Backend Connection Error
```bash
# Check if MongoDB is running
docker-compose ps

# View logs
docker-compose logs backend
docker-compose logs mongodb
```

### Frontend Can't Connect to Backend
```bash
# Ensure backend is running
curl http://localhost:5000/health

# Should return: {"status":"healthy",...}
```

## 💡 Tips

1. **First Time Setup**: Run `./scripts/setup.sh` to install all dependencies
2. **Fresh Start**: Run `./scripts/cleanup.sh` to remove all containers and volumes
3. **Check Health**: Visit http://localhost:5000/health to verify backend status
4. **View Metrics**: Visit http://localhost:5000/metrics for Prometheus metrics

## 🎯 Project Goals

This project demonstrates:
- ✅ Full-stack development (React + Node.js + MongoDB)
- ✅ Containerization with Docker
- ✅ Container orchestration with Kubernetes
- ✅ CI/CD with GitHub Actions
- ✅ Infrastructure as Code with Terraform
- ✅ Monitoring with Prometheus & Grafana
- ✅ Production-ready practices

Perfect for IT majors and DevOps portfolios!

---

**Need Help?** Check the full README.md or create an issue on GitHub.
