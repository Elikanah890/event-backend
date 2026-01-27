import csv
from typing import List, Dict

def parse_guest_csv(file_path: str) -> List[Dict]:
    """
    Parse CSV file containing guest info for production-ready insertion.

    Expected CSV columns:
    - full_name (required)
    - title
    - guest_type (VIP/NORMAL, defaults to NORMAL)
    - email
    - phone
    - organization
    - profile_photo_url
    - notes
    - is_active (defaults to True if empty)

    Returns list of dictionaries suitable for DB insertion.
    """
    guests: List[Dict] = []

    with open(file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)

        for row in reader:
            full_name = (row.get("full_name") or "").strip()
            if not full_name:
                continue  # skip invalid rows without a full name

            guest_type = (row.get("guest_type") or "NORMAL").strip().upper()
            if guest_type not in {"VIP", "NORMAL"}:
                guest_type = "NORMAL"

            # Handle boolean field for is_active
            is_active_str = (row.get("is_active") or "").strip().lower()
            is_active = not is_active_str in {"false", "0", "no"}

            guest = {
                "full_name": full_name,
                "title": (row.get("title") or "").strip() or None,
                "guest_type": guest_type,
                "email": (row.get("email") or "").strip() or None,
                "phone": (row.get("phone") or "").strip() or None,
                "organization": (row.get("organization") or "").strip() or None,
                "profile_photo_url": (row.get("profile_photo_url") or "").strip() or None,
                "notes": (row.get("notes") or "").strip() or None,
                "is_active": is_active,
            }

            guests.append(guest)

    return guests
