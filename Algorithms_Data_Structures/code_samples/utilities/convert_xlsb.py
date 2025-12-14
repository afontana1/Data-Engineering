from pyxlsb import open_workbook
import csv
import time

file_name = ""
expected_sheet = "Raw Data"


class TimerError(Exception):
    """A custom exception used to report errors in use of Timer class"""


class Timer:
    def __init__(self):
        self._start_time = None

    def start(self):
        """Start a new timer"""
        if self._start_time is not None:
            raise TimerError(f"Timer is running. Use .stop() to stop it")

        self._start_time = time.perf_counter()

    def stop(self):
        """Stop the timer, and report the elapsed time"""
        if self._start_time is None:
            raise TimerError(f"Timer is not running. Use .start() to start it")

        elapsed_time = time.perf_counter() - self._start_time
        self._start_time = None
        print(f"Elapsed time: {elapsed_time:0.4f} seconds")


def convert_xlsb(new_file_name, old_file_name):
    """Convert XLSB to CSV"""
    with open(new_file_name + ".csv", "w", newline="") as file_handle:
        csv_writer = csv.writer(file_handle)
        print("opening worksheets")
        with open_workbook(old_file_name) as wb:
            print("Opened workbook")
            if expected_sheet not in wb.sheets:
                return False
            print("Getting {}".format(expected_sheet))
            with wb.get_sheet(expected_sheet) as sheet:
                for row in sheet.rows():
                    csv_writer.writerow([r.v for r in row]),
    return True


t = Timer()
t.start()
convert_xlsb(file_name.strip(".xlsb"), file_name)
t.stop()
