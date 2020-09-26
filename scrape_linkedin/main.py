from ProfileScraper import ProfileScraper
import os
from selenium.webdriver import Chrome
import pandas as pd

def scrape(url):
    driver_options = {}
    driver_type = Chrome

    scraper = ProfileScraper(driver=driver_type, cookie='cookie', driver_options = driver_options)
    profile = scraper.scrape(url=url)

    output = profile.to_dict()

    return output


def scrape_profile(url):
    international = ["International Baccalaureate", "IBDP", "IB", "IB Score", "A Level", "French Baccalaureate"]

    data = scrape(url)

    fullName = data['personal_info']['name']
    firstName = fullName[:fullName.index(' ')]
    lastName = fullName[fullName.rindex(' ')+1:]

    #print("Full Name: ", fullName)
    #print("First Name: ", firstName)
    #print("Last Name: ", lastName)

    headline = data['personal_info']['headline']

    #print("Headline: ", headline)

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
        if "High School" in schoolName or "High School" in degreeName or any(element in degreeName for element in international):
            filtered = list(filter(lambda a: a is not None, school.values()))
            if any(element in ' '.join(filtered) for element in international):
                int_hs = 'Y'

    if (undergrad_yr == 0 or undergrad_yr == 'N/A') and len(grad_yrs) > 0:
        undergrad_yr = int(min(grad_yrs))

    for experience in data['experiences']['jobs']:
        date_range = experience['date_range']
        date = 0

        if date_range is None:
            date = 'N/A'
        elif date_range[4:8].isnumeric():
            date = int(date_range[4:8])
        elif date_range[0:4].isnumeric():
            date = int(date_range[0:4])
        else:
            date = 'N/A'

        if date is not 'N/A' and date < undergrad_yr:
            undergrad_yr = date

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

    return fullName, firstName, lastName, location, undergrad, university, yrs_experience, headline, int_hs, email

def main():
    excel_file = "BusinessP1.xlsx"
    data = pd.read_excel(excel_file)
    df = pd.DataFrame(data)

    for index, row in df.iterrows():
        scraped_data = scrape_profile(row['LinkedIn URL'])
        df.loc[index, 'Full Name'] = scraped_data[0]
        df.loc[index, 'First Name'] = scraped_data[1]
        df.loc[index, 'Last Name'] = scraped_data[2]
        df.loc[index, 'Location'] = scraped_data[3]
        df.loc[index, 'Undergrad'] = scraped_data[4]
        df.loc[index, 'Other Schools'] = scraped_data[5]
        df.loc[index, 'Yrs Exp'] = scraped_data[6]
        df.loc[index, 'Headline'] = scraped_data[7]
        df.loc[index, 'Int HS?'] = scraped_data[8]
        df.loc[index, 'Email'] = scraped_data[9]

    df.to_excel('BusinessP1.xlsx')


if __name__ == "__main__":
    main()
