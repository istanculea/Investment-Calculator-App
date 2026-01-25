# Investment Calculator Web Application

This repository contains a Flask‑based web application that acts as an interactive investment calculator.  The app lets you project the future value of a portfolio that begins with a **lump‑sum investment** and grows through regular contributions.  It also helps you understand the impact of different compounding intervals, contribution schedules, and inflation on your returns.  A detailed schedule and chart give you a year‑by‑year view of how your balance evolves.

## Motivation

When you invest money you often combine a single starting deposit with recurring contributions.  The time value of money means that both the size and timing of those payments matter.  Financial references show that the future value of a constant stream of payments (an *ordinary annuity*) growing at a periodic rate `i` can be calculated as:

\[\text{FV}_{\text{annuity}} = \frac{R\left((1 + i)^n - 1\right)}{i}\]\【621504373427111†L74-L90】

where:

* `R` is the payment each period.
* `i` is the interest rate per period.
* `n` is the number of payments.

If you also start with an initial lump sum `PV`, the total future value after `n` periods is given by the sum of the compound growth of the lump sum and the annuity factor:

\[\text{FV} = PV\,(1 + i)^n + \frac{R\left((1 + i)^n - 1\right)}{i}\]\【621504373427111†L74-L90】

This formula assumes contributions are made at the end of each period (an **ordinary annuity**).  If payments are made at the beginning of each period (an **annuity due**) the second term is multiplied by an additional factor of `(1 + i)`.  Our application supports both payment timings.  For scenarios where contributions grow each year at a constant rate `g`, the formula adapts to:

\[\text{FV}_{\text{growing}} = \frac{R}{i - g}\Bigl((1 + i)^n - (1 + g)^n\Bigr)\times (1 + iT)\]\【871895981983830†L271-L388】

where `T` is `0` for ordinary annuities and `1` for annuities due.  These formulas come from time‑value‑of‑money derivations, and the app falls back to simulation when growth rates or payment timings make a closed‑form solution less stable.

Inflation reduces the **purchasing power** of your investments.  To compare today’s dollars with future dollars, the real future value can be found by deflating the nominal future value using the inflation rate.  Finance tutorials explain this adjustment as:

\[\text{Real Future Value} = \frac{\text{Nominal Future Value}}{(1 + \text{Inflation Rate})^n}\]\【870213610722547†L37-L45】.

Our calculator reports both the nominal future value and its inflation‑adjusted real value.

## Features

* **Flexible compounding and contribution frequencies** – choose monthly, quarterly or yearly compounding separately from the contribution schedule.
* **Payment timing** – specify whether contributions happen at the *beginning* or *end* of each period (annuity due vs. ordinary annuity).
* **Contribution growth rate** – model a constant annual increase in contributions to simulate salary raises or planned increases.
* **Inflation adjustment** – enter an annual inflation rate to see your results in today’s dollars using the purchasing power formula【870213610722547†L37-L45】.
* **Detailed schedule** – view a year‑by‑year table showing cumulative contributions and portfolio balance.
* **Interactive chart** – a line chart generated with Matplotlib illustrates how your balance grows over time.
* **Responsive interface** – built with Flask and Bootstrap, the app runs locally in a browser on desktop or mobile.

## Getting Started

### Prerequisites

* Python 3.10 or later.
* [pip](https://pip.pypa.io/) for installing dependencies.

### Installing

1. **Clone the repository**:
   ```
   git clone https://github.com/your‑username/investment‑calculator‑app.git
   cd investment‑calculator
   ```

2. **Create a virtual environment and install dependencies**:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows use venv\Scripts\activate
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

### Running the Application

After installing the dependencies, start the Flask development server with:

```
python app.py
```

By default the app will listen on `http://localhost:5000`.  Open this URL in your browser and enter your investment parameters.  Submitting the form will display the projected balances, chart and schedule.

### Containerized Deployment

A `Dockerfile` is included for easy deployment in containerized environments.  To build and run the container locally:

```
docker build -t your‑username/investment‑calculator-app .
docker run -p 5000:5000 your‑username/investment‑calculator-app
```

Visit `http://localhost:5000` to use the calculator.  See the commentary in the Dockerfile for details on the base image and dependency installation.

## Testing

The project includes automated tests using [pytest](https://pytest.org/).  Unit tests validate the core calculation functions against known formulas, and integration tests exercise the Flask routes using the test client.

To run the tests, install the additional testing dependency (`pytest`) and execute:

```
pip install pytest
pytest
```

You should see output indicating that all tests pass.  Writing tests helps ensure that future changes do not break the financial logic or web interface.

## License

This project is licensed under the MIT License.  See the `LICENSE` file for details.
