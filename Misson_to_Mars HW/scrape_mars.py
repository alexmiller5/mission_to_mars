import pandas as pd
import urllib.request
from splinter import Browser
from bs4 import BeautifulSoup as bs
import time

def scrape_info():
    # this dictionary will hold everything we pull from all the sites
    scraped_data = {}

    # site 1 -
    news_url = "https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"

    # use [splinter &] beautiful soup to parse the url above
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)

    browser.visit(news_url)
    time.sleep(1)

    # Scrape page into Soup
    html = browser.html
    soup = bs(html, "html.parser")

    # use bs to find() [divs] and filter on the class_='content_tile'
    found_titles = soup.find_all('div',class_='content_title')

    news_title = found_titles[0].text
    scraped_data['news_title'] = news_title

    # use bs to find() the example_title_div and filter on the class_='article_teaser_body'
    found_teasers = soup.find_all('div',class_='article_teaser_body')

    news_p = found_teasers[0].text
    scraped_data['news_p'] = news_p

    # site 2 - https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars
    jpl_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'

    # use splinter to connect to the url and navigate, then use bs4 to repeat what you did in site 1
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)

    browser.visit(jpl_url)
    time.sleep(1)

    html = browser.html
    soup = bs(html, "html.parser")

    #get redirect link from featured pic
    found_box = soup.find_all('a',class_='fancybox')
    newurl = 'https://www.jpl.nasa.gov/' + found_box[0]['data-link']

    browser.visit(newurl)
    time.sleep(1)

    html = browser.html
    soup = bs(html, "html.parser")

    #get large image url from article page
    found_pic = soup.find_all('figure',class_='lede')[0].find('a')['href']
    featured_image_url = 'https://www.jpl.nasa.gov' + found_pic
    scraped_data['featured_image_url'] = featured_image_url

    # Example:
    #featured_image_url = 'https://www.jpl.nasa.gov/spaceimages/images/largesize/PIA16225_hires.jpg'
    #scraped_data['featured_image_url'] = featured_image_url

    # site 3 - https://twitter.com/marswxreport?lang=en
    twitter_url = 'https://twitter.com/marswxreport?lang=en'

    # grab the latest tweet and be careful its a weather tweet
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)

    browser.visit(twitter_url)
    time.sleep(1)

    html = browser.html
    soup = bs(html, "html.parser")

    found_tweet = soup.find(class_='js-tweet-text-container').find('p').text

    # Example:
    scraped_data['mars_weather'] = found_tweet #this may not go inside the dictionary as i thought

    # site 4 - 
    facts_url = 'https://space-facts.com/mars/'

    # use pandas to parse the table

    facts_df = pd.read_html(facts_url)[0]

    # convert facts_df to a html string and add to dictionary.
    facts = facts_df.to_html()
    scraped_data['facts'] = facts

    # site 5  https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars

    hemi_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'

    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)

    browser.visit(hemi_url)
    time.sleep(1)

    html = browser.html
    soup = bs(html, "html.parser")

    found_items = soup.find_all(class_='item')

    #build list of titles and links
    found_links = []
    found_titles = []

    a = 0
    for i in found_items:
        add_title = found_items[a].find('h3').text
        add_link = 'https://astrogeology.usgs.gov' + found_items[a].find(class_='itemLink product-item')['href']
        found_links.append(add_link)
        found_titles.append(add_title)
        a += 1

    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)

    #visit links to get imgs
    found_imgs = []

    a = 0
    for i in found_links:
        browser.visit(found_links[a])
        a +=1
        time.sleep(1)
        html = browser.html
        soup = bs(html, "html.parser")
        #get img url
        add_img = soup.find(class_='downloads').find('a')['href']
        found_imgs.append(add_img)
    
    #build list of dictionaries
    hemisphere_image_urls = []

    a = 0
    for i in found_titles:
        temp_d = {f'title{a}': found_titles[a], f'img_url{a}': found_imgs[a]}
        hemisphere_image_urls.append(temp_d)
        a += 1
   
    scraped_data['hemispheres'] = hemisphere_image_urls
    
    # Example:
    #hemisphere_image_urls = [
    #    {"title": "Valles Marineris Hemisphere", "img_url": "..."},
    #    {"title": "Cerberus Hemisphere", "img_url": "..."},
    #    {"title": "Schiaparelli Hemisphere", "img_url": "..."},
    #    {"title": "Syrtis Major Hemisphere", "img_url": "..."},
    #]
    return scraped_data
