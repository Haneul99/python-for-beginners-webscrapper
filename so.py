import requests
from bs4 import BeautifulSoup

URL = f"https://www.stackoverflow.com/jobs?q=python&sort=i"


def get_last_page():
    result = requests.get(URL)
    soup = BeautifulSoup(result.text, "html.parser")
    pages = soup.find("div", {"class": "s-pagination"}).find_all("a")
    max_page = pages[-2].get_text(strip=True)
    return int(max_page)


def extract_job(html):
    title = html.find("h2").find("a")["title"]
    company, location = html.find("h3").find_all("span", recursive=False)
    #리스트에 요소가 두개임을 알 때, 변수를 두개 적어주면 차례로 변수에 저장됨. company = list[0], location = list[1] 처럼 저장.
    #recursive = False를 하면, 겉의 두 span만 가져옴. span 내부의 span은 가져오지 않음.
    company = company.get_text(strip=True)
    location = location.get_text(strip=True).strip("-").strip("\n")
    job_id = html["data-jobid"]
    return {
        "title": title,
        "company": company,
        "location": location,
        "apply_link": f"https://www.stackoverflow.com/jobs/{job_id}"
    }


def extract_jobs(last_page):
    jobs = []
    for page in range(last_page):
        result = requests.get(f"{URL}&pg={page+1}")
        soup = BeautifulSoup(result.text, "html.parser")
        results = soup.find_all("div", {"class": "-job"})
        for result in results:
            job = extract_job(result)
            jobs.append(job)
    return jobs


def get_jobs():
    last_page = get_last_page()
    jobs = extract_jobs(last_page)
    return jobs
