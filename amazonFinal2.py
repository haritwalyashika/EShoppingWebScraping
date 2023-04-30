import csv 
from bs4 import BeautifulSoup
from selenium import webdriver
from msedge.selenium_tools import Edge, EdgeOptions

def get_url(search_term):
     template='https://www.amazon.com/s?k={}&crid=3T38SMJFW8AWD&sprefix=speakers%2Caps%2C290&ref=nb_sb_ss_ts-doa-p_1_8'
     search_term=search_term.replace(' ','+')

     URL=template.format(search_term)
     return template.format(search_term)

     URL+='&page{}'
     return URL

def extract_record(item):
    #title(description) and url 
    atag=item.h2.a
    description=atag.text.strip()
    url="https://www.amazon.com"+atag.get('href')

    #price
    try:
        price_parent=item.find('span',{'class':'a-price'})
        price=price_parent.find('span',{'class':'a-offscreen'}).text

    except AttributeError:
         return 
         
    #rank and rating 
    try:
        rating=item.i.text
        review_count=item.find('span',{'class':'a-size-base s-underline-text'}).text
    except  AttributeError:
         rating=''
         review_count=''

    
    result=(description,price,rating,review_count,url)
    return result

def main(search_item):
     #startup our webdriver
     options=EdgeOptions()
     options.use_chromium=True
     driver=webdriver.Firefox(executable_path='/home/yashika/bin/geckodriver')
     records=[]
     url=get_url(search_item)

     for page in range(1,21):
          driver.get(url.format(page))
          soup =BeautifulSoup(driver.page_source,'html5lib')
          results=soup.find_all('div',{'data-component-type':'s-search-result'})

          for item in results:
                record=extract_record(item)
                if record:
                      records.append(record)
     driver.close()                 

     with open('results4.csv','w',newline='',encoding='utf-8') as f:
          writer=csv.writer(f)
          writer.writerow(['Description','Price','Rating','ReviewCount','URL'])
          writer.writerows(records)

main('speakers bluetooth wireless')          