from SearchScraper import SearchScraper
from selenium.webdriver import Chrome
from utils import HEADLESS_OPTIONS
import csv

url = input("URL:\t")
email = input("Email:\t")
password = input("Password:\t")

driver_options = HEADLESS_OPTIONS
driver_type = Chrome
scraper = SearchScraper(driver=driver_type, email=email, password=password, driver_options=driver_options)
results = scraper.scrape(url=url)

fields = ['LinkedIn URL', 'Full Name']
csvfile = open('searchURLs.csv', 'w+', newline='')
csvwriter = csv.writer(csvfile)
csvwriter.writerow(fields)

for person in results:
    csvwriter.writerow([person['id'], person['name']])