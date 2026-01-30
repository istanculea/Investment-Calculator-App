r"""
Flask application that implements a complex investment calculator.

This calculator supports a lump‑sum initial investment, regular
contributions (annuity payments) and allows the user to choose a
frequency (monthly, quarterly or yearly).  The future value of the
investment can be computed using the standard time value of money
formulas.  For a constant contribution paid at the end of each period,
the future value of the investment is given by【871895981983830†L271-L388】:

    FV = PV (1 + i)^n + \frac{PMT}{i} \bigl((1 + i)^n - 1\bigr).

Here `PV` represents the initial lump sum, `PMT` the periodic
payment, `i` the periodic interest rate, and `n` the total number of
periods.  When payments are made at the beginning of each period
(an annuity due), the second term is multiplied by an additional
factor of (1 + i)【871895981983830†L271-L388】.  For growing annuities where each
payment increases by a constant growth rate `g`, the formula adapts to

    FV = \frac{PMT}{i - g} \bigl((1 + i)^n - (1 + g)^n\bigr) (1 + iT),

provided that `g` differs from `i`; if `g == i` the series reduces to
`PMT * n * (1 + i)^{n-1}`【871895981983830†L271-L388】.  The factor `T` equals 0 for
ordinary annuities and 1 for annuities due.  The application also
calculates the real value of the investment by adjusting the nominal
future value for inflation using the purchasing power method
described by Analytics Vidhya【226416388788434†L261-L274】.

In addition to computing future and real values, the app produces
a year‑by‑year schedule of balances and contributions and generates
a plot of investment growth over time.  Users can specify whether
their periodic contributions are made at the beginning or end of each
period and can optionally set an annual growth rate for their
contributions.
"""

from __future__ import annotations

import base64
import io
import logging
import os
from typing import List, Dict

from flask import Flask, render_template, request

import matplotlib
matplotlib.use('Agg')  # Use non‑interactive backend for server environments
import matplotlib.pyplot as plt


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Security headers
@app.after_request
def add_security_headers(response):
    """Add security headers to all responses."""
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'SAMEORIGIN'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
    response.headers['Content-Security-Policy'] = "default-src 'self'; style-src 'self' 'unsafe-inline'; img-src 'self' data:;"
    return response

# Secret key for session management (should be set via environment variable in production)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max request size


def calculate_future_value(
    initial_investment: float,
    periodic_contribution: float,
    annual_interest_rate: float,
    years: int,
    compounding_per_year: int,
    contributions_per_year: int,
    payment_timing: str = 'end',
    contribution_growth_rate: float = 0.0,
) -> float:
    """
    Compute the future value of an investment with optional contribution growth
    and flexible payment timing.

    This convenience function simulates the investment period by period
    using the ``generate_schedule`` helper.  It sums all interest and
    contributions to produce the final balance.  When the annual
    contribution growth rate is zero and the payment timing is at the
    end of each period, the result matches the closed‑form formula
    presented in financial references【871895981983830†L271-L388】.  For growing
    contributions or annuities due the schedule simulation handles the
    compounding explicitly.

    Parameters
    ----------
    initial_investment : float
        The initial lump sum invested at time zero.
    periodic_contribution : float
        The base payment amount made each contribution period.
    annual_interest_rate : float
        The nominal annual interest rate expressed as a decimal.
    years : int
        Total number of years the investment is held.
    compounding_per_year : int
        Number of compounding periods per year (e.g., 12 for monthly).
    contributions_per_year : int
        Number of contributions made per year (e.g., 4 for quarterly).
    payment_timing : str, optional
        Either ``'end'`` for an ordinary annuity or ``'beginning'`` for an
        annuity due.  Defaults to ``'end'``.
    contribution_growth_rate : float, optional
        Annual growth rate of the periodic contribution expressed as a
        decimal (e.g., 0.03 for 3% annual increase).  Defaults to zero
        (fixed payments).

    Returns
    -------
    float
        The future value of the investment at the end of the term.
    """
    schedule = generate_schedule(
        initial_investment,
        periodic_contribution,
        annual_interest_rate,
        years,
        compounding_per_year,
        contributions_per_year,
        payment_timing,
        contribution_growth_rate,
    )
    # The final balance is the balance at the last recorded year
    return schedule[-1]['balance'] if schedule else initial_investment


