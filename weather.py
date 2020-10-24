from bs4 import BeautifulSoup as bs
from splinter import Browser
import requests
import time
from jobs import cities_list


executable_path = {'executable_path': 'chromedriver.exe'}
browser = Browser('chrome', **executable_path, headless=True)

url="https://weatherspark.com"

weather_list = []
browser.visit(url)

for city in cities_list:
    
    browser.find_by_tag('input').fill(f"{city}\n")
    time.sleep(1)

    response = requests.get(browser.url)
    
    soup = bs(response.text,"html.parser")
    blurb = soup.find("div",class_="Section-body").find('p').text
    blurb = blurb.replace("\n","")
    blurb = blurb.replace("Â","")
    blurb_dict = {"city":f"{city}",
                 "weather":f"{blurb}"}
    weather_list.append(blurb_dict)
    print(city)

