import pandas as pd
import sys
from cookies import cookies
from scrape_profile import scrape_profile


# school lists to store the most common ones
IVIES = ["Harvard University", "Yale University", "Princeton University", "Columbia University in the City of New York",
         "University of Pennsylvania", "Brown University", "Dartmouth College", "Cornell University"]
OXBRIDGE = ["University of Oxford", "University of Cambridge"]


def school_list(schools, country):
    if country == '':
        return schools['School Name'].tolist()
    else:
        country_schools = []
        for index, row in schools.iterrows():
            if schools.loc[index, 'US/UK'] is country:
                country_schools.append(schools.loc[index, 'School Name'])
        return country_schools


def main():
    # choose LinkedIn account
    name = input("Whose LinkedIn account should be used (Jenna, Guiseppe, or Bot)?\t")
    name = name.lower()

    if name in cookies:
        cookie = cookies[name]
    else:
        sys.exit("Didn't enter a valid LinkedIn account! Must choose Jenna, Giuseppe, or Bot.")

    # input name of spreadsheet (get profile links from this sheet and eventually return information to the same sheet)
    filename = input("Name of spreadsheet?\t")

    # choose undergrad options
    undergrads = []
    undergrad_enter = True
    restrict_undergrad = input("Restrictions on undergrad schools (Y/N)?\t")
    if restrict_undergrad == 'N': undergrad_enter = False
    while undergrad_enter == True:
        school = input("Input a school to include (1 for Ivies, 2 for Oxbridge, 3 for Ivies + Oxbridge, -1 to quit, or input your own):\t")
        if school == "-1":
            undergrad_enter = False
        elif school == "1":
            undergrads += IVIES
        elif school == "2":
            undergrads += OXBRIDGE
        elif school == "3":
            undergrads += IVIES + OXBRIDGE
        else:
            undergrads = undergrads.append(school)

    # choose US or UK and read schools
    toggle_country = int(input("If restricted undergrad schools are too limited, top US schools (1), top UK schools (2), either (3), or return all (4)?\t"))
    undergrads_by_country = []

    if toggle_country < 4:
        schools_file = "../spreadsheets/Schools.xlsx"
        schools = pd.read_excel(schools_file)
        school_df = pd.DataFrame(schools)

        undergrads_by_country = school_list(school_df, toggle_country)

    # specify years of experience
    exp_min = int(input("Preferred minimum years of experience after undergrad (-1 if no restriction)?\t"))
    exp_max = int(input("Preferred maximum years of experience after undergrad (100 if no restriction)?\t"))

    # minimum results
    min_results = int(input("At least how many results?\t"))

    # read links from spreadsheet
    excel_file = "../spreadsheets/" + filename + ".xlsx"
    data = pd.read_excel(excel_file)
    df = pd.DataFrame(data)

    # set up variables to check for additional filters
    exp_restrict_count = 0
    exp_12_count = 0

    undergrad_restrict_count = 0
    undergrad_country_count = 0

    # TODO: location

    # scrape profiles
    for index, row in df.iterrows():
        url = row['LinkedIn URL']

        if not pd.isnull(url) and pd.isnull(row['Full Name']):
            if '?' in url:
                url = url[:url.rindex('?')]
            elif url[-1] is not '/':
                url = url[:url.rindex('-')]
            scraped_data = scrape_profile(url, cookie)

            df.loc[index, 'LinkedIn URL'] = url
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
            df.loc[index, 'Grad Yr'] = scraped_data[10]

            # years of experience counts
            if scraped_data[6] <= exp_max and scraped_data[6] >= exp_min: exp_restrict_count += 1
            if scraped_data[6] <= 12: exp_12_count += 1

            # undergrad counts
            if scraped_data[4] in undergrads: undergrad_restrict_count += 1
            if undergrads_by_country is not [] and scraped_data[4] in undergrads_by_country: undergrad_country_count += 1

    # save to database -- commented out because no database yet
    # TODO: figure out how this would interact with PostgreSQL database (instead of Excel file)
    # reader = pd.read_excel(r'../spreadsheets/database.xlsx')
    # df.to_excel('../spreadsheets/database.xlsx', index=False, header=False, startrow=len(reader) + 1)

    # filter by years of experience
    print("exp restrict count", exp_restrict_count)
    print("exp 12 count", exp_12_count)
    if exp_restrict_count >= min_results:
        for index, row in df.iterrows():
            if df.loc[index, 'Yrs Exp'] > exp_max or df.loc[index, 'Yrs Exp'] < exp_min:
                df = df.drop(index)
    elif exp_12_count >= min_results:
        for index, row in df.iterrows():
            if df.loc[index, 'Yrs Exp'] > 12:
                df = df.drop(index)

    # filter by undergrad
    print("undergrad restrict count", undergrad_restrict_count)
    print("undergrad country count", undergrad_country_count)
    if undergrad_restrict_count >= min_results:
        for index, row in df.iterrows():
            if df.loc[index, 'Undergrad'] not in undergrads:
                df = df.drop(index)
    elif undergrads_by_country is not [] and undergrad_country_count >= min_results:
        for index, row in df.iterrows():
            if df.loc[index, 'Undergrad'] not in undergrads_by_country:
                df = df.drop(index)

    # save to initial spreadsheet
    df.to_excel('../spreadsheets/' + filename + '.xlsx', index=False)


if __name__ == "__main__":
    main()