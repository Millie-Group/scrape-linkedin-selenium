from SearchScraper import SearchScraper
from selenium.webdriver import Chrome
from utils import HEADLESS_OPTIONS
import csv

#url = input("URL:\t")
email = input("Email:\t")
password = input("Password:\t")
filename = input("Filename:\t")

driver_options = HEADLESS_OPTIONS
driver_type = Chrome
# Below if you want a blank Chrome tab when running searcher.py
# scraper = SearchScraper(driver=driver_type, email=email, password=password, driver_options=driver_options)

# Below  if you want a Chrome tab displaying the LinkedIn search when running searcher.py
scraper = SearchScraper(driver=driver_type, email=email, password=password, driver_options={})

# Insert LinkedIn URL below
results = scraper.scrape(url=)

fields = ['LinkedIn URL', 'Full Name', 'Distance', 'Headline', 'First Name', 'Last Name', 'Location', 'Other Locations',
          'Undergrad', 'Other Schools', 'Yrs Exp', 'Int HS?', 'Grad Yr']
csvfile = open(filename + '.csv', 'w+', newline='')
csvwriter = csv.writer(csvfile)
csvwriter.writerow(fields)

for person in results:
    csvwriter.writerow([person['id'], person['name'], person['distance']])
