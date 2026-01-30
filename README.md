# Investment Calculator — DevOps Portfolio Project
![Python](https://img.shields.io/badge/Python-3.10+-blue)![Flask](https://img.shields.io/badge/Flask-Web_Framework-lightgrey)![Docker](https://img.shields.io/badge/Docker-Containerized-blue)
![CI](https://img.shields.io/badge/CI-GitHub_Actions-success)![Registry](https://img.shields.io/badge/Image-Docker_Hub-blue)![Tests](https://img.shields.io/badge/Tests-pytest-success)

---

## Project Objective

This repository contains a production-style Flask application used as a **DevOps portfolio project**.

The goal is to demonstrate real-world engineering practices across:

* Application development
* CI/CD automation
* Container publishing
* Cloud-native readiness

The financial calculator exists to provide non-trivial business logic rather than a toy example.

---

## Current Architecture

```
Browser
   |
   v
Flask Web App
   |
   v
Investment Engine + Schedule Simulation
   |
   v
Matplotlib Chart Renderer
   |
Docker Container
   |
Docker Hub Registry
```

Images are automatically built and published via GitHub Actions.

---

## Implemented DevOps Capabilities

### CI/CD

* **GitHub Actions pipeline:**
  * Automated testing on Python 3.10, 3.11, and 3.12
  * Code quality checks with flake8
  * Test coverage reporting with codecov
  * Docker image building and pushing to Docker Hub
  * Security scanning with Trivy
  * Runs on push to main/develop branches and PRs

### Quality Gates

* Unit tests for calculation engine
* Flask route integration tests  
* Input validation tests
* Error handling tests
* Pipeline blocks on test failure
* Security vulnerability scanning

---

### Containerization

* Multi-stage Docker build
* Dependency isolation
* Stateless container
* Port 5000 exposed for orchestration platforms
* **Non-root user for security**
* **Health checks for monitoring**
* **Optimized layer caching**

---

### Security

* **Security headers** (CSP, X-Frame-Options, etc.)
* **Input validation and sanitization**
* **Non-root Docker user**
* **Pinned dependency versions**
* **Environment-based configuration**
* **Automated vulnerability scanning**

---

### Engineering Practices

* Separation of UI, logic, and plotting
* Deterministic financial simulation
* Production-ready Flask layout
* Infrastructure-friendly container design
* **Comprehensive error handling and logging**
* **Input validation**
* **Type hints and documentation**
* **Health check endpoints**

---

## Application Features

* Lump sum + recurring investments
* Flexible compounding vs contribution frequency
* Beginning or end-of-period payments
* Growing contributions
* Inflation adjustment
* Year-by-year schedule
* Portfolio growth chart

---

## Technology Stack

* **Python 3.10+** (tested on 3.10, 3.11, 3.12)
* **Flask** - Web framework
* **Matplotlib** - Chart generation
* **pytest** - Testing framework
* **Docker** - Containerization
* **GitHub Actions** - CI/CD
* **Docker Hub** - Container registry
* **Trivy** - Security scanning
* **flake8** - Code linting
* **black** - Code formatting

---

## Local Development

### Prerequisites
- Python 3.10 or higher
- pip

### Setup

```bash
git clone https://github.com/istanculea/Investment-Calculator-App.git
cd Investment-Calculator-App/investment_calculator_app

python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

pip install -r requirements.txt
pip install -r requirements-dev.txt  # For development dependencies
```

### Environment Configuration

Copy the example environment file and configure as needed:

```bash
cp .env.example .env
# Edit .env with your configuration
```

---

## Run Locally

### Using Python directly

```bash
cd investment_calculator_app
python app.py
```

Visit http://localhost:5000 in your browser.

### Using Docker Compose (Recommended)

```bash
docker-compose up
```

### Using Docker

```bash
cd investment_calculator_app
docker build -t investment-calculator .
docker run -p 5000:5000 investment-calculator
```

---

## Run from Docker Hub

```bash
docker pull your-dockerhub-username/investment-calculator
docker run -p 5000:5000 your-dockerhub-username/investment-calculator
```

---

## Testing

Run the test suite:

```bash
cd investment_calculator_app
pytest tests/ -v
```

Run with coverage:

```bash
pytest tests/ --cov=. --cov-report=html
```

Run linting:

```bash
flake8 .
```

---

## Roadmap (In Progress)

### Kubernetes Deployment (Helm)

* Helm chart for application deployment
* Configurable values.yaml
* Service + Ingress
* Horizontal Pod Autoscaler

---

### Observability

* Prometheus scraping
* Grafana dashboards:

  * Request latency
  * Error rate
  * Pod CPU / memory
  * Application throughput

---

### Future Enhancements

* ArgoCD GitOps deployment
* Trivy image scanning
* SLO-based alerting

---


## This project demonstrates:

✅ Real application logic  
✅ CI/CD automation with comprehensive pipeline  
✅ Container publishing with security best practices  
✅ Cloud-native design with health checks  
✅ Kubernetes readiness  
✅ **Security-first approach**  
✅ **Production-ready error handling**  
✅ **Comprehensive testing (7 tests)**  
✅ **Code quality standards**

---

## Contributing

Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on how to contribute to this project.

---

## License

MIT
