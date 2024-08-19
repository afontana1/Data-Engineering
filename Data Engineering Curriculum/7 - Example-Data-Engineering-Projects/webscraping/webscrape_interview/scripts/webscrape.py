'''
Functionality used to extract the metadata from the web page
click_through_extract_meta(URL) being the main function

- Load the website url
- identify the location of the "next" tab
- default view will be set to 100
- identify the table and look through each row
- process each row, extracting relevant metadata (filename,sector,date,target url)
- write that record metadata to file for later consumption
'''

from selenium import webdriver
import json
import os

URL = "https://finsight.com/product/us/abs/ee?products=ABS&regions=USOA"
path = r'C:/Users/Aj/Desktop/chromedriver_win32/chromedriver.exe'

def find_number_of_entries(table_footer):
    '''Return int representation of table length'''
    elements = [j.lower() for j in table_footer.text.split()]
    return int(elements[elements.index("show")-1])

def get_table_rows(driver):
    '''get table rows'''
    table = driver.find_element_by_tag_name("table")
    table_body = table.find_element_by_tag_name("tbody")
    rows = table_body.find_elements_by_tag_name("tr")
    return rows

def process_row(row):
    '''Return metadata from row'''
    cells = row.find_elements_by_tag_name("td")
    sector,name,links,filingdate = cells[0],cells[1],cells[-1],cells[-2]
    sector_name = sector.find_element_by_tag_name("div").text
    file_name = name.find_elements_by_tag_name("span")[-1].text
    
    hrefs = []
    for href in links.find_elements_by_tag_name("a"):
        link = href.get_attribute("href")
        hrefs.append(link)
        
    return {
        "sector":sector_name,
        "name":file_name,
        "file_date":filingdate.text,
        "urls":hrefs
    }

def click_through_extract_meta(url):
    '''Click through urls and extract the metadata.'''
    driver = webdriver.Chrome(executable_path = path)
    driver.get(url)
    time.sleep(5)
    table = driver.find_element_by_tag_name("table")
    table_body = table.find_element_by_tag_name("tbody")
    rows = table_body.find_elements_by_tag_name("tr")
    
    parent_div = table.find_element_by_xpath('..')
    next_sibling = driver.execute_script("""return arguments[0].nextElementSibling""", parent_div)
    num_of_entries = find_number_of_entries(next_sibling) #get number of entries in footnote for iteration estimation

    driver.find_elements_by_class_name("Select-value-label")[0].click()
    driver.find_elements_by_class_name("Select-menu-outer")[0].click()
    i = 0
    while i < ((num_of_entries//100)+1):
        output = []
        table_rows = get_table_rows(driver)
        for row in table_rows:
            processed = process_row(row)
            output.append(processed)
        
        #write metadata to out file for ingestion into a document store database
        with open("data/table_{}.json".format(i),'w', encoding='utf-8') as outfile:
            json.dump(output,outfile)
            
        driver.find_elements_by_xpath('//a[@tabindex="0"]')[-1].click()
        time.sleep(3)
        i+=1

if __name__ == "__main__":
	#click_through_extract_meta(URL)