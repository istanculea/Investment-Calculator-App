# Investment Calculator Web Application

![Python](https://img.shields.io/badge/Python-3.10+-blue)
![Flask](https://img.shields.io/badge/Flask-Web_Framework-lightgrey)
![Docker](https://img.shields.io/badge/Docker-Containerized-blue)
![Tests](https://img.shields.io/badge/Tests-pytest-success)
![License](https://img.shields.io/badge/License-MIT-green)
![Status](https://img.shields.io/badge/Status-Active_Development-orange)
![CI](https://img.shields.io/badge/CI-GitHub_Actions-black)
![Code Style](https://img.shields.io/badge/Code%20Style-PEP8-brightgreen)

---

## Overview

A Flask-based web application that acts as an interactive investment calculator.  
It projects portfolio growth from a lump sum plus recurring contributions while accounting for:

- Compounding frequency
- Contribution timing
- Contribution growth
- Inflation

The application provides year-by-year schedules and visual charts.

---

## DevOps Portfolio Project

This project demonstrates practical DevOps and cloud-native skills across the full application lifecycle.

### Architecture Overview

User → Flask Web App → Financial Engine  
                 ↓  
            Matplotlib Charts  
                 ↓  
            Docker Container

### Implemented DevOps Concepts

- Docker containerization  
- Dependency isolation  
- pytest automated testing  
- Infrastructure-ready builds  
- Local/container parity  
- Modular business logic  
- Observability-ready structure  

This project intentionally includes real business logic (financial math), visualization, testing, and container security — not just “Hello World”.

---

## Financial Model

The calculator uses standard **time-value-of-money** formulas.

### Lump Sum Growth

FV = PV(1+i)^n

---

### Ordinary Annuity (End-of-Period Contributions)

FV = R((1+i)^n - 1) / i

Combined:

FV = PV(1+i)^n + R((1+i)^n - 1) / i

---

### Annuity Due (Beginning-of-Period)

FV_due = FV_annuity × (1+i)

---

### Growing Contributions

FV = R/(i-g) × [(1+i)^n - (1+g)^n] × (1+iT)

Where:

- R = contribution  
- i = interest rate  
- g = contribution growth  
- n = periods  
- T = 0 ordinary / 1 due  

---

### Inflation Adjustment

FV_real = FV_nominal / (1+inflation)^n

---

### Numerical Stability

When analytical formulas become unstable (for example i ≈ g or long horizons), the app switches to deterministic period-by-period simulation.

This hybrid analytical + numerical approach mirrors production financial systems.

---

## Features

- Flexible compounding and contribution frequencies  
- Beginning or end-of-period payments  
- Growing contributions  
- Inflation-adjusted real returns  
- Year-by-year schedule  
- Matplotlib growth charts  
- Responsive Flask + Bootstrap UI  

---

## Getting Started

### Prerequisites

- Python 3.10+  
- pip  

---

### Installation

git clone https://github.com/your-username/investment-calculator-app.git  
cd investment-calculator  
python -m venv venv  
source venv/bin/activate  
pip install --upgrade pip  
pip install -r requirements.txt  

---

## Run Locally

python app.py  

Open:

http://localhost:5000

---

## Docker Deployment

docker build -t your-username/investment-calculator-app .  
docker run -p 5000:5000 your-username/investment-calculator-app  

Navigate to:

http://localhost:5000

---

## Testing

Uses pytest for unit and integration testing.

pip install pytest  
pytest  

---

## License

MIT License — see LICENSE file.

---