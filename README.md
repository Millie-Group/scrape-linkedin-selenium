# scrape_linkedin

## Introduction

`scrape_linkedin` is a python package to scrape all details from public LinkedIn
profiles, turning the data into structured json. You can scrape Companies
and user profiles with this package.

**Warning**: LinkedIn has strong anti-scraping policies, they may blacklist ips making
unauthenticated or unusual requests

## Table of Contents

<!--ts-->

- [scrape_linkedin](#scrapelinkedin)
  - [Introduction](#introduction)
  - [Table of Contents](#table-of-contents)
  - [Installation](#installation)
  - [Running](#running)
  - [Getting & Setting LI_AT](#getting--setting-liat)
    - [Getting LI_AT](#getting-liat)
  - [Usage](#usage)
    - [Python Package](#python-package)
      - [Profiles](#profiles)

<!-- Added by: austinoboyle, at: 2018-05-06T20:13-04:00 -->

<!--te-->

## Installation

`git clone https://github.com/Millie-Group/scrape-linkedin-selenium.git`

## Running

Create a spreadsheet (of `.xlsx`, `.xls`, or `.csv` format) in `spreadsheets/`.
Navigate to `scrape_linkedin/main.py` and run, entering in the necessary information
when prompted.

## Getting & Setting LI_AT

Because of Linkedin's anti-scraping measures, you must make your selenium
browser look like an actual user. To do this, you need to add the li_at cookie
to the selenium session.

### Getting LI_AT

1.  Navigate to www.linkedin.com and log in
2.  Open browser developer tools (Ctrl-Shift-I or right click -> inspect
    element)
3.  Select the appropriate tab for your browser (**Application** on Chrome,
    **Storage** on Firefox)
4.  Click the **Cookies** dropdown on the left-hand menu, and select the
    `www.linkedin.com` option
5.  Find and copy the li_at **value**
6.  This should be pasted into the console when you are prompted for a cookie

## Usage

### Python Package

#### Profiles

Use `ProfileScraper` component to scrape profiles.

```python
from scrape_linkedin import ProfileScraper

with ProfileScraper() as scraper:
    profile = scraper.scrape(user='austinoboyle')
print(profile.to_dict())
```

`Profile` - the class that has properties to access all information pulled from
a profile. Also has a to_dict() method that returns all of the data as a dict

    with open('profile.html', 'r') as profile_file:
        profile = Profile(profile_file.read())

    print (profile.skills)
    # [{...} ,{...}, ...]
    print (profile.experiences)
    # {jobs: [...], volunteering: [...],...}
    print (profile.to_dict())
    # {personal_info: {...}, experiences: {...}, ...}

**Structure of the fields scraped**

-   personal_info
    -   name
    -   company
    -   school
    -   headline
    -   followers
    -   summary
    -   websites
    -   email
    -   phone
    -   connected
    -   current_company_link
    -   image
-   skills
-   experiences
    -   volunteering
    -   jobs
    -   education
-   interests
-   accomplishments
    -   publications
    -   cerfifications
    -   patents
    -   courses
    -   projects
    -   honors
    -   test scores
    -   languages
    -   organizations
