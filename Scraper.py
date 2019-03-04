import os
from splinter import Browser
from bs4 import BeautifulSoup  as bs
import datetime as dt   
import pandas as pd
import time

# Store data to upsert into mongodb
marsdict = {}

def init_browser():
    # Path to chromedriver
    executable_path = {"executable_path": "C:/Users/Janie228/SCHOOL/Browser_Drivers/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)

# This function store all the required urls into a dictionary list by type
def get_urlist():
    url_List = []
    url_dict = {}
    url_dict["type"] = "news"
    url_dict["url"] = "https://mars.nasa.gov/news/"
    url_List.append(url_dict)
    url_dict = {}
    url_dict["type"] = "space"
    url_dict["url"] = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    url_List.append(url_dict)
    url_dict = {}
    url_dict["type"] = "weather"
    url_dict["url"] = "https://twitter.com/marswxreport?lang=en"
    url_List.append(url_dict)
    url_dict = {}
    url_dict["type"] = "facts"
    url_dict["url"] = "http://space-facts.com/mars/"
    url_List.append(url_dict)
    url_dict = {}
    url_dict["type"] = "hemispheres"
    url_dict["url"] = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    url_List.append(url_dict)
    return url_List

# This function scrape all the sites related to Mars info:
# news, space, weather, facts, and hemispheres
def scrape_mars():
    #Initialize values
    browser = init_browser()
    urlist = get_urlist()

    # Loop thru the scrape list to scrape each site and parse according to the if criteria
    for item in urlist:
        print(item["type"])
        print(item["url"])
        # If item is one of the three types blow, start off without scraping, else scrape
        if (item["type"] == "hemispheres") or (item["type"] == "space") or (item["type"] == "facts"):
            # If criteria met, visit site, click to result link, parse, store in dictionary
            if (item["type"] == "hemispheres"):
                # Call the function to do the scraping and parsing
                browser = parse_hemisphere(browser, item["url"])
                    
            elif item["type"] == "facts":
                # Read html table from site & zip into dictionary
                fact_table = pd.read_html(item["url"])[0]
                marsdict["marsFacts"] = dict(zip(fact_table[0] , fact_table[1]))

            elif item["type"] == "space":
                # Call the function to do the scraping and parsing
                browser = parse_featuredImg(browser, item["url"])

        else:
            soup = ''
            i = 0

             # Allow 3 try if exception occurs
            while (soup == '') and (i < 3):
                try:
                    # Visit site and scrape html
                    browser.visit(item["url"])

                    html = browser.html
                    soup = bs(html, "html.parser")

                    # Parse news and store in dictionary
                    if item["type"] == "news":              
                        marsdict["newsTitle"] = soup.find("div", class_ = "content_title").text.strip()
                        marsdict["newsDesc"] = soup.find("div", class_ = "rollover_description_inner").text.strip()

                    # Parse weather and store in dictionary
                    elif item["type"] == "weather":
                        time.sleep(2)
                        # Click Home to stop login popup from throwing error on process
                        browser.click_link_by_partial_text("Home")
                        weather = (soup.find("p", class_ = "TweetTextSize"))
                        marsdict["marsWeather"]  = weather.text.split(weather.a.text)[0]

                except:
                    print("Connection refused by the server..")
                    print("Let me sleep for 1 seconds")
                    print("ZZzzzz...")
                    print(marsdict)
                    time.sleep(15)
                    print("Was a nice sleep, now let me continue...")
                    i = i + 1
                    continue 

    print(marsdict) 
    browser.quit()

    return marsdict

# This function will scrape and parse the hemisphere site for images as in list
def parse_hemisphere(browser, url):
    # Store the hemisphere word links into a list
    hemisphere_List = ["Cerberus Hemisphere Enhanced", "Schiaparelli Hemisphere Enhanced", "Syrtis Major Hemisphere Enhanced", "Valles Marineris Hemisphere Enhanced"]
    sphereList = []

    # Loop thru the hemisphere list
    # With each loop, visit the site, click on the link, parse the image, and store in dictionary
    for link in hemisphere_List:
        soup = ''
        i = 0
        sphereDict = {}
        sphereDict["img_title"] = link.replace(" Enhanced", "")
        
        # Allow 3 try if exception occurs
        while (soup == '') and (i < 3):
            try:
                browser.visit(url)
                time.sleep(2)
                browser.click_link_by_partial_text(link)
                time.sleep(2)
                html = browser.html
                soup = bs(html, "html.parser")

                sphereDict["img_url"] = (soup.find("div", class_ = "downloads")).a["href"]
                sphereList.append(sphereDict)  
            except:
                print("Connection refused by the server..")
                print("Let me sleep for 1 seconds")
                print("ZZzzzz...")
                print(marsdict)
                time.sleep(15)
                print("Was a nice sleep, now let me continue...")
                i = i + 1
                continue

    # Pass data into main dictionary
    marsdict["marsHemisphere"] = sphereList

    # return browser
    return browser

# This function will scrape and parse  mars' featured image 
def parse_featuredImg(browser, url):
    soup = ''
    i = 0

    # Visit the site, click on the link, parse the data, and store to dictionary 
    # Allow 3 try if exception occurs   
    while (soup == '') and (i < 3):
        try:
            browser.visit(url)
            time.sleep(1)
            browser.click_link_by_partial_text("FULL IMAGE")
            time.sleep(2)
            browser.click_link_by_partial_text("more info")

            html = browser.html
            soup = bs(html, "html.parser")

            marsdict["img_releaseDate"] = (soup.find("h2", class_ = "category_title")).span.text.replace("|", "").strip()
            marsdict["img_featuredTitle"] = soup.find("h1", class_ = "article_title").text.replace("\t", "").replace("\n", "").strip()
            marsdict["img_featuredUrl"] = f"{'https://www.jpl.nasa.gov'}{(soup.find('figure', class_='lede')).a['href']}"
        except:
            print("Connection refused by the server..")
            print("Let me sleep for 1 seconds")
            print("ZZzzzz...")
            print(marsdict)
            time.sleep(15)
            print("Was a nice sleep, now let me continue...")
            i = i + 1
            continue 
                
    # return browser
    return browser
