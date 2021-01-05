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
scraper = SearchScraper(driver=driver_type, email=email, password=password, driver_options=driver_options)
results = scraper.scrape(url='https://www.linkedin.com/search/results/people/?currentCompany=%5B%221441%22%5D&geoUrn=%5B%22102571732%22%5D&keywords=&network=%5B%22F%22%5D&origin=FACETED_SEARCH')

fields = ['LinkedIn URL', 'Full Name', 'Distance', 'Headline', 'First Name', 'Last Name', 'Location', 'Other Locations',
          'Undergrad', 'Other Schools', 'Yrs Exp', 'Int HS?', 'Grad Yr']
csvfile = open(filename + '.csv', 'w+', newline='')
csvwriter = csv.writer(csvfile)
csvwriter.writerow(fields)

for person in results:
    csvwriter.writerow([person['id'], person['name'], person['distance']])