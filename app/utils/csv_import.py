import csv
from typing import List, Dict

def parse_guest_csv(file_path: str) -> List[Dict]:
    """
    Parse CSV file containing guest info.
    Expected columns: name, title, guest_type, contact
    Returns list of dictionaries for DB insertion.
    """
    guests = []
    with open(file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            guest = {
                "name": row.get("name", "").strip(),
                "title": row.get("title", "").strip(),
                "guest_type": row.get("guest_type", "NORMAL").upper(),
                "contact": row.get("contact", "").strip()
            }
            guests.append(guest)
    return guests
