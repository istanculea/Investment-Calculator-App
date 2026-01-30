# Contributing to Investment Calculator App

Thank you for your interest in contributing to the Investment Calculator App!

## Development Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/istanculea/Investment-Calculator-App.git
   cd Investment-Calculator-App/investment_calculator_app
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   pip install -r requirements-dev.txt
   ```

## Running Tests

Run the test suite with pytest:
```bash
pytest tests/ -v
```

For coverage report:
```bash
pytest tests/ --cov=. --cov-report=html
```

## Code Quality

Before submitting a PR, ensure your code passes all quality checks:

### Linting
```bash
flake8 .
```

### Code Formatting
We use Black for code formatting:
```bash
black . --check  # Check formatting
black .          # Apply formatting
```

## Running the Application Locally

```bash
python app.py
```

Then visit http://localhost:5000 in your browser.

## Running with Docker

```bash
docker build -t investment-calculator .
docker run -p 5000:5000 investment-calculator
```

## Pull Request Process

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Run tests and linting
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to your branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

## Coding Standards

- Follow PEP 8 style guidelines
- Write docstrings for all functions and classes
- Add tests for new features
- Keep functions focused and single-purpose
- Use type hints where appropriate

## Reporting Bugs

Please use GitHub Issues to report bugs. Include:
- Description of the bug
- Steps to reproduce
- Expected behavior
- Actual behavior
- Environment details (OS, Python version, etc.)

## Feature Requests

We welcome feature requests! Please open an issue with:
- Clear description of the feature
- Use case / motivation
- Proposed implementation (if you have ideas)

## Questions?

Feel free to open an issue for any questions about contributing.
