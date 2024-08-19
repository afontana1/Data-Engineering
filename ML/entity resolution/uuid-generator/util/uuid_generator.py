import uuid
import hashlib

from typing import Optional, Callable, Type, TypeVar
import typing

import re
import math
from unidecode import unidecode
from functools import partial, reduce
import string

import nltk

nltk.download("stopwords")
from nltk.corpus import stopwords

from .regex_patterns import CommonRegex
from .phone_parser import PhoneParser


class uuidGenerator:
    def __init__(
        self,
        email: str = "",
        source_system: str = "",
        first_name: Optional[str] = "",
        last_name: Optional[str] = "",
        phone: Optional[str] = "",
        address: Optional[str] = "",
    ):
        self.email = email
        self.source_system = source_system
        self.first_name = first_name
        self.last_name = last_name
        self.phone = phone
        self.address = address

    def generate_hash(self, **kwargs) -> uuid.UUID:
        """Generate uuid5 using sha1 hash algorithm.

        Args:
            email (str): required from source system
            source_system (str): source name
            first_name (str): optional
            last_name (str): optional
            phone (str): optional
            address (str): optional
        Return:
            unique object identifier (UUID)
        """
        identifiers = []
        for key, value in kwargs.items():
            if isinstance(value, list):
                identifiers.append(value[0])
            else:
                identifiers.append(value)
        identifier = "#".join(identifiers)
        return uuid.uuid5(uuid.NAMESPACE_OID, identifier)

    def normalize(self) -> dict:
        """Normalize input parameters."""
        normalized_parameters = {}
        for arg, parameter in self.__dict__.items():
            if arg == "address":
                normalized_address = self.normalize_address(input_string=parameter)
                address_parsed = self.parse_address(input_string=normalized_address)
                if address := address_parsed.get("street_addresses"):
                    normalized_parameters[arg] = address
                if po_box := address_parsed.get("po_box"):
                    normalized_parameters["po_box"] = po_box
                if state_code := address_parsed.get("state_code"):
                    normalized_parameters["state_code"] = state_code
                if zip_code := address_parsed.get("zip_code"):
                    normalized_parameters["zip_code"] = zip_code
                if state_name := address_parsed.get("state_names"):
                    normalized_parameters["state_name"] = state_name
            elif "name" in arg:
                normalized_parameters[arg] = self.normalize_name(input_string=parameter)
            elif arg == "source_system":
                normalized_parameters[arg] = parameter.lower().strip()
            elif arg == "phone":
                if normalized_number := self.normalize_number(arg):
                    for attr in ["countryCode", "areaCode", "phoneNumber", "extension"]:
                        if value := normalized_number.get(attr):
                            normalized_parameters[attr] = value
                else:
                    # Not a valid number
                    normalized_parameters[arg] = ""
            else:
                normalized_parameters[arg] = self.normalize_email(parameter)

        return normalized_parameters

    def parse_address(self, input_string: str) -> CommonRegex:
        return CommonRegex(input_string)

    def transform_encoding(self, input_string: str) -> str:
        return unidecode(input_string)

    def transform_case(self, input_string: str) -> str:
        return input_string.lower().strip()

    def remove_punctuation(self, input_string: str) -> str:
        return "".join([ch for ch in input_string if ch not in set(string.punctuation)])

    def normalize_email_string(self, email: str) -> str:
        """Normalize the email address by lowercasing the domain part of the it."""
        email = email or ""
        try:
            email_name, domain_part = email.strip().rsplit("@", 1)
        except ValueError:
            pass
        else:
            email = "@".join([email_name, domain_part.lower()])
        return email

    def remove_stopwords(
        self,
        input_string: str,
        stopwords: nltk.corpus.reader.wordlist.WordListCorpusReader = stopwords.words(
            "english"
        ),
    ) -> str:
        return " ".join(
            [word for word in input_string.split() if word not in stopwords]
        )

    def normalize_name(self, input_string: str) -> Callable:
        pipeline = [
            self.transform_encoding,
            self.transform_case,
            self.remove_punctuation,
        ]
        return reduce((lambda value, func: func(value)), pipeline, input_string)

    def normalize_address(
        self,
        input_string: str,
        stopwords: nltk.corpus.reader.wordlist.WordListCorpusReader = stopwords.words(
            "english"
        ),
    ) -> Callable:
        pipeline = [
            self.transform_encoding,
            self.transform_case,
            self.remove_punctuation,
            partial(self.remove_stopwords, stopwords=stopwords),
        ]
        return reduce((lambda value, func: func(value)), pipeline, input_string)

    def normalize_number(self, phone: str) -> PhoneParser:
        validation = CommonRegex(phone)
        if not validation.get("phone_number"):
            return ""
        return PhoneParser.parse(phone)

    def normalize_email(self, email: str) -> str:
        validation = CommonRegex(email)
        if not validation.get("emails"):
            return ""
        return self.normalize_email_string(email)

    def create_hash(self) -> uuid.UUID:
        """Main function for generating Hash."""
        normalized_parameters = self.normalize()
        print(normalized_parameters)
        uuid = self.generate_hash(**normalized_parameters)
        return uuid


if __name__ == "__main__":
    x = uuidGenerator(
        email="ajfontana78@gmail.com",
        source_system="Tock",
        first_name="AJ",
        last_name="Fontana",
        phone="555-5555",
        address="3421 Rhone Drive, Ceres Ca",
    )

    print(x.__dict__)
    print(x.create_hash())
