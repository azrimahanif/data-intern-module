# Week 4: Docker & CI/CD - Deploy to Render

## 🎯 Week Goals

Transform your Week 3 FastAPI application into a production-ready, containerized application deployed on Render. Learn Docker containerization, CI/CD pipelines, and cloud deployment best practices.

### 📚 Learning Objectives

- **Docker Containerization**
  - Create production-ready Docker images
  - Multi-stage builds for optimization
  - Docker Compose for local development
  - Environment-based configuration

- **CI/CD Pipeline Development**
  - GitHub Actions for automated testing
  - Docker image building and pushing
  - Automated deployment to Render
  - Security scanning and code quality

- **Cloud Deployment**
  - Deploy to Render (free tier)
  - PostgreSQL database setup
  - Environment variable management
  - Production monitoring and logging

## 🏗️ Project: "Deploy Employee Management API to Render"

### **What You'll Build:**
1. **Containerize** your Week 3 FastAPI application
2. **Set up CI/CD** pipeline with GitHub Actions
3. **Deploy to Render** with PostgreSQL database
4. **Monitor** production application performance

### **Why Render?**
- ✅ **100% FREE** (750 hours/month)
- ✅ **No credit card required**
- ✅ **PostgreSQL included**
- ✅ **Automatic HTTPS**
- ✅ **Easy GitHub integration**

---

## 📋 **4 Implementation Phases**

### **Phase 1: Fix Week 3 & Prepare for Docker (25 points)**
- [ ] Fix missing dependencies and configuration
- [ ] Create production-ready requirements.txt
- [ ] Add environment-based configuration
- [ ] Test local application thoroughly

### **Phase 2: Docker Containerization (30 points)**
- [ ] Create multi-stage Dockerfile
- [ ] Set up Docker Compose for local development
- [ ] Optimize image size and security
- [ ] Test containerized application locally

### **Phase 3: CI/CD Pipeline (25 points)**
- [ ] Set up GitHub Actions workflow
- [ ] Automated testing and building
- [ ] Docker image optimization
- [ ] Security scanning with Trivy

### **Phase 4: Render Deployment (20 points)**
- [ ] Deploy to Render platform
- [ ] Set up PostgreSQL database
- [ ] Configure production environment
- [ ] Test production deployment

---

## 🚀 **Getting Started**

### **Prerequisites**
- ✅ Week 3 FastAPI application completed
- ✅ Docker Desktop installed
- ✅ GitHub account with repository
- ✅ Render account (free signup)

### **Required Tools Installation**
```bash
# Install Docker Desktop
# Download from: https://www.docker.com/products/docker-desktop/

# Verify installation
docker --version
docker-compose --version

# Install additional tools (optional)
# SQLite Browser: https://sqlitebrowser.org/
```

---

## 📁 **Required Project Structure**

```
week4_docker_ci/
├── README.md                           # This file
├── starter/                            # Provided starter files
│   ├── requirements.txt               # Production dependencies
│   ├── .env.example                   # Environment template
│   ├── Dockerfile                     # Multi-stage container
│   ├── docker-compose.yml             # Local development
│   └── .github/workflows/             # CI/CD pipelines
└── submission/
    ├── main.py                        # Your Week 3 FastAPI app
    ├── models/                        # Data models
    ├── routers/                       # API endpoints
    ├── services/                      # Business logic
    ├── database/                      # Database config
    ├── Dockerfile                     # Your container config
    ├── docker-compose.yml             # Local development
    ├── .github/workflows/             # CI/CD pipelines
    ├── requirements.txt               # Dependencies
    ├── .env                          # Environment variables
    ├── render.yaml                    # Render deployment config
    └── README.md                     # Deployment documentation
```

---

## 📝 **Submission Requirements**

### **Due Date: Friday, 5:00 PM**

### **What You Must Submit:**
1. ✅ **Working containerized application**
2. ✅ **GitHub Actions CI/CD pipeline**
3. ✅ **Live deployment URL on Render**
4. ✅ **PostgreSQL database working**
5. ✅ **All Week 3 functionality preserved**
6. ✅ **Comprehensive documentation**

### **Bonus Points (10 extra):**
- ✅ **Custom domain setup**
- ✅ **Advanced monitoring**
- ✅ **Database backup strategy**
- ✅ **Performance optimization**

---

## 🔗 **Useful Resources**

- [Render Documentation](https://render.com/docs)
- [Docker Best Practices](https://docs.docker.com/develop/dev-best-practices/)
- [GitHub Actions Guide](https://docs.github.com/en/actions)
- [FastAPI Deployment](https://fastapi.tiangolo.com/deployment/)

---

**Focus**: Transform your local FastAPI app into a production-ready, cloud-deployed application with professional DevOps practices!
