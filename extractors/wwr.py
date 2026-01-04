from playwright.sync_api import sync_playwright
import time
from bs4 import BeautifulSoup
import csv

class WwrJobScrapper:
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
            page.goto(f"https://weworkremotely.com/remote-jobs/search?utf8=%E2%9C%93&term={keyword}")

            for x in range(3):
                time.sleep(2)
                page.keyboard.down("End")

            content = page.content()
            soup = BeautifulSoup(content, "html.parser")

            ul = soup.find("ul")
            if not ul:
                continue 

            jobs = soup.find_all("li", class_="new-listing-container feature")
            jobs_db = []

            for job in jobs:
                title = job.find("h3", class_="new-listing__header__title").text
                company_name = job.find("p", class_="new-listing__company-name").text
                link = f"https://weworkremotely.com{job.find('a')['href']}"

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
        


def extract_wwr_jobs(keyword):
    scrapper = WwrJobScrapper()
    scrapper.add_keyword(keyword)
    return scrapper.start()

