import requests
import os
import inspect
import re
import time 

from bs4 import BeautifulSoup
from selenium import webdriver

#change directory
#os.chdir("C:/Users/james/Desktop/Projects/ATCC_scraping")

#for interactive webpages, use selenium
#html_text = requests.get('https://www.atcc.org/search?title=ATCC%20Bacteria%20Alphanumeric%20(Genus%20/%20Species)#sort=%40searchlistingcardtitle%20ascending&f:contentTypeFacetATCC=[Products]&f:productcategoryFacet=[Bacteria%20%26%20Phages]')
#print(html_text)
#response 200 means that the call was successful

#add .text at the end
#html_text = requests.get('https://www.atcc.org/search?title=ATCC%20Bacteria%20Alphanumeric%20(Genus%20/%20Species)#sort=%40searchlistingcardtitle%20ascending&f:contentTypeFacetATCC=[Products]&f:productcategoryFacet=[Bacteria%20%26%20Phages]').text
#soup = BeautifulSoup(html_text, 'lxml')

driver_path = r"C:/chromedriver/chromedriver.exe"
url = "https://www.atcc.org/search?title=ATCC%20Bacteria%20Alphanumeric%20(Genus%20/%20Species)#sort=%40searchlistingcardtitle%20ascending&f:contentTypeFacetATCC=[Products]&f:productcategoryFacet=[Bacteria%20%26%20Phages]"
driver = webdriver.Chrome(executable_path=driver_path)
driver.get(url)

page_source = driver.page_source
soup = BeautifulSoup(page_source, 'lxml')

#html = soup.prettify("utf-8")
#with open("output1.html", "wt") as file:
#    file.write(str(html))

results = soup.find_all("div", class_="coveo-list-layout CoveoResult")
print(results)


def find_jobs():
    for result in results: 
        strain_link = result.a['href']
        link = "https://www.atcc.org" + strain_link
        driver.get(link)
        c = driver.page_source
        strain_page = BeautifulSoup(c, 'lxml')
        strain = strain_page.find('h1', class_="product_name").text.strip()
        for_profit = strain_page.find('span', class_ = 'forprofit').text.replace(' ', '').strip()
        non_profit = strain_page.find('span', class_ = 'border').text.replace(' ', '').replace('Non-Profit:', '').strip()
        table = strain_page.find('table', class_="fulllist") #find the information table
        for row in table.find_all('tr'):
            for cell in row.find_all('th'):
                cell_text = cell.text.strip()
                if cell_text == 'Biosafety Level':
                    bsl_info = cell.parent.text.replace(' ', '')
                    bsl = int(re.search('\d+', bsl_info).group()) #search the 1st integer in the string and save
                if cell_text == 'Product Format':
                    pf = cell.parent.text
                    pf = re.sub('Product Format', '', pf) #delete prefix
                    pf = pf.strip() #delete whitespace
                    print(pf)
        print(strain)
        print(for_profit)
        print(non_profit)
        print(bsl)
        print(pf)
        

if __name__ ==  '__main__':
    while True:
        find_jobs()
        time_wait = 15
        time.sleep(time_wait)
        

driver.close()