import requests
from bs4 import BeautifulSoup

LIMIT = 50
URL = f"https://www.indeed.com/jobs?q=python&limit={LIMIT}"


def extract_pages():
    result = requests.get(URL)
    soup = BeautifulSoup(result.text, "html.parser")
    pagination = soup.find("div", {"class": "pagination"})
    links = pagination.find_all('a')
    pages = []
    for link in links[:-1]:
        pages.append(int(link.string))
        #-1은 마지막 idx 전까지를 의미함. 0:-1 의 경우 0번째 idx부터 마지막 직전 idx까
        #여기서는 pagination 부분에서 string이 숫자밖에 없기 때문에 find('span').string과 결과가 동일
    max_page = pages[-1]
    return max_page

def extract_job(html):
    title = html.find("h2", {"class": "title"}).find("a")["title"]
    company = html.find("span", {"class": "company"})
    company_anchor = company.find("a")
    if company_anchor is not None:
        company = str(company_anchor.string)
    else:
        company = str(company.string)
    company = company.strip()
    location = html.find("div", {"class": "recJobLoc"})["data-rc-loc"]
    job_id = html["data-jk"]
    return {
        'title': title,
        'company': company,
        'location': location,
        'link': f"https://www.indeed.com/viewjob?jk={job_id}"
    }


def extract_indeed_jobs(last_page):
    jobs = []
    for page in range(1):
        result = requests.get(f"{URL}&start={page*LIMIT}")
        soup = BeautifulSoup(result.text, "html.parser")
        results = soup.find_all("div", {"class": "jobsearch-SerpJobCard"})
        for result in results:
            job = extract_job(result)
            jobs.append(job)
    return jobs

def get_jobs():
    last_page = extract_pages()
    indeed_jobs = extract_indeed_jobs(last_page)
    return indeed_jobs

