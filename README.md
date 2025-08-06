# pychoam

`pychoam` is a minimal event-driven trading framework for Interactive Brokers built on
`ib_insync`.  It supports both live trading and CSV-based back-testing with identical
strategy logic.

## Installation

```bash
pip install -e .[dev]
cp .env.example .env  # then edit credentials
```

## Usage

Back-test a CSV file:

Provide a CSV with columns `ts,o,h,l,c,v` and run:

```bash
pychoam backtest --file path/to/data.csv
```

Run against a live IB paper account:

```bash
pychoam live --env .env
```

## Notes

* Designed for educational purposes only.
* Ensure you are connected to IB's paper-trading gateway before running the live
  command.
