# Import the required modules
import os
import sqlite3
import logging
import datetime
from pydantic import BaseModel
from fastapi import FastAPI, Request, HTTPException, Depends
from starlette.responses import JSONResponse
from sqlalchemy.orm import Session
from starlette.middleware.base import BaseHTTPMiddleware


# Create logs directory if not exist
os.makedirs("logs", exist_ok=True)

# Configure logger
logger = logging.getLogger("uvicorn")
logger.setLevel(logging.INFO)

formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

handler = logging.FileHandler("logs/app.log")
handler.setFormatter(formatter)

logger.addHandler(handler)

# Initialize the FastAPI app
app = FastAPI(
    title="The Collatz Conjecture Explorer",
    description="This API provides insights and data related to the Collatz Conjecture, supporting exploration and visualization of Collatz sequences. Updates to come!",
    version="0.0.1",
)

blocked_ips = []  # List to store blocked IPs


# Function to update blocked IPs from a file
def update_blocked_ips():
    global blocked_ips
    with open("blocked_ips.txt", "r") as f:
        blocked_ips = f.read().splitlines()


update_blocked_ips()  # Update the blocked IP list when the application starts


# Middleware to block requests from specific IPs
class BlockListMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        ip = request.client.host  # Get the client IP

        # Check if IP is unique and log it
        try:
            with open("ip_addresses.txt", "r") as f:
                unique_ips = f.read().splitlines()
            if ip not in unique_ips:
                with open("ip_addresses.txt", "a") as f:
                    f.write(f"{ip}\n")
        except FileNotFoundError:
            # If file doesn't exist yet, we write the IP directly
            with open("ip_addresses.txt", "a") as f:
                f.write(f"{ip}\n")

        logger.info(f"Received a request from IP: {ip}")
        if ip in blocked_ips:
            logger.warning(f"Blocked a request from IP: {ip}")
            return JSONResponse({"error": "Access denied."}, status_code=403)

        response = await call_next(request)
        return response


# Add the middleware to the app
app.add_middleware(BlockListMiddleware)


# Pydantic model for a Collatz record
class CollatzRecord(BaseModel):
    starting_number: int
    number_of_steps: int
    max_value: int
    sequence_length: int
    convergence: int
    timestamp: str


# Function to get a database connection
def get_db():
    conn = sqlite3.connect("collatz.db")
    db = conn.cursor()
    yield db
    conn.close()


# API endpoints
@app.get(
    "/collatz/{num}",
    response_model=CollatzRecord,
    summary="Retrieve Collatz Sequence",
    description="Get the Collatz sequence and its statistics for a specific starting number.",
)
def read_collatz(num: int, db: Session = Depends(get_db)):
    logger.info(f"Accessing Collatz sequence for number: {num}")  # Log number access
    c = db.execute("SELECT * FROM collatz WHERE starting_number = ?", (num,))
    data = c.fetchone()
    if data is None:
        return {"error": "No data found for this number."}
    else:
        return CollatzRecord(
            starting_number=data[0],
            number_of_steps=data[1],
            max_value=data[2],
            sequence_length=data[3],
            convergence=data[4],
            timestamp=data[5],
        )


@app.get(
    "/stats",
    summary="Collatz Computation Statistics",
    description="Get the overall computation statistics, including the last checked number, total computation time, and average steps.",
)
def read_stats(db: Session = Depends(get_db)):
    c = db.execute(
        "SELECT MAX(starting_number), MIN(timestamp), MAX(timestamp) FROM collatz"
    )
    last_number, min_timestamp_str, max_timestamp_str = c.fetchone()
    c = db.execute("SELECT AVG(number_of_steps) FROM collatz")
    average_steps = c.fetchone()[0]

    if last_number is None:
        return {
            "last_checked_number": 0,
            "total_computation_time": 0,
            "average_steps": 0,
        }
    else:
        min_timestamp = datetime.datetime.strptime(
            min_timestamp_str, "%Y-%m-%d %H:%M:%S"
        )
        max_timestamp = datetime.datetime.strptime(
            max_timestamp_str, "%Y-%m-%d %H:%M:%S"
        )
        total_time = (max_timestamp - min_timestamp).total_seconds()
        return {
            "last_checked_number": last_number,
            "total_computation_time": total_time,
            "average_steps": average_steps,
        }


