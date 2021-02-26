import requests
import os

from bs4 import BeautifulSoup
from selenium import webdriver


os.chdir("C:/Users/james/Desktop/Projects/ATCC_scraping")

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

for result in results: 
    strain_link = result.a['href']
    link = "https://www.atcc.org" + strain_link
    driver.get(link)
    c = driver.page_source
    strain_page = BeautifulSoup(c, 'lxml')
    strain = strain_page.find('h1', class_="product_name").text.replace(' ', '')
    print(strain)

strain_info = soup.find_all('li', class_='coveo-product-details__item')
strain_info


driver.close()