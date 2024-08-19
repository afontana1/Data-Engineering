from faker import Faker
from dataclasses import dataclass, fields

from typing import Optional
import random

import pandas as pd


@dataclass
class Person:

    email: str
    source_system: str = ""
    first_name: Optional[str] = ""
    last_name: Optional[str] = ""
    phone: Optional[str] = ""
    address: Optional[str] = ""

    def __post_init__(self):
        if not self.source_system:
            self.source_system = random.choice(
                ["tock", "sfcc", "sfmc", "antares", "google"]
            )

    def dict(self):
        return {field.name: str(getattr(self, field.name)) for field in fields(self)}


class GenerateFakeData(Faker):
    def __init__(self, size: int = 10000):
        super().__init__()
        self.attrs = {
            "first_name": "first_name",
            "last_name": "last_name",
            "email": ["free_email", "company_email", "email"],
            "phone": ["phone_number"],
            "address": ["street_address", "address"],
        }
        self.size = size

    def generate_records(self) -> list[Person]:
        """Generate list of records."""
        self.people = people = []
        for i in range(self.size):
            people.append(
                Person(
                    email=getattr(self, random.choice(self.attrs.get("email")))(),
                    first_name=getattr(self, self.attrs.get("first_name"))(),
                    last_name=getattr(self, self.attrs.get("last_name"))(),
                    phone=getattr(self, random.choice(self.attrs.get("phone")))(),
                    address=getattr(self, random.choice(self.attrs.get("address")))(),
                )
            )
        return people

    def generate_random_data(self):
        cols = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        columns = [random.choice(cols) for i in range(10)]
        for i in range(self.size):
            record = {}
            for col in columns:
                record[col] = random.randint(0, 5000)
            yield record

    def get_people(self):
        for person in self.people:
            yield person.dict()

    def dataframe(self, add_random_data=False):
        """Convert into a dataframe"""
        if not hasattr(self, "people"):
            self.generate_records()

        if not add_random_data:
            return pd.DataFrame([person.dict() for person in self.people])

        records = []
        for data, person in zip(self.generate_random_data(), self.get_people()):
            record = {}
            record.update(person)
            record.update(data)
            records.append(record)
        return pd.DataFrame(records)
