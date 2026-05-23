import re
import json

file = open("input/raw-text.txt", "r")
text = file.read()

# STEP 1: extract all emails
email_pattern = r"[A-Za-z0-9._%+-]+@[^ \n]+"
emails = re.findall(email_pattern, text)

# STEP 2: create empty lists
alu_official = []
alu_alumni = []
alu_si = []
invalid_emails = []

# STEP 3: loop through emails
for email in emails:

    if email.count("@") != 1:
        invalid_emails.append(email)
        continue

    if ".." in email:
        invalid_emails.append(email)
        continue

    if "." not in email:
        invalid_emails.append(email)
        continue

    if email.endswith("@alueducation.com"):
        alu_official.append(email)

    elif email.endswith("@alumni.alueducation.com"):
        alu_alumni.append(email)

    elif email.endswith("@si.alueducation.com"):
        alu_si.append(email)

    else:
        invalid_emails.append(email)
        # -----------------------------
# URL EXTRACTION
# -----------------------------

url_pattern = r"https?://[^\s]+"
urls = re.findall(url_pattern, text)

valid_urls = []
invalid_urls = []

for url in urls:

    # security check: script injection
    if "<script>" in url:
        invalid_urls.append(url)
        continue

    # basic malformed check
    if "htp" in url:
        invalid_urls.append(url)
        continue

    valid_urls.append(url)

print("\nEXTRACTED URLS:")
print(urls)

print("\nVALID URLS:")
print(valid_urls)

print("\nINVALID URLS:")
print(invalid_urls)
# -----------------------------
# PHONE NUMBER EXTRACTION
# -----------------------------

phone_pattern = r"(\+\d{1,3}[\s-]?\d{3}[\s-]?\d{3}[\s-]?\d{3,4}|\(\d{3}\)\s?\d{3}[\s-]?\d{4})"

phones = re.findall(phone_pattern, text)

valid_phones = []
invalid_phones = []

for phone in phones:

    # remove spaces for checking
    cleaned = phone.replace(" ", "").replace("-", "")

    # basic validation rules
    if len(cleaned) < 10:
        invalid_phones.append(phone)
        continue

    if cleaned.count("+") > 1:
        invalid_phones.append(phone)
        continue

    valid_phones.append(phone)

# -----------------------------
# PRINT RESULTS (OUTSIDE LOOP)
# -----------------------------

print("\nEXTRACTED PHONES:")
print(phones)

print("\nVALID PHONES:")
print(valid_phones)

print("\nINVALID PHONES:")
print(invalid_phones)
# -----------------------------
# CREDIT CARD EXTRACTION
# -----------------------------

card_pattern = r"\b(?:\d{4}[- ]?){3}\d{4}\b"
cards = re.findall(card_pattern, text)

valid_cards = []
masked_cards = []

for card in cards:

    # remove spaces and dashes for checking
    cleaned = card.replace(" ", "").replace("-", "")

    # must be 16 digits
    if len(cleaned) != 16:
        continue

    # mask card (SECURITY requirement)
    masked = cleaned[:4] + " ******** " + cleaned[-4:]

    valid_cards.append(cleaned)
    masked_cards.append(masked)

# -----------------------------
# PRINT OUTSIDE LOOP
# -----------------------------

print("\nEXTRACTED CREDIT CARDS:")
print(cards)

print("\nMASKED CREDIT CARDS:")
print(masked_cards)
# -----------------------------
# SAVE RESULTS TO JSON
# -----------------------------

output_data = {
    "emails": {
        "alu_official": alu_official,
        "alu_alumni": alu_alumni,
        "alu_si": alu_si,
        "invalid_emails": invalid_emails
    },

    "urls": {
        "valid_urls": valid_urls,
        "invalid_urls": invalid_urls
    },

    "phones": {
        "valid_phones": valid_phones,
        "invalid_phones": invalid_phones
    },

    "credit_cards": {
        "valid_cards": valid_cards,
        "masked_cards": masked_cards
    }
}

with open("output/sample-output.json", "w") as f:
    json.dump(output_data, f, indent=4)

print("\nJSON file created successfully!")