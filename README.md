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

* GitHub Actions pipeline:

  * Runs pytest
  * Builds Docker image
  * Pushes image to Docker Hub

---

### Containerization

* Multi-stage Docker build
* Dependency isolation
* Stateless container
* Port 5000 exposed for orchestration platforms

---

### Quality Gates

* Unit tests for calculation engine
* Flask route integration tests
* Pipeline blocks on test failure

---

### Engineering Practices

* Separation of UI, logic, and plotting
* Deterministic financial simulation
* Production-ready Flask layout
* Infrastructure-friendly container design

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

* Python 3.10
* Flask
* Matplotlib
* pytest
* Docker
* GitHub Actions
* Docker Hub

---

## Local Development

```bash
git clone https://github.com/your-username/investment-calculator-app.git
cd investment-calculator-app

python -m venv venv
source venv/bin/activate

pip install -r requirements.txt
```

---

## Run Locally

```bash
python app.py
```

---

## Run from Docker Hub

```bash
docker pull your-dockerhub-username/investment-calculator
docker run -p 5000:5000 your-dockerhub-username/investment-calculator
```

---

## Testing

```bash
pytest
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
✅ CI/CD automation
✅ Container publishing
✅ Cloud-native design
✅ Kubernetes readiness

---

## License

MIT
