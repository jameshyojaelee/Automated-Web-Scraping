import requests
import os
import inspect
import re
import time 
import csv

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

#change directory
os.chdir("C:/Users/james/Desktop/Projects/ATCC_web_scraping")

PATH = r"C:/chromedriver/chromedriver.exe"
url = "https://www.atcc.org/search?title=ATCC%20Bacteria%20Alphanumeric%20(Genus%20/%20Species)#sort=relevancy&f:contentTypeFacetATCC=[Products]&f:productcategoryFacet=[Bacteria%20%26%20Phages]"
driver = webdriver.Chrome(executable_path=PATH)
driver.get(url)

def find_jobs():
    with open('result.csv', 'w', newline='', encoding='utf8') as file:
        writer=csv.writer(file)
        while True:
            page_source = driver.page_source
            soup = BeautifulSoup(page_source, 'lxml')
            results = soup.find_all("div", class_="coveo-list-layout CoveoResult")
            for result in results: 
                strain_link = result.a['href']
                link = "https://www.atcc.org" + strain_link
                driver.get(link)
                c = driver.page_source
                strain_page = BeautifulSoup(c, 'lxml')
                strain = strain_page.find('h1', class_="product_name")
                if strain is not None:
                    strain = strain.text.replace(u"\u2122", '').replace(u"\u00AE", '').strip() # remove trademarks and registered marks
                else:
                    strain = 'unavailable'
                for_profit = strain_page.find('span', class_ = 'forprofit')
                if for_profit is not None:
                    for_profit = for_profit.text.replace(' ', '').strip() 
                else:
                    for_profit = 'unavailable'
                non_profit = strain_page.find('span', class_ = 'border')
                if non_profit is not None:
                    non_profit = non_profit.text.replace(' ', '').replace('Non-Profit:', '').strip()
                else:
                    non_profit = 'unavailable'
                table = strain_page.find('table', class_="fulllist") #find the information table
                for row in table.find_all('tr'):
                    for cell in row.find_all('th'):
                        cell_text = cell.text.strip()
                        if cell_text == 'Biosafety Level':
                            bsl_info = cell.parent
                            if bsl_info is not None:
                                bsl_info = bsl_info.text.replace(' ', '')
                                bsl = str(re.search('\d+', bsl_info).group()) #search the 1st integer in the string and save
                            else:
                                bsl = 'unavailable'
                        if cell_text == 'Product Format':
                            pf = cell.parent
                            if pf is not None:
                                pf = pf.text
                                pf = re.sub('Product Format', '', pf) #delete prefix
                                pf = pf.replace(u"\u2122", '').replace(u"\u00AE", '').strip() #remove useless signs, and delete whitespace
                            else:
                                pf = 'unavailable'                            
                print(strain)
                print(for_profit)
                print(non_profit)
                print(bsl)
                print(pf)
                product = ','.join([strain, for_profit, non_profit, bsl, pf]) #create comma-separated list of info
                writer.writerow([strain, for_profit, non_profit, bsl, pf])
            #go all the way back to the main page (10 pages)
            driver.execute_script("window.history.go(-10)")
            time.sleep(5)
            try:
                driver.find_element_by_css_selector('a[title="Next"]').click() #move to the next page
            except:
                print("Web-scraping finished")
                break


if __name__ ==  '__main__':
    find_jobs()
    driver.close()
#    while True:
#        find_jobs()
#        time_wait = 15
#        time.sleep(time_wait)

