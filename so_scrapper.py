import requests
from bs4 import BeautifulSoup

def get_last_page(url):
  html_text = requests.get(url)
  soup = BeautifulSoup(html_text.text, "html.parser")

  html_pages = soup.find("div",{"class":"s-pagination"}).find_all("a")
  
  pages = []
  for page in html_pages[0:-1]:
    pages.append(page.find("span").string)
  last_page = int(pages[-1])
  
  return last_page
  
def extract_jobs(last_page, url):
  jobs=[]
  for page in range(last_page):  
    print(f"Scrapping SO: Page:{page+1}")
    html_text = requests.get(f"{url}&pg={page+1}")
    soup = BeautifulSoup(html_text.text,"html.parser")
    htmls = soup.find_all("div",{"class":"-job"})
    
    for html in htmls:
      job = extract_job(html)
      jobs.append(job)  
      
  return jobs
  
def extract_job(html):
  # title
  title = html.find("h2",{"class":"mb4"}).find("a")["title"]
  
  # company and location
  company_row = html.find("h3",{"class":"fc-black-700"})
  company, location = company_row.find_all("span", recursive=False)
  company = str(company.string).strip()
  location = str(location.string).strip()
  # company.get_text(strip=True)
  # location.get_text(strip=True)
  
  # link
  data_jobid = html["data-jobid"]
  
  return {"title":title,"company":company, "location":location, "link":f"https://stackoverflow.com/jobs/{data_jobid}/"}

def get_jobs(word):
  url = f"https://stackoverflow.com/jobs?q={word}"
  last_page = get_last_page(url)
  jobs = extract_jobs(last_page, url)
  
  return jobs