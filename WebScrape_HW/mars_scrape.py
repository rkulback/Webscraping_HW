# Import ependencies
from bs4 import BeautifulSoup
import requests
import pymongo
from splinter import Browser
import time
import pandas as pd

 # Initialize PyMongo to work with MongoDBs
conn = 'mongodb://localhost:27017'
client = pymongo.MongoClient(conn)

 # Define database and collection
db = client.mars_db
collection = db.items


#start splinter to conduct searches
def my_browser():
    executable_path = {'executable_path': '/Users/ryankulback/Desktop/Pandas-Project/chromedriver'}
    return Browser('chrome', **executable_path, headless=False)

def mars_scrape():

    mars_book = {}

    browser = my_browser()

    # mars headlines URL with a sleep to ensure page is able to fully load
    mars_headlines_url = "https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"

    browser.visit(mars_headlines_url)
    time.sleep(1)

    # Navigate Splinter to the news articles section, find and store the first articles title
    mars_latest_news_title_first_li = browser.find_by_css('body .item_list .slide').first

    mars_latest_news_title = mars_latest_news_title_first_li.find_by_css('.content_title a').value

    # Find and store the first articles text
    mars_latest_news_ptext = mars_latest_news_title_first_li.find_by_css('.article_teaser_body').value

    # append values to the dictionary

    mars_book['mars_headline'] = mars_latest_news_title
    mars_book['mars_text'] = mars_latest_news_ptext

    # JPL Mars Image to get high res featured image
    # image is not always of mars but instructions say to get the featured image

    jpl_image_site_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"

    base_url = "https://www.jpl.nasa.gov"

    browser.visit(jpl_image_site_url)

    # click the image link to get a high res image
    full_image = browser.find_by_id('full_image').first.click() 

    time.sleep(1)

    featured_image_url = browser.find_by_css('img.fancybox-image')['src']

    mars_book['feature_image']= featured_image_url

    #mars weather tweet information
    #possible issue if the first tweet is not a weather report - may have to code saftey provision

    mars_weather_url = "https://twitter.com/marswxreport?lang=en"
    browser.visit(mars_weather_url)

    tweet_body = browser.find_by_css('div .js-tweet-text-container').first

    mars_weather = tweet_body.text

    mars_book['latest_weather'] = mars_weather

    #mars facts using pandas

    mars_facts_url = "https://space-facts.com/mars/"

    mars_html = pd.read_html(mars_facts_url)

    mars_html_cleaned = mars_html[0]

    mars_html_cleaned.rename(columns={0:"description", 1:"value"}, inplace=True)

    mars_html_cleaned.set_index("description", inplace=True)

    mars_facts = mars_html_cleaned.to_html()

    mars_book['mars_facts'] = mars_facts

    #mars hemispheres

    mars_hemis_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"

    browser.visit(mars_hemis_url)

    time.sleep(.5)

    #this code clicks the third element in the list to get high res image of cerberus hemi

    cerberus_block = browser.find_by_css('div .result-list')

    cerberus_hemi = cerberus_block.find_by_css('div .item')[0]

    cerberus_link = cerberus_hemi.find_by_css('div .description a').click()

    time.sleep(.5)

    cerberus_body = browser.find_by_css('div .downloads')

    cerberus_image = cerberus_body.find_by_css('li a')['href']

    mars_book['cerberus_hemi'] = cerberus_image

    browser.back()

    time.sleep(.5)

    #this code clicks the third element in the list to get high res image of schiaparelli hemi

    schiaparelli_block = browser.find_by_css('div .result-list')

    schiaparelli_hemi = schiaparelli_block.find_by_css('div .item')[1]

    schiaparelli_link = schiaparelli_hemi.find_by_css('div .description a').click()

    time.sleep(.5)

    schiaparelli_body = browser.find_by_css('div .downloads')

    schiaparelli_image = schiaparelli_body.find_by_css('li a')['href']

    mars_book['schiaparelli_hemi'] = schiaparelli_image

    browser.back()

    time.sleep(.5)

    #this code clicks the third element in the list to get high res image of syrtis hemi

    syrtis_block = browser.find_by_css('div .result-list')

    syrtis_hemi = syrtis_block.find_by_css('div .item')[2]

    syrtis_link = syrtis_hemi.find_by_css('div .description a').click()

    time.sleep(.5)

    syrtis_body = browser.find_by_css('div .downloads')

    syrtis_image = syrtis_body.find_by_css('li a')['href']

    mars_book['syrtis_hemi'] = syrtis_image

    browser.back()

    time.sleep(.5)

    #this code clicks the third element in the list to get high res image of valles hemi

    valles_block = browser.find_by_css('div .result-list')

    valles_hemi = valles_block.find_by_css('div .item')[3]

    valles_link = valles_hemi.find_by_css('div .description a').click()

    time.sleep(.5)

    valles_body = browser.find_by_css('div .downloads')

    valles_image = valles_body.find_by_css('li a')['href']

    mars_book['valles_hemi'] = valles_image

    browser.quit()

    collection.insert_one(mars_book)

    return mars_book