def generate_schedule(
    initial_investment: float,
    periodic_contribution: float,
    annual_interest_rate: float,
    years: int,
    compounding_per_year: int,
    contributions_per_year: int,
    payment_timing: str = 'end',
    contribution_growth_rate: float = 0.0,
) -> List[Dict[str, float]]:
    """
    Generate a year‑by‑year schedule of balances and contributions.

    The schedule is computed by iteratively applying periodic interest
    and contributions for each compounding period.  Contributions may
    optionally grow at a constant rate and can be made at either the
    beginning or end of each period.  When the annual growth rate is
    zero and payments occur at the end of each period, the results
    coincide with the closed‑form future value formulas for ordinary
    annuities【871895981983830†L271-L388】.  If the growth rate equals the
    periodic interest rate, the contributions behave as a special
    case noted in the financial derivations【871895981983830†L271-L388】.

    Parameters
    ----------
    initial_investment : float
        Present value of the initial lump sum.
    periodic_contribution : float
        Base payment amount for each contribution period.
    annual_interest_rate : float
        Nominal annual interest rate expressed as a decimal.
    years : int
        Total number of years for the investment horizon.
    compounding_per_year : int
        Number of compounding periods per year.
    contributions_per_year : int
        Number of contribution payments per year.
    payment_timing : str, optional
        ``'end'`` for payments at the end of each period (ordinary annuity)
        or ``'beginning'`` for payments at the beginning of each period
        (annuity due).  Defaults to ``'end'``.
    contribution_growth_rate : float, optional
        Annual growth rate of the contribution amounts as a decimal
        (e.g., 0.03 for 3% annual increase).  Defaults to zero.

    Returns
    -------
    list of dict
        Each entry contains ``year``, ``balance``, and ``total_contributions``.
    """
    # Handle cases with no compounding or contributions gracefully
    if years <= 0 or compounding_per_year <= 0:
        return []

    # Compute periodic interest rate
    period_rate = annual_interest_rate / compounding_per_year
    total_periods = years * compounding_per_year

    # Determine contribution payment interval in terms of compounding periods
    if contributions_per_year > 0:
        payment_interval = compounding_per_year // contributions_per_year
        if payment_interval == 0:
            # If contributions frequency is higher than compounding frequency,
            # treat contributions frequency equal to compounding frequency
            payment_interval = 1
            contributions_per_year = compounding_per_year
    else:
        payment_interval = None

    # Convert annual contribution growth rate to the growth rate per contribution period
    if contributions_per_year > 0:
        # Use compound growth per contribution period
        growth_per_period = (1 + contribution_growth_rate) ** (1 / contributions_per_year) - 1
    else:
        growth_per_period = 0.0

    # Initialize state variables
    balance = initial_investment
    total_contributions = initial_investment
    schedule: List[Dict[str, float]] = []
    payment_count = 0

    for period in range(1, total_periods + 1):
        # Determine if this period is a contribution period
        contribution_period = (
            contributions_per_year > 0 and payment_interval is not None and
            ((period - 1 if payment_timing == 'beginning' else period) % payment_interval == 0)
        )

        # If payment timing is 'beginning', deposit contributions before applying interest
        if payment_timing == 'beginning' and contribution_period:
            if periodic_contribution != 0:
                # Apply growth to contribution based on number of prior payments
                amount = periodic_contribution * ((1 + growth_per_period) ** payment_count)
                balance += amount
                total_contributions += amount
                payment_count += 1

        # Apply interest for this compounding period
        balance += balance * period_rate

        # If payment timing is 'end', deposit contributions after interest
        if payment_timing == 'end' and contribution_period:
            if periodic_contribution != 0:
                amount = periodic_contribution * ((1 + growth_per_period) ** payment_count)
                balance += amount
                total_contributions += amount
                payment_count += 1

        # Record year‑end values
        if period % compounding_per_year == 0:
            year = period // compounding_per_year
            schedule.append({
                'year': year,
                'balance': balance,
                'total_contributions': total_contributions
            })

    return schedule


