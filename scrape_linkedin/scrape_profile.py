from ProfileScraper import ProfileScraper
from selenium.webdriver import Chrome
from utils import HEADLESS_OPTIONS


def extract_name(data):
    """
    Extracts the full name, first name, and last name from a LinkedIn user's profile

    Parameters
    ----------
    data: the dictionary representation of a LinkedIn user's profile

    Returns
    -------
    The user's full name, first name, and last name
    """

    full_name = data['personal_info']['name']
    if ' ' in full_name:
        first_name = full_name[:full_name.index(' ')]
        last_name = full_name[full_name.rindex(' ') + 1:]
    else:
        first_name = ''
        last_name = ''

    return full_name, first_name, last_name


def extract_undergrad(school, undergrad):
    """
    Extracts information about a LinkedIn user's undergraduate school

    Parameters
    ----------
    school: the undergraduate school
    undergrad: a list of other undergraduate schools

    Returns
    -------
    The updated list of undergraduate schools and the undergraduate year of graduation
    """

    undergrad.append(school['name'])
    date_range = school['date_range']

    if date_range is None:
        undergrad_yr = 'N/A'
    elif 'Present' not in date_range:
        undergrad_yr = int(date_range[-4:])
    elif date_range[0:4].isnumeric():
        undergrad_yr = int(date_range[0:4]) + 4
    else:
        undergrad_yr = int(date_range[4:8])

    return undergrad, undergrad_yr


def check_int(school, international):
    """
    Checks if a school is an international school based on a school list and other criteria

    Parameters
    ----------
    school: current school being checked
    international: AP/IB school list

    Returns
    -------
    Y or N
    """

    # list of criteria that could qualify a school as an international school even if it is not on the school lists
    int_criteria = ["International Baccalaureate", "IBDP", "IB", "IB Score", "A Level",
                    "A-Level", "French Baccalaureate", "A Levels", "A*"]

    school_name = school['name']

    degree_name = school['degree']
    if degree_name is None: degree_name = ''

    field_of_study = school['field_of_study']
    if field_of_study is None: field_of_study = ''

    grades = school['grades']
    if grades is None: grades = ''

    if any(element.lower() == school_name.lower() for element in international["AP"]):
        int_hs = 'Y (AP)'
    elif any(element.lower() == school_name.lower() for element in international["IB"]):
        int_hs = 'Y (IB)'
    elif any(element.lower() in school_name.lower() for element in int_criteria) or \
            any(element.lower() in degree_name.lower() for element in int_criteria) or \
            any(element.lower() in field_of_study.lower() for element in int_criteria) or \
            any(element.lower() in grades.lower() for element in int_criteria):
        int_hs = 'Y'
    else:
        int_hs = 'N'

    return int_hs


def extract_work(data):
    """
    Extracts information about each of the LinkedIn user's past work experiences

    Parameters
    ----------
    data: the dictionary representation of a LinkedIn user's profile

    Returns
    -------
    The year of the user's first work experience and all past working locations
    """

    first_work = 2021
    locs = []

    for experience in data['experiences']['jobs']:
        date_range = experience['date_range']
        location = experience['location']

        if location not in locs:
            locs.append(location)

        if date_range is None:
            date = 'N/A'
        elif date_range[4:8].isnumeric():
            date = int(date_range[4:8])
        elif date_range[0:4].isnumeric():
            date = int(date_range[0:4])
        else:
            date = 'N/A'

        if date is not 'N/A':
            if date < first_work:
                first_work = date

    return first_work, locs


def scrape(url, cookie, headless=True):
    """
    Scrapes a profile using the account for which a cookie is given

    Parameters
    ----------
    url: URL of the LinkedIn profile to be scraped
    cookie: 'li_at' cookie for the user account scraping the profile
    headless: whether or not a headless driver should be used (defaults to True)

    Returns
    -------
    Dictionary representation of a profile's JSON
    """

    # sets up a Selenium instance using Chrome
    driver_options = HEADLESS_OPTIONS
    if headless == False:
        driver_options = {}
    driver_type = Chrome

    # initializes a scraper object based on the cookie to scrape the URL's profile
    scraper = ProfileScraper(driver=driver_type, cookie=cookie, driver_options = driver_options)
    profile = scraper.scrape(url=url)

    # converts the profile output to a dictionary (rather than a JSON)
    output = profile.to_dict()

    # print(output)     # uncomment this line to visualize the dictionary output of a profile
    return output


def scrape_profile(url, cookie, international):
    """
    Extracts the specific information needed from the scraped output of a profile

    Parameters
    ----------
    url: URL of the LinkedIn profile to be scraped
    cookie: 'li_at' cookie for the user account scraping the profile
    international: international school (AP/IB) lists --> this is passed as an argument to avoid reading
        the lists in multiple times

    Returns
    -------
    Information needed for the LinkedIn member (in order: full name, first name, last name, current location,
        undergrad school(s), other school(s), years of experience since undergrad graduation, headline,
        international high school?, email, undergrad year of graduation (if found)
    """

    data = scrape(url, cookie)                              # scrapes the profile located at URL

    fullName, firstName, lastName = extract_name(data)      # finds the name of the LinkedIn user

    headline = data['personal_info']['headline']            # finds the headline of the LinkedIn user

    # TODO: add support for past locations
    location = data['personal_info']['location']            # finds the current location of the LinkedIn user

    email = data['personal_info']['email']                  # finds the email of the LinkedIn user (if included)

    all_schools = []
    undergrad = []
    undergrad_yr = 0
    int_hs = 'N'

    for school in data['experiences']['education']:         # iterate over each of the user's schools
        degree_name = school['degree']                      # find degree name
        if degree_name is None: degree_name = ''

        # undergrad school
        if degree_name is not '' and (degree_name[0] is 'B' or 'Bachelor' in degree_name):
            undergrad, undergrad_yr = extract_undergrad(school, undergrad)

        # other schools
        else:
            all_schools.append(school['name'])

        if int_hs == 'N':                                   # check for international high school
            int_hs = check_int(school, international)

    if undergrad_yr == 'N/A':                               # set undergrad year to 0 if it has not been found
        undergrad_yr = 0

    first_work, locs = extract_work(data)                   # find work information

    # set years of experience (either based on undergrad year or first work experience)
    if undergrad_yr == 0 and first_work < 2021:
        yrs_experience = max(0, 2020 - int(first_work))
    else:
        yrs_experience = max(0, 2020 - int(undergrad_yr))
    if yrs_experience == 2020:
        yrs_experience = 0

    undergrad = ', '.join(undergrad)
    all_schools = ', '.join(all_schools)
    locs = ', '.join(locs)

    return fullName, firstName, lastName, location, locs, undergrad, all_schools, \
           yrs_experience, headline, int_hs, email, undergrad_yr