import csv 
from bs4 import BeautifulSoup
from selenium import webdriver
import tkinter as tk

def get_url(search_term):
    template='https://www.flipkart.com/search?q={}&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off'
    search_term=search_term.replace(' ','%20')
    URL=template.format(search_term)
    #return template.format(search_term)
    URL+='&page={}'
    return URL

def extract_record(item):
    #title(description) and url 
    #atag=item.h2.a
    atag=item.a
    #description=atag.text.strip()
    description=item.find("div",{'class':"_4rR01T"}).text
    print(description)
    print(atag.get('href'))
    url="https://www.flipkart.com"+atag.get('href')
    #price
    #try:
        #price_parent=item.find('span',{'class':'a-price'})
    price=item.find('div',{'class':'_30jeq3 _1_WHN1'}).text
    print(price)
        #class="_30jeq3 _1_WHN1"
        #price=price_parent.find('span',{'class':'a-offscreen'}).text
    #except AttributeError:
         #return 
    #rank and rating 
    #try:
        #rating=item.i.text
        #review_count=item.find('span',{'class':'a-size-base s-underline-text'}).text
    rating=item.find('div',{'class':'_3LWZlK'}).text
    review_count=item.find('span',{'class':'_2_R_DZ'}).text
    print(rating,review_count)
    #except  AttributeError:
        #rating=''
        #review_count=''
    result=(description,price,rating,review_count,url)
    return result

s=[]

def getInput():
    inp = entry.get()
    s.append(inp)
    root.destroy()

def main(search_item):
    #startup our webdriver
    driver = webdriver.Edge(r"msedgedriver.exe")
    records=[]
    
    url=get_url(search_item)

    for page in range(1,11):
        driver.get(url.format(page))
        print(url.format(page))
        soup =BeautifulSoup(driver.page_source,'html5lib')
        #results=soup.find_all('div',{'data-component-type':'s-search-result'})
        results=soup.find_all('div',{'class':'_13oc-S'})
        #class="_13oc-S"
        #class':'_1YokD2 _3Mn1Gg
        #class="_1YokD2 _3Mn1Gg"
        print(len(results))
        for item in results:
            record=extract_record(item)
            #if record:
            records.append(record)
    driver.close()                 
    with open('results4.csv','w',newline='',encoding='utf-8') as f:
        writer=csv.writer(f)
        writer.writerow(['Description','Price','Rating','ReviewCount','URL'])
        writer.writerows(records)
        
root = tk.Tk()
root.title("Price Comparison")
root.geometry("400x200")
root.configure(bg="#75AF6F")

# Load the background image
bg_image = tk.PhotoImage(file="w2.png")

# Create a canvas to hold the background image
canvas = tk.Canvas(root, width=400, height=200, bg="#75AF6F")
canvas.pack(fill="both", expand=True)
canvas.create_image(0, 0, image=bg_image, anchor="nw")

title_font = ("Helvetica", 24, "bold")
label_font = ("Helvetica", 12)
button_font = ("Helvetica", 14)

title_label = tk.Label(canvas, text="Price Comparison", font=title_font, bg="#75AF6F", fg="white")
title_label.pack(pady=(30,10))

entry_label = tk.Label(canvas, text="Enter product name:", font=label_font, bg="#75AF6F", fg="white")
entry_label.pack()

entry = tk.Entry(canvas, font=label_font)
entry.pack(pady=10)

printButton = tk.Button(canvas, text="Search", command=getInput, font=button_font, bg="#4CAF50", fg="white")
printButton.pack()

root.mainloop()   
main(s[0])