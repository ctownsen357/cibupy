from bs4 import BeautifulSoup
from datetime import date, timedelta, datetime
import requests

def get_violations(smonth, sday, syear, emonth, eday, eyear):
    """
    Takes integers of start: month, day, year AND end: month, day, year
    and returns a list of violations for the period.
    """
    more_results = True
    page_start = 1 #The API starts at one and returns 4 items per page.
    return_violations = []
    loop_counter = 0

    while more_results == True and loop_counter < 10:
        loop_counter += 1
        #using the params as posted data was not working
        url = "http://wake-nc.healthinspections.us/reports.cfm?start={start}&f=search&strSearch1=&relevance1=fName&strSearch2=&relevance2=fName&strSearch3=&relevance3=fName&lscore=&hscore=&ftype=Any&fzipcode=Any&rcritical=Any&sMonth={smonth}&sDay={sday}&sYear={syear}&eMonth={emonth}&eDay={eday}&eYear={eyear}&func=Search".format(start=page_start,smonth=smonth,sday=sday,syear=syear,emonth=emonth,eday=eday,eyear=eyear)
        response = requests.get(url)
        number_of_violations = -1

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            violations = soup.find_all('table', attrs={"style": "border:1px solid;border-color:3C5EAA"})
            if number_of_violations == -1:
                search_tags = soup.find_all("b", attrs={"style": "color:red"})
                for tag in search_tags:
                    if "out of" in tag.text:
                        number_of_violations = int(tag.text.split(" ")[0])

            if len(violations) == 0 or number_of_violations == 0:
                more_results = False
            else:
                page_start += 4
                for viol in violations:
                    anchor_tag = viol.find('a', class_='body')
                    if anchor_tag != None:
                        cells = viol.findChildren('td')
                        for cell in cells:
                            if "Location:" in cell.text:
                                start = cell.text.index('Location:')
                                end = cell.text.index('\nFacility Type:')
                                location = cell.text[start:end]
                                break
                        return_violations.append({'name-anchor-tag': anchor_tag, 'location': location})
                if len(return_violations) == number_of_violations:
                    more_results = False
    return return_violations


if __name__ == '__main__':
    # get a list of violations from yesterday and post to Twitter
    start_date = date.today() - timedelta(days=1)
    end_date = date.today()
    violations = get_violations(smonth=start_date.month,sday=start_date.day,syear=start_date.year,
                                          emonth=end_date.month,eday=end_date.day,eyear=end_date.year)

    print(violations) #post next