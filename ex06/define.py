import sys
import requests
from bs4 import BeautifulSoup

def main():
    if len(sys.argv) != 2:
        print("Usage: python define.py <word>")
        sys.exit(1)

    word = sys.argv[1]
    url = f"https://dexonline.ro/definitie/{word}"
    headers = {"User-Agent": "Mozilla/5.0"}

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Error fetching definition: {e}")
        sys.exit(1)

    soup = BeautifulSoup(response.text, "html.parser")

    # ✅ Try multiple possible containers
    defs = soup.find_all("div", class_="tree-def html")
    if not defs:
        defs = soup.select(".def, .defWrapper, article")

    if not defs:
        print(f"No definition found for '{word}'.")
        sys.exit(0)

    for i, block in enumerate(defs[:2], start=1):
        text = block.get_text(separator=" ", strip=True)
        print(f"{i}. {text}")

if __name__ == "__main__":
    main()
