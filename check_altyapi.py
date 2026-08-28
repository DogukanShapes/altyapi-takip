import requests

sites = {
    "Google (kontrol)": "https://www.google.com",
    "Millenicom": "https://www.milleni.com.tr",
}

for name, url in sites.items():
    try:
        r = requests.get(url, timeout=10)
        print(f"{name}: OK, status {r.status_code}")
    except Exception as e:
        print(f"{name}: BAŞARISIZ - {e}")
