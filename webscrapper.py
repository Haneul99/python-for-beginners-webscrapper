import requests
from bs4 import BeautifulSoup

indeed_result = requests.get("https://www.indeed.com/jobs?q=python&limit=50")

indeed_soup = BeautifulSoup(indeed_result.text, "html.parser")

pagination = indeed_soup.find("div", {"class": "pagination"})

pages = pagination.find_all('a')
spans = []
for page in pages:
    spans.append(page.find("span"))
spans = spans[:-1] #-1은 마지막 idx 전까지를 의미함. 0:-1 의 경우 0번째 idx부터 마지막 직전 idx까
print(spans)
