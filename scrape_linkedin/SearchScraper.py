from Scraper import Scraper
import json
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import re
import demoji
import unidecode

import time
from utils import *

demoji.download_codes()

class SearchScraper(Scraper):
    """
    Scraper for Personal LinkedIn Profiles. See inherited Scraper class for
    details about the constructor.
    """

    def scrape(self, url=''):
        self.driver.get(url)
        try:
            myElem = WebDriverWait(self.driver, self.timeout).until(AnyEC(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, '.search-results-container')),
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, '.profile-unavailable'))
            ))
        except TimeoutException as e:
            raise Exception(
                """Took too long to load profile.  Common problems/solutions:
                1. Invalid LI_AT value: ensure that yours is correct (they
                   update frequently)
                2. Slow Internet: increase the timeout parameter in the Scraper constructor""")
        return self.scrape_all_pages()

    def next_page(self):
        next_btn = self.driver.find_element_by_css_selector('[aria-label="Next"]')
        print(next_btn)
        next_btn.click()
        self.wait(EC.text_to_be_present_in_element(
                (By.CSS_SELECTOR, '.search-results-container'), str(self.page_num + 1)
        ))
        self.page_num += 1

    def scrape_all_pages(self):
        self.page_num = 1
        all_results = []
        more_pages = True
        while more_pages:
            more_pages, page_results = self.scrape_page()
            all_results += page_results
            if more_pages:
                self.next_page()
        return all_results

    def scrape_page(self):
        print("\tSCRAPING PAGE: ", self.page_num)
        self.scroll_to_bottom()
        try:
            next_btn = self.driver.find_element_by_css_selector('[aria-label="Next"]')
            if not next_btn.is_enabled(): next_btn = None
        except NoSuchElementException:
            next_btn = None
        connections = self.driver.find_elements_by_css_selector(
            '.entity-result')
        results = []
        for conn in connections:
            result = {}
            result['name'] = conn.find_element_by_css_selector(
                '.entity-result__title-text').text.partition('\n')[0]
            # Below added by Rishik to address emojis & accented names
            if result['name'] == 'LinkedIn Member':
                continue
            result['name'] = demoji.replace(result['name'], "")
            result['name'] = unidecode.unidecode(result['name'])
            link = conn.find_element_by_css_selector(
                '.app-aware-link').get_attribute('href')
            #user_id = re.search(r'/in/(.*?)/', link).group(1)
            result['id'] = link
            result['distance'] = conn.find_element_by_css_selector(
                '.entity-result__badge').text[2:]
            results.append(result)
            print(result)
        return bool(next_btn), results

    def configure_connection_type(self):
        dropdown_btn = self.wait_for_el(
            '.search-s-facet--facetNetwork form button')
        if not self.first_only:
            return
        new_url = re.sub(r'&facetNetwork=(.*?)&',
                         r'&facetNetwork=%5B"F"%5D&', self.driver.current_url)
        self.driver.get(new_url)
        self.wait(EC.text_to_be_present_in_element(
            (By.CSS_SELECTOR, '.search-s-facet--facetNetwork'), '1st'
        ))
