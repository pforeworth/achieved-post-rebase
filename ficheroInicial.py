# pip install requests
import requests

def fetch(url: str):
    r = requests.get(url, timeout=5)
    r.raise_for_status()
    return r.json()

if __name__ == "__main__":
    print(fetch("https://api.github.com"))
    print(fetch("cambio2 master"))
    print(fetch("cambio2 master"))
    print(fetch("cambio2 master"))
