import requests
from playwright.sync_api import sync_playwright

URL = "https://www.milleni.com.tr/internet-altyapi-sorgulama"


def run():
    # Önce basit bir HTTP isteğiyle bağlantıyı test edelim
    try:
        r = requests.get(URL, timeout=15)
        print(f"requests ile bağlantı OK, status: {r.status_code}")
    except Exception as e:
        print(f"requests ile bağlantı BAŞARISIZ: {e}")

    # Şimdi Playwright ile deneyelim, daha kısa timeout ve daha hafif bekleme
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        try:
            page.goto(URL, wait_until="domcontentloaded", timeout=20000)
            print("Playwright goto başarılı")
            page.screenshot(path="debug_screenshot.png", full_page=True)
            with open("debug_page.html", "w", encoding="utf-8") as f:
                f.write(page.content())
        except Exception as e:
            print(f"Playwright goto BAŞARISIZ: {e}")
        browser.close()


if __name__ == "__main__":
    run()
