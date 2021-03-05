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
                strain= for_profit= non_profit= bsl= pf= genome_seq = cc_medium = growth_conditions = 'unavailable' #set all variables to 'unavailable' first. 
                strain_link = result.a['href']
                link = "https://www.atcc.org" + strain_link
                driver.get(link)
                c = driver.page_source
                strain_page = BeautifulSoup(c, 'lxml')
                # get strain info
                strain = strain_page.find('h1', class_="product_name")
                if strain is not None:
                    strain = strain.text.replace(u"\u2122", '').replace(u"\u00AE", '').strip() # remove trademarks and registered marks
                # get for_profit price
                for_profit = strain_page.find('span', class_ = 'forprofit')
                if for_profit is not None:
                    for_profit = for_profit.text.replace(' ', '').strip() 
                # get non-profit price
                non_profit = strain_page.find('span', class_ = 'border')
                if non_profit is not None:
                    non_profit = non_profit.text.replace(' ', '').replace('Non-Profit:', '').strip()
                # get the info table that includes bsl, product format, etc
                table = strain_page.find('table', class_="fulllist") #find the information table
                for row in table.find_all('tr'):
                    for cell in row.find_all('th'):
                        cell_text = cell.text.strip()
                        if cell_text == 'Biosafety Level':
                            bsl_info = cell.parent
                            if bsl_info is not None:
                                bsl_info = bsl_info.text.replace(' ', '')
                                bsl = str(re.search('\d+', bsl_info).group()) #search the 1st integer in the string and save
                        if cell_text == 'Product Format':
                            pf = cell.parent
                            if pf is not None:
                                pf = pf.text
                                pf = re.sub('Product Format', '', pf) #delete prefix
                                pf = pf.replace(u"\u2122", '').replace(u"\u00AE", '').strip() #remove useless signs, and delete whitespace 
                        if cell_text == 'Verified By':
                            genome_seq = 'seqeunce available'
                culture_method_table = strain_page.find('div', {'id': 'layoutcontent_2_middlecontent_0_productdetailcontent_0_maincontent_2_rptTabContent_pnlTabContent_2'})
                for row in culture_method_table.find_all('tr'):
                    for cell in row.find_all('th'):
                        cell_text = cell.text.strip()
                        if cell_text == 'Medium':
                            cc_medium = cell.parent
                            if cc_medium is not None:
                                cc_medium = cc_medium.text
                                cc_medium = re.sub('Medium', '', cc_medium) #remove prefix
                                cc_medium = cc_medium.replace(u"\u2122", '').replace(u"\u00AE", '').strip() #remove useless signs, and delete whitespace 
                        if cell_text == 'Growth Conditions':
                            growth_conditions = cell.parent
                            if growth_conditions is not None:
                                growth_conditions = growth_conditions.text
                                growth_conditions = re.sub('Growth Conditions', '', growth_conditions) #remove prefix
                                growth_conditions = growth_conditions.replace('°C', 'Celsius ').strip() #remove useless signs, and delete whitespace 

                print(strain)
                print(for_profit, non_profit)
                print(bsl)
                print(pf)
                print(genome_seq)
                print(cc_medium)
                print(growth_conditions)

            #create comma-separated list of info 
            #product = ','.join([strain, genome_seq, for_profit, non_profit, bsl, pf, cc_medium, growth_conditions])
            #write to csv file
            writer.writerow([strain, genome_seq, for_profit, non_profit, bsl, pf, cc_medium, growth_conditions])
            driver.execute_script("window.history.go(-10)") #go all the way back to the main page (10 pages)
            time.sleep(5) #pause 5sec
            try:
                #driver.find_element_by_css_selector('a[title="Next"]').click() #move to the next page
                break
            except:
                print("Web-scraping finished")
                break
    driver.close()

if __name__ ==  '__main__':
    find_jobs()
#    while True:
#        find_jobs()
#        time_wait = 10 * 60
#        time.sleep(time_wait)