@app.route('/', methods=['GET', 'POST'])
def index() -> str:
    """Render the main page and handle form submissions."""
    if request.method == 'POST':
        # Read form fields, converting to appropriate types
        try:
            initial_investment = float(request.form.get('initial_investment', 0))
            periodic_contribution = float(request.form.get('periodic_contribution', 0))
            contribution_frequency = request.form.get('contribution_frequency', 'monthly')
            # New: compounding frequency separate from contribution frequency
            compounding_frequency = request.form.get('compounding_frequency', contribution_frequency)
            annual_interest_rate = float(request.form.get('annual_interest_rate', 0)) / 100.0
            years = int(request.form.get('years', 0))
            inflation_rate = float(request.form.get('inflation_rate', 0)) / 100.0
            payment_timing = request.form.get('payment_timing', 'end')
            contribution_growth_rate = float(request.form.get('contribution_growth_rate', 0)) / 100.0
            
            # Input validation
            if initial_investment < 0 or periodic_contribution < 0:
                logger.warning("Negative investment values received")
                return render_template('index.html', error="Investment amounts cannot be negative.")
            
            if years <= 0 or years > 100:
                logger.warning(f"Invalid years value: {years}")
                return render_template('index.html', error="Years must be between 1 and 100.")
            
            if annual_interest_rate < -1 or annual_interest_rate > 1:
                logger.warning(f"Invalid interest rate: {annual_interest_rate}")
                return render_template('index.html', error="Interest rate must be between -100% and 100%.")
                
        except (TypeError, ValueError) as e:
            # If conversion fails, re‑render the index page with an error message
            logger.error(f"Invalid input: {e}")
            return render_template('index.html', error="Invalid input. Please enter numeric values.")

        # Map frequency string to periods per year
        freq_map = {
            'monthly': 12,
            'quarterly': 4,
            'yearly': 1
        }
        compounding_per_year = freq_map.get(compounding_frequency, 12)
        contributions_per_year = freq_map.get(contribution_frequency, 12)

        # Generate a detailed schedule based on the new parameters
        schedule = generate_schedule(
            initial_investment,
            periodic_contribution,
            annual_interest_rate,
            years,
            compounding_per_year,
            contributions_per_year,
            payment_timing,
            contribution_growth_rate,
        )

        # Calculate future value from the schedule
        future_value = schedule[-1]['balance'] if schedule else initial_investment

        # Compute the real (inflation‑adjusted) value
        real_value = future_value / ((1 + inflation_rate) ** years) if years > 0 else future_value

        # Extract series for plotting
        years_list = [entry['year'] for entry in schedule]
        balances_list = [entry['balance'] for entry in schedule]

        # Determine total contributions and interest earned
        total_contributions = schedule[-1]['total_contributions'] if schedule else initial_investment
        total_interest = future_value - total_contributions

        # Create a plot of the investment growth
        try:
            plt.figure(figsize=(8, 4))
            plt.plot(years_list, balances_list, marker='o', linestyle='-', color='#007bff')
            plt.title('Investment Growth Over Time')
            plt.xlabel('Year')
            plt.ylabel('Portfolio Value')
            plt.grid(True)
            buf = io.BytesIO()
            plt.savefig(buf, format='png', bbox_inches='tight')
            buf.seek(0)
            image_base64 = base64.b64encode(buf.read()).decode('utf-8')
            plt.close()
        except Exception as e:
            logger.error(f"Error generating plot: {e}")
            image_base64 = ""

        logger.info(f"Calculation completed: FV={future_value:.2f}, Years={years}")

        return render_template(
            'results.html',
            initial_investment=initial_investment,
            periodic_contribution=periodic_contribution,
            contribution_frequency=contribution_frequency,
            compounding_frequency=compounding_frequency,
            annual_interest_rate=annual_interest_rate * 100,
            years=years,
            inflation_rate=inflation_rate * 100,
            payment_timing=payment_timing,
            contribution_growth_rate=contribution_growth_rate * 100,
            future_value=future_value,
            real_value=real_value,
            total_contributions=total_contributions,
            total_interest=total_interest,
            schedule=schedule,
            img_data=image_base64
        )

    # Default GET request simply renders the form
    return render_template('index.html')


@app.route('/health')
def health():
    """Health check endpoint for monitoring and orchestration."""
    return {'status': 'healthy', 'version': '1.0.0'}, 200


if __name__ == '__main__':
    # Run the Flask development server.  In a production environment
    # the Flask application should be served via a WSGI server such as
    # gunicorn or uWSGI.
    app.run(debug=True, host='0.0.0.0', port=5000)