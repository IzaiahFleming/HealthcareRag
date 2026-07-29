"""Generate SYNTHETIC PHI-laden text to TEST the redaction guardrail.
This is fake data from Faker -- never put real patient data anywhere in this repo.
"""
from faker import Faker

fake = Faker()


def fake_note():
    return (
        f"Patient {fake.name()} (DOB {fake.date_of_birth().isoformat()}, "
        f"MRN {fake.numerify('MRN-#######')}, SSN {fake.ssn()}) was seen at "
        f"{fake.address().replace(chr(10), ', ')}. Contact: {fake.phone_number()}."
    )


if __name__ == "__main__":
    print(fake_note())
