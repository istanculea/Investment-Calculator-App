"""Unit and integration tests for the investment calculator.

These tests use pytest to verify the correctness of the financial
calculations and the Flask routes.  Running them helps ensure that
future modifications do not inadvertently change the calculation
behavior or break the web interface.
"""

from importlib import import_module

import pytest

import math

# Import the app module dynamically to avoid side effects during test collection.
app_module = import_module("investment_calculator.app")


def test_calculate_future_value_no_contributions():
    """A simple lump‑sum investment should grow by compound interest."""
    initial = 1000.0
    periodic = 0.0
    rate = 0.05  # 5% annual interest
    years = 2
    # Monthly compounding and no contributions
    compounding_per_year = 12
    contributions_per_year = 0
    fv = app_module.calculate_future_value(
        initial, periodic, rate, years, compounding_per_year,
        contributions_per_year, payment_timing="end", contribution_growth_rate=0.0,
    )
    # Expected future value using compound interest formula: FV = PV*(1 + i)^n
    period_rate = rate / compounding_per_year
    n = years * compounding_per_year
    expected_fv = initial * (1 + period_rate) ** n
    assert math.isclose(fv, expected_fv, rel_tol=1e-6)


def test_calculate_future_value_with_contributions():
    """Future value with regular contributions should match the annuity formula."""
    initial = 0.0
    periodic = 200.0  # Contribution per period
    rate = 0.06  # 6% annual interest
    years = 1
    compounding_per_year = 12
    contributions_per_year = 12  # Monthly payments
    fv = app_module.calculate_future_value(
        initial, periodic, rate, years, compounding_per_year,
        contributions_per_year, payment_timing="end", contribution_growth_rate=0.0,
    )
    period_rate = rate / compounding_per_year
    n = years * compounding_per_year
    # Future value formula for lump sum 0 plus ordinary annuity contributions
    expected_fv = periodic / period_rate * ((1 + period_rate) ** n - 1)
    assert math.isclose(fv, expected_fv, rel_tol=1e-6)


def test_flask_index_route():
    """The index route should render successfully and handle form submissions."""
    # Use Flask's test client
    app = app_module.app
    app.testing = True
    with app.test_client() as client:
        # GET request should return status 200
        resp = client.get("/")
        assert resp.status_code == 200
        # POST request with valid data
        data = {
            "initial_investment": "1000",
            "periodic_contribution": "100",
            "contribution_frequency": "monthly",
            "compounding_frequency": "monthly",
            "annual_interest_rate": "5",
            "years": "1",
            "inflation_rate": "2",
            "payment_timing": "end",
            "contribution_growth_rate": "0",
        }
        resp = client.post("/", data=data, follow_redirects=True)
        assert resp.status_code == 200
        # The response should include the calculated future value and real value strings
        # A simple check is to ensure the HTML contains a currency amount
        assert b"Future Value" in resp.data
        assert b"Real Value" in resp.data
