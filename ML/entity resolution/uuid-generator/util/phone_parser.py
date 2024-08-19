import re
from typing import Optional, Callable, Type, TypeVar
import typing


class PhoneParser:
    def __init__(self, components: dict = {}):
        self.__dict__.update(components)

    @classmethod
    def matchCountryCode(
        cls, telephoneNo: str, defaultCountryCode: str = ""
    ) -> (str, str):
        # match phones starting with +
        parts = re.split(r"^\+(\d+)", telephoneNo)
        if len(parts) > 1:
            return parts[1], parts[2]

        parts = re.split(r"^(1)(\D.*)", telephoneNo)
        if len(parts) > 1:
            return parts[1], parts[2]
        else:
            # could return a default country code here
            return defaultCountryCode, telephoneNo

    @classmethod
    def matchExtension(cls, telephoneNo: str) -> list:
        matched = re.match(r"([^a-zA-Z]+)([a-zA-Z]+\D*)(\d+)", telephoneNo)
        if matched:
            parts = matched.groups()
            if len(parts) > 1:
                return parts[2], parts[0]
        return "", telephoneNo

    @classmethod
    def parseNumbers(cls, telephoneNo: str) -> list:
        parts = re.findall(r"(\d+)", telephoneNo)
        return parts

    @classmethod
    def parsePhoneNumber(cls, telephoneNo: str) -> dict:
        countryCode, areaCode, phoneNumber, extension = "", "", "", ""
        countryCode, phoneNumber = cls.matchCountryCode(telephoneNo)
        extension, phoneNumber = cls.matchExtension(phoneNumber)
        numbers = cls.parseNumbers(phoneNumber)
        numberOfParts = len(numbers)
        if numberOfParts > 1:
            areaCode = numbers[0]
            phoneNumber = "".join(numbers[1:])
        else:
            phoneNumber = "".join(numbers)

        return {
            "countryCode": countryCode,
            "areaCode": areaCode,
            "phoneNumber": phoneNumber,
            "extension": extension,
        }

    @classmethod
    def parse(cls, phone: str) -> TypeVar("T", bound="TrivialClass"):
        return cls(getattr(cls, "parsePhoneNumber")(phone))

    def get(self, key):
        return self.__dict__.get(key, "")


if __name__ == "__main__":
    testData = [
        "",
        "garbage",
        "garbage1231moregarbage",
        "0120-24-3343",
        "046-824-3721",
        "0468243721",
        "+1-222-333-4444",
        "(222) 333-4444",
        "222.333.4444",
        "1-222-333-4444",
        "222.333.4444 ex55",
        "222.333.4444 ex55",
        "222.333.4444 ex.55",
        "222.333.4444 ex.  55",
        "222.333.4444 extension 55",
        "222.333.4444 extension. 55",
        "222.333.4444 x55",
        "222.333.4444 x 55",
        "222.333.4444 x.55",
        "222.333.4444ex.55",
        "222.333.4444ex55",
        "222.333.4444ex 55",
        "222.333.4444ex. 55",
        "222.333.4444extension 55",
        "222.333.4444extension. 55",
        "222.333.4444x55",
        "222.333.4444x 55",
        "222.333.4444x.55",
    ]
    x = PhoneParser().parse("+1-422-833-5808x1315")
    phones = []
    for phone in testData:
        phones.append(PhoneParser().parse(phone))

    phones[0].phoneNumber
