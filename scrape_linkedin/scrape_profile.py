from ProfileScraper import ProfileScraper
from selenium.webdriver import Chrome


# TODO: Look into using headless instead of Chrome
def scrape(url, cookie):
    driver_options = {}
    driver_type = Chrome

    scraper = ProfileScraper(driver=driver_type, cookie=cookie, driver_options = driver_options)
    profile = scraper.scrape(url=url)

    output = profile.to_dict()

    return output


# TODO: comment code and separate into methods
def scrape_profile(url, cookie):
    # TODO: remove once Ritvik sends school list
    international = ["International Baccalaureate", "IBDP", "IB", "IB Score", "A Level",
                     "A-Level", "French Baccalaureate", "AP", "Advanced Placement", "A Levels", "A*"]

    data = scrape(url, cookie)

    fullName = data['personal_info']['name']
    firstName = fullName[:fullName.index(' ')]
    lastName = fullName[fullName.rindex(' ')+1:]

    #print("Full Name: ", fullName)
    #print("First Name: ", firstName)
    #print("Last Name: ", lastName)

    headline = data['personal_info']['headline']

    #print("Headline: ", headline)

    # TODO: add support for past locations
    location = data['personal_info']['location']

    #print("Location: ", location)

    university = []
    undergrad = []
    grad_yrs = []
    undergrad_yr = 0
    yrs_experience = 0
    int_hs = 'N'

    keepSchool = ''

    for school in data['experiences']['education']:
        schoolName = school['name']
        degreeName = school['degree']

        if 'College' in schoolName or 'University' in schoolName:
            keepSchool = schoolName

        if degreeName is not None and (degreeName[0] is 'B' or 'Bachelor' in degreeName):
            undergrad.append(schoolName)
            date_range = school['date_range']

            if date_range is None:
                undergrad_yr = 'N/A'
            elif 'Present' not in date_range:
                undergrad_yr = int(date_range[-4:])
                grad_yrs.append(int(undergrad_yr))
            elif date_range[0:4].isnumeric():
                undergrad_yr = int(date_range[0:4]) + 4
                grad_yrs.append(int(undergrad_yr))
            else:
                undergrad_yr = int(date_range[4:8])
                grad_yrs.append(int(undergrad_yr))

        else:
            university.append(schoolName)

            date_range = school['date_range']
            yr = 0

            if date_range is None:
                yr = 'N/A'
            elif 'Present' not in date_range:
                yr = int(date_range[-4:])
                grad_yrs.append(yr)
            elif date_range[0:4].isnumeric():
                yr = int(date_range[0:4]) + 4
                grad_yrs.append(int(yr))
            else:
                yr = int(date_range[4:8])
                grad_yrs.append(int(yr))

        if degreeName is None:
            degreeName = ''
        if any(element.lower() in degreeName.lower() for element in international) or any(element.lower() in schoolName.lower() for element in international):
            filtered = list(filter(lambda a: a is not None, school.values()))
            if any(element in ' '.join(filtered) for element in international):
                int_hs = 'Y'

    if undergrad_yr == 'N/A':
        undergrad_yr = 0

    first_work = 2021

    for experience in data['experiences']['jobs']:
        date_range = experience['date_range']

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

    if undergrad_yr == 0 and first_work < 2021:
        yrs_experience = max(0, 2020 - int(first_work))
    else:
        yrs_experience = max(0, 2020 - int(undergrad_yr))
    if yrs_experience == 2020:
        yrs_experience = 0

    if len(undergrad) == 0:
        undergrad.append(keepSchool)

    undergrad = ', '.join(undergrad)
    #print("Undergrad: ", undergrad)

    university = ', '.join(university)
    #print("Other Schools: ", university)

    email = data['personal_info']['email']
    #print("Email: ", data['personal_info']['email'])

    #print("International HS? ", int_hs)

    return fullName, firstName, lastName, location, undergrad, university, yrs_experience, headline, int_hs, email, undergrad_yr