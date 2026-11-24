import csv
import re
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent


def normalize_name(row):
    name_parts = " ".join(row[:3]).split()
    row[:3] = name_parts[:3] + [""] * (3 - len(name_parts[:3]))
    return row


def normalize_phone(phone):
    phone_pattern = re.compile(
        r"(?:\+7|8)\s*\(?\s*(\d{3})\s*\)?\s*"
        r"(\d{3})[\s-]*(\d{2})[\s-]*(\d{2})"
        r"(?:\s*(?:\u0434\u043e\u0431\.?|\u0434\u043e\u043f\.?)\s*(\d+))?",
        re.IGNORECASE,
    )

    def replace(match):
        phone = f"+7({match.group(1)}){match.group(2)}-{match.group(3)}-{match.group(4)}"
        if match.group(5):
            phone += f" \u0434\u043e\u0431.{match.group(5)}"
        return phone

    return phone_pattern.sub(replace, phone)


def merge_contacts(contacts):
    merged = {}
    for contact in contacts:
        key = (contact[0], contact[1])
        if key not in merged:
            merged[key] = contact
            continue

        current = merged[key]
        for index, value in enumerate(contact):
            if not current[index] and value:
                current[index] = value

    return list(merged.values())


with open(BASE_DIR / "phonebook_raw.csv", encoding="utf-8") as file:
    contacts_list = list(csv.reader(file, delimiter=","))

header = contacts_list[0]
contacts_list = contacts_list[1:]

for contact in contacts_list:
    normalize_name(contact)
    contact[5] = normalize_phone(contact[5])

contacts_list = merge_contacts(contacts_list)

with open(BASE_DIR / "phonebook.csv", "w", encoding="utf-8", newline="") as file:
    datawriter = csv.writer(file, delimiter=",")
    datawriter.writerow(header)
    datawriter.writerows(contacts_list)
