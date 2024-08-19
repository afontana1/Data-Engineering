# Collatz Conjecture Explorer

This repository contains an API and a computation service for exploring and understanding the Collatz Conjecture, an unsolved problem in mathematics.

## Features

The Collatz Conjecture Explorer offers several features:

- Continual calculation of Collatz sequences starting from any given number, and storage of these results in a SQLite database.
- A RESTful API for querying the results of these calculations, including specific sequences, statistical summaries, and more.
- Ability to query Collatz sequences for a specific range of numbers or search sequences by specific criteria.
- Ability to retrieve the top N sequences with the highest number of steps, as well as average statistics over a specified number of sequences.
- The computation service automatically updates distribution statistics when it's shut down.

## Requirements

- Python 3.7 or newer
- SQLite3
- FastAPI
- Uvicorn (for serving the API)

## Installation

install the dependencies using pip:

```bash
pip install -r requirements.txt
```

## Usage

To start the computation service, run:

```bash
python collatz.py
```

The computation service will continually calculate Collatz sequences and store the results in a SQLite database.

To start the API, run:

```bash
uvicorn app:app --host 0.0.0.0 --port 8000
```

You can then access the API at http://localhost:8000. For example, to get the Collatz sequence for the number 6, you would access http://localhost:8000/collatz/6.

## API Endpoints

Here are some of the API endpoints you can use:

- /collatz/{num}: Get the Collatz sequence and its statistics for a specific starting number.
- /stats: Get the overall computation statistics, including the last checked number, total computation time, and average steps.
- /collatz/range/{start}/{end}: Get the Collatz sequences for a range of starting numbers.
- /collatz/top/{n}: Get the top N Collatz sequences with the highest number of steps.
- /collatz/average/{n}: Get the average number of steps and average max value over the last N Collatz sequences.
- /collatz/search/{number_of_steps}/{max_value}: Search for Collatz sequences by a specific number of steps and max value.
- /collatz/stats/hourly: Get the hourly Collatz computation statistics.
- /collatz/stats/distribution: Get the distribution statistics for Collatz computations. (Not yet implemented)

## Notes

The computation service can be interrupted with CTRL+C or by closing your CLI , at which point it will calculate and store distribution statistics.

The API includes a middleware for blocking requests from specific IPs. The list of blocked IPs can be updated by adding them to blocked_ips.txt and using the /refresh_block_list/{password} endpoint with the correct password.
