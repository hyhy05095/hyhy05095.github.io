from playwright.sync_api import sync_playwright
import time
from bs4 import BeautifulSoup
import csv

class BerlinJobScrapper:
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
            page.goto(f"https://berlinstartupjobs.com/skill-areas/{keyword}/")

            for x in range(3):
                time.sleep(3)
                page.keyboard.down("End")

            content = page.content()
            soup = BeautifulSoup(content, "html.parser")

            
            ul = soup.find("ul", class_="jobs-list-items")
            if not ul:
                return

            jobs = ul.find_all("li", class_="bjs-jlid")
            jobs_db = []

            for job in jobs:
                title = job.find("h4", class_="bjs-jlid__h").text.strip() if job.find("h4", class_="bjs-jlid__h") else "N/A"
                company_name = job.find("a", class_="bjs-jlid__b").text.strip() if job.find("a", class_="bjs-jlid__b") else "N/A"
                link = job.find("a")["href"] if job.find("a") and "href" in job.find("a").attrs else "N/A"

                job = {
                    "title":title,
                    "company_name":company_name,
                    "link":link
                }
                jobs_db.append(job)

            self.result.extend(jobs_db);
            page.close()
        self.reset()
        self.p.stop()
        return self.result
        


def extract_berlin_jobs(keyword):
    scrapper = BerlinJobScrapper()
    scrapper.add_keyword(keyword)
    return scrapper.start()

