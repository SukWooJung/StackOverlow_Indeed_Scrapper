import requests
from bs4 import BeautifulSoup

def get_last_page(url):
  result = requests.get(url)

  #모든 html 결과 가져오기
  #print(indeed_result.text)
 
  #Extract data from html 
  soup = BeautifulSoup(result.text, "html.parser") 

  pagination = soup.find("div",{"class":"pagination"})

  # print(pagination)

  links = pagination.find_all("a")

  # print(pages)
  # link.find("span")
  pages = []
  for link in links[0:-1]:
   pages.append(int(link.string))
  # print(spans[:-1])
  max_page = pages[-1]
  return max_page

def extract_job(html):   
  #title
  title = html.find("h2", {"class":"title"}).find("a")["title"]

  #company
  company = html.select_one("div.sjcl span.company")

  company_anchor = company.find("a")
  if company_anchor is not None:
    company = str(company_anchor.string)
  else:
    company = str(company.string)
  company = company.strip()
  
  #location
  #location = html.select_one("span.location")
  location = html.find("span",{"class":"location"}).string
  
  #job_id
  job_id = html["data-jk"]
  
  return {"title":title, "company":company, "location":location, "link":f"https://kr.indeed.com/viewjob?jk={job_id}&from=serp&vjs=3"}

def extract_jobs(last_pages, url, limit):
  
  jobs = []
  for page in range(last_pages):  
    print(f"Scrapping Indeed: Page: {page}")
    url_text = requests.get(f"{url}&start={page*limit}")
    soup = BeautifulSoup(url_text.text, "html.parser")
    results = soup.find_all("div", {"class":"jobsearch-SerpJobCard"})
    for result in results:
      job = extract_job(result)
      jobs.append(job)
  return jobs
    
def get_jobs(word):  
  limit = 50
  url = f"https://kr.indeed.com/%EC%B7%A8%EC%97%85?q={word}&radius=0&limit={limit}"

  last_page = get_last_page(url)
  
  jobs = extract_jobs(last_page, url, limit)
  return jobs

