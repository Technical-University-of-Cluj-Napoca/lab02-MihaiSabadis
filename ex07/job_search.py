import sys
import requests
from bs4 import BeautifulSoup

def main():
    if len(sys.argv) != 2:
        print("Usage: python job_search.py <keyword>")
        sys.exit(1)

    keyword = sys.argv[1]
    url = "https://www.juniors.ro/jobs"
    params = {"q": keyword}
    headers = {"User-Agent": "Mozilla/5.0"}

    try:
        response = requests.get(url, params=params, headers=headers, timeout=10)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Error fetching jobs: {e}")
        sys.exit(1)

    soup = BeautifulSoup(response.text, "html.parser")
    jobs = soup.select("li.job")

    if not jobs:
        print("No jobs found.")
        sys.exit(0)

    print(f"\nTop {min(7, len(jobs))} results for '{keyword}':\n")

    for i, job in enumerate(jobs[:7], start=1):
        # Title
        title_tag = job.select_one(".job_header_title h3")
        title = title_tag.get_text(strip=True) if title_tag else "N/A"

        # Location and date
        strong_tag = job.select_one(".job_header_title strong")
        location, date = "N/A", "N/A"
        if strong_tag:
            parts = [p.strip() for p in strong_tag.get_text(strip=True).split("|")]
            if len(parts) >= 1:
                location = parts[0]
            if len(parts) >= 2:
                date = parts[1]

        # Technologies
        techs = [a.get_text(strip=True) for a in job.select(".job_tags a")]

        # Company
        company = "N/A"
        for li in job.select(".job_requirements li"):
            if li.get_text(strip=True).startswith("Companie"):
                company = li.get_text(strip=True).replace("Companie:", "").strip()
                break

        print(f"─────────────── {i} ───────────────")
        print(f"Title: {title}")
        print(f"Company: {company}")
        print(f"Location: {location}")
        print(f"Technologies: {', '.join(techs) if techs else 'N/A'}")
        print(f"Posted: {date}")
        print()

if __name__ == "__main__":
    main()
