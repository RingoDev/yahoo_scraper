from selenium import webdriver
import time
from bs4 import BeautifulSoup
import pandas as pd

# BaseURL of Yahoo Finance website.
URL = "https://finance.yahoo.com/"
# List of companies.

Companies = [ "DIS" ] #"GM", "JNJ",

# Start the Driver
driver = webdriver.Chrome()
# Hit the url of Yahoo Finance and wait for 2 seconds.
driver.get(URL)
time.sleep(2)

# Click on 'I agree' button and wait for a second.
driver.find_element_by_xpath("//button[@value='agree']").click()
time.sleep(1)

for name in Companies:

    # Enter name of company in searchbox, and wait for 2 seconds.
    driver.find_element_by_xpath("//input[@placeholder = 'Search for news, symbols or companies']").send_keys(
        name)
    time.sleep(2)
    # Click on Search icon and wait for 2 seconds.
    driver.find_element_by_xpath("//button[@id= 'header-desktop-search-button']").click()
    time.sleep(2)

    # Driver clicks on Historical Data tab and sleeps for 2 seconds.
    driver.find_element_by_xpath("//span[text() = 'Historical Data']").click()
    time.sleep(2)

    # open Dropdown
    driver.find_element_by_xpath("//span[text() = 'Time Period']/../../div[1]/div[1]").click()

    time.sleep(2)

    #select Max option
    driver.find_element_by_xpath("//div[@data-test = 'date-picker-menu']/ul[2]/li[4]/button").click()
    time.sleep(2)


    # press Apply button
    driver.find_element_by_xpath("//span[text() = 'Apply']/..").click()
    time.sleep(2)

    date_span = driver.find_element_by_xpath("//span[text() = 'Time Period']/../../div[1]/div[1]").text
    scrolls = (int(date_span.split("-")[1].split(",")[1].strip()) - int(date_span.split("-")[0].split(",")[1].strip()))*3

    print(date_span)
    print("scrolling down " + str(scrolls) + " times")

    #Todo let scrolling depend on the date of the TimePeriod span
    for i in range(0, scrolls):
        driver.execute_script("window.scrollBy(0,10000)")
        print("scroll: "+ str(i))
        time.sleep(0.2)

    # Fetch the webpage and store in a variable.
    webpage = driver.page_source
    # print the fetched webpage.
    print(webpage)

    # Web page fetched from driver is parsed using Beautiful Soup.
    HTMLPage = BeautifulSoup(driver.page_source, 'html.parser')

    # Table is searched using class and stored in another variable.
    Table = HTMLPage.find('table', class_='W(100%) M(0)')

    # List of all the rows is store in a variable 'Rows'.
    Rows = Table.find_all('tr', class_='BdT Bdc($seperatorColor) Ta(end) Fz(s) Whs(nw)')

    # Empty list is created to store the data
    extracted_data = []
    # Loop to go through each row of table
    for j in range(0, len(Rows)):
        try:
            # Empty dictionary to store data present in each row
            RowDict = {}
            # Extracted all the columns of a row and stored in a variable
            Values = Rows[j].find_all('td')

            # Values (Open, High, Close etc.) are extracted and stored in dictionary
            if len(Values) == 7:
                RowDict["Date"] = Values[0].find('span').text.replace(',', '')
                RowDict["Open"] = Values[1].find('span').text.replace(',', '')
                RowDict["High"] = Values[2].find('span').text.replace(',', '')
                RowDict["Low"] = Values[3].find('span').text.replace(',', '')
                RowDict["Close"] = Values[4].find('span').text.replace(',', '')
                RowDict["Adj Close"] = Values[5].find('span').text.replace(',', '')
                RowDict["Volume"] = Values[6].find('span').text.replace(',', '')
                # Uncomment below print statement if required
                print(RowDict)
                # Dictionary is appended in list
                extracted_data.append(RowDict)
        except:
            # To check the exception caused for which company
            print("Row Number: " + str(j))
        finally:
            # To move to the next row
            j = j + 1

    # Converted list of dictionaries to a Dataframe.
    df = pd.DataFrame(extracted_data)
    print(df)
    df.to_csv(name + '.csv',index=False)
