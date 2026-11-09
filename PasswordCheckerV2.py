print("VERSION 2 RUNNING")

import string
import hashlib
import requests

def load_common_passwords(filename):
    with open(filename, encoding="utf-8", errors="ignore") as f:
        return set(line.strip() for line in f)


def times_pwned(pw):
    sha1 = hashlib.sha1(pw.encode("utf-8")).hexdigest().upper()
    prefix = sha1[:5]
    suffix = sha1[5:]

    url = f"https://api.pwnedpasswords.com/range/{prefix}"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
    except requests.RequestException:
        return None

    for line in response.text.splitlines():
        hash_suffix, count = line.split(":")
        if hash_suffix == suffix:
            return int(count)
        return 0

def check_strengh(pw, common):
    if pw in common:
        return 0, ["This is a very common password. Attackers try these first."]

    pwned = times_pwned(pw)
    if pwned is None:
        print("(Couldnt reach Have I Been Pwned, skipping the breach check...)")
    elif pwned > 0:
        return 0, [f"This password has appeared in data breaches {pwned:,} times. Don's use it."]
    else:
        print("Good news: not found in any known data breaches.")
    

    score = 0
    tips = []

    if len(pw) >= 12:
        score += 1
    else:
        tips.append("Make it atleast 12 characters long")

    if any(c.islower() for c in pw):
        score += 1
    else:
        tips.append("Add a lowercase letter.")

    if any(c.isupper() for c in pw):
        score += 1
    else:
        tips.append("Add a number.")

    if any(c in string.punctuation for c in pw):
        score += 1
    else:
            tips.append("Add a symbol like ! or #.")

    return score, tips


common = load_common_passwords("100k-most-used-passwords-NCSC.txt")
pw = input("Enter a password to test: ")
score, tips = check_strengh(pw, common)

print(f"Score: {score}/5")
for tip in tips:
    print("-", tip)