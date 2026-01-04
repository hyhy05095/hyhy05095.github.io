from playwright.sync_api import sync_playwright
import time
from bs4 import BeautifulSoup
import csv

class Web3JobScrapper:
    def __init__(self):
        self.p = sync_playwright().start()
        self.browser = self.p.chromium.launch(headless=False)
        self.keywords = []
        self.result = []

    def add_keyword(self, keyword):
        if isinstance(keyword, list) == True:
            self.keywords = keyword
        elif isinstance(keyword, str) == True:
            self.keywords.append(keyword) 
        print(f"Keywords : {self.keywords}")

    def reset(self):
        self.keywords.clear()


    def start(self):
        for keyword in self.keywords:
            print(f"Scrapper {keyword}...")
            page = self.browser.new_page()
            page.goto(f"https://web3.career/{keyword}-jobs")

            for x in range(3):
                time.sleep(3)
                page.keyboard.down("End")

            content = page.content()
            soup = BeautifulSoup(content, "html.parser")

            jobs = soup.find_all("tr", class_="table_row", attrs={"data-jobid": True})
            jobs_db = []

            for job in jobs:
                link = f"https://web3.career/{job.find('a')['href']}"
                title = job.find("h2", class_="fs-6 fs-md-5 fw-bold my-primary").text
                company_name = job.find("h3", attrs={"data-jobid": True}).text
                job = {
                    "title":title,
                    "company_name":company_name,
                    "link":link
                }
                jobs_db.append(job)

            self.result.extend(jobs_db);
        self.reset()
        self.p.stop()
        return self.result
        


def extract_web3_jobs(keyword):
    scrapper = Web3JobScrapper()
    scrapper.add_keyword(keyword)
    return scrapper.start()

