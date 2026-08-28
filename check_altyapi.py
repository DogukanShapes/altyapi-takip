"""
Adım 1: Keşif (diagnostic) scripti.
Bu script Millenicom altyapı sorgulama sayfasını açar, ekran görüntüsü alır,
sayfanın HTML'ini kaydeder ve tüm giriş alanlarını (input/select/button) listeler.
Amaç: form alanlarının gerçek yapısını görüp, bir sonraki adımda otomatik
adres girme + sorgulama scriptini doğru şekilde yazabilmek.
"""

from playwright.sync_api import sync_playwright

URL = "https://www.milleni.com.tr/internet-altyapi-sorgulama"


def run():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(URL, wait_until="networkidle", timeout=60000)
        page.wait_for_timeout(3000)

        page.screenshot(path="debug_screenshot.png", full_page=True)

        html = page.content()
        with open("debug_page.html", "w", encoding="utf-8") as f:
            f.write(html)

        elements = page.eval_on_selector_all(
            "input, select, button, [role='combobox'], [role='button'], [role='listbox'], [contenteditable]",
            """els => els.map(el => ({
                tag: el.tagName,
                type: el.type || null,
                id: el.id || null,
                name: el.name || null,
                placeholder: el.placeholder || null,
                aria_label: el.getAttribute('aria-label'),
                text: el.innerText ? el.innerText.trim().slice(0, 60) : null,
                class: el.className || null
            }))"""
        )
        with open("debug_elements.txt", "w", encoding="utf-8") as f:
            for e in elements:
                f.write(str(e) + "\n")

        page_text = page.inner_text("body").lower()
        has_captcha_hint = any(k in page_text for k in ["captcha", "doğrulama kodu", "robot değilim"])
        with open("debug_elements.txt", "a", encoding="utf-8") as f:
            f.write(f"\n--- Captcha ihtimali (kelime taraması): {has_captcha_hint} ---\n")

        browser.close()


if __name__ == "__main__":
    run()