@app.get(
    "/collatz/range/{start}/{end}",
    summary="Collatz Sequences in Range",
    description="Get the Collatz sequences for a range of starting numbers.",
)
def read_collatz_range(start: int, end: int, db: Session = Depends(get_db)):
    c = db.execute(
        "SELECT * FROM collatz WHERE starting_number BETWEEN ? AND ?", (start, end)
    )
    data = c.fetchall()
    return [
        {
            "starting_number": x[0],
            "number_of_steps": x[1],
            "max_value": x[2],
            "sequence_length": x[3],
            "convergence": x[4],
            "timestamp": x[5],
        }
        for x in data
    ]


@app.get(
    "/collatz/top/{n}",
    summary="Top N Collatz Sequences",
    description="Get the top N Collatz sequences with the highest number of steps.",
)
def read_top_collatz(n: int, db: Session = Depends(get_db)):
    c = db.execute("SELECT * FROM collatz ORDER BY number_of_steps DESC LIMIT ?", (n,))
    data = c.fetchall()
    return [
        {
            "starting_number": x[0],
            "number_of_steps": x[1],
            "max_value": x[2],
            "sequence_length": x[3],
            "convergence": x[4],
            "timestamp": x[5],
        }
        for x in data
    ]


@app.get(
    "/collatz/average/{n}",
    summary="Average Collatz Statistics",
    description="Get the average number of steps and average max value over the last N Collatz sequences.",
)
def read_average_collatz(n: int, db: Session = Depends(get_db)):
    c = db.execute(
        "SELECT AVG(number_of_steps), AVG(max_value) FROM (SELECT * FROM collatz ORDER BY starting_number DESC LIMIT ?)",
        (n,),
    )
    avg_steps, avg_max = c.fetchone()
    return {"average_number_of_steps": avg_steps, "average_max_value": avg_max}


@app.get(
    "/collatz/search/{number_of_steps}/{max_value}",
    summary="Search Collatz Sequences",
    description="Search for Collatz sequences by a specific number of steps and max value.",
)
def read_search_collatz(
    number_of_steps: int, max_value: int, db: Session = Depends(get_db)
):
    c = db.execute(
        "SELECT * FROM collatz WHERE number_of_steps = ? AND max_value = ?",
        (number_of_steps, max_value),
    )
    data = c.fetchall()
    return [
        {
            "starting_number": x[0],
            "number_of_steps": x[1],
            "max_value": x[2],
            "sequence_length": x[3],
            "convergence": x[4],
            "timestamp": x[5],
        }
        for x in data
    ]


@app.get(
    "/collatz/stats/hourly",
    summary="Hourly Collatz Statistics",
    description="Get the hourly Collatz computation statistics.",
)
def read_hourly_stats(db: Session = Depends(get_db)):
    # Calculate the current time and one hour before the current time
    current_time = datetime.datetime.now()
    one_hour_ago = current_time - datetime.timedelta(hours=1)

    # Query to count the number of collatz computations in the last hour
    c = db.execute(
        "SELECT COUNT(*) FROM collatz WHERE timestamp BETWEEN ? AND ?",
        (one_hour_ago, current_time),
    )
    count = c.fetchone()[0]

    return {"collatz_count_last_hour": count}


@app.get(
    "/collatz/stats/distribution",
    summary="Collatz Distribution Statistics",
    description="Get the distribution statistics for Collatz computations. This feature is not yet implemented.",
)
def read_distribution():
    return {"message": "Distribution statistics not yet implemented"}


@app.post(
    "/refresh_block_list/{password}",
    summary="Refresh the IP Block List",
    description="Refreshes the IP block list. Requires the correct password.",
)
def refresh_block_list(password: str):
    correct_password = "collatz"  # change this
    if password == correct_password:
        update_blocked_ips()
        logger.info("IP block list has been updated")
        return {"message": "Block list successfully updated"}
    else:
        raise HTTPException(status_code=403, detail="Incorrect password.")
