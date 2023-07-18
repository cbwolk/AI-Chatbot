from bs4 import BeautifulSoup
from lxml import etree

import requests
import pandas as pd
import nest_asyncio
nest_asyncio.apply()

##################### IMPORTANT NOTE: ########################
### This key is note visible and should be hidden in a .env file

OPENAI_KEY = ''


##################################################
###### Getting XML links and product pages #######
##################################################

# Pretend to be a user so the site doesn't reject processing
header = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) '
                  'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

# Function adapted from https://stackoverflow.com/questions/31276001/parse-xml-sitemap-with-python
def links_from_xml(xml_link):
    req = requests.get(xml_link, headers=header)
    soup = BeautifulSoup(req.text, 'lxml')
    links = []

    for link in soup.findAll('loc'):
        links.append(link.getText('', True))

    return links

xml_links_parent = links_from_xml("https://www.homedepot.com/sitemap/P/PIPs.xml")
xml_links_children = []
product_links = []

for link in xml_links_parent:
    xml_links_children.extend(links_from_xml(link))

##################################################
############# Getting product links ##############
# It's very time intensive to get every link, so for
#  testing purposed I limit it to about 10.
# You can change the way the XML list and the corresponding
#  list of product links are spliced. Currently, I iterate
#  through a few product XML pages and get the first
#  few products listed in that category
##################################################

for link in xml_links_children[:5]:
    product_links.extend(links_from_xml(link)[:2])


##################################################
######## Getting product info from links #########
##################################################

newHeader = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                           '(KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36'}

consolidatedData = []

# The class name and XPath had various names depending on the product,
#   which is why in some cases multiple paths are attempted.
#   See the README for more information.
# Function adapted from https://www.freecodecamp.org/news/scraping-ecommerce-website-with-python/

for link in product_links:
    req = requests.get(link, headers=newHeader).text
    soup = BeautifulSoup(req, 'html.parser')
    dom = etree.HTML(str(soup))

    try:
        name = dom.xpath('//*[@id="root"]/div/div[3]/div/div/div[2]/div[1]/div[1]/div/div/div[3]/span/h1')[0].text
    except:
        try:
            name = dom.xpath('//*[@id="root"]/div/div[3]/div/div/div[2]/div[1]/div[1]/div/div/div[2]/span/h1')[0].text
        except:
            continue

    try:
        price = "$" + dom.xpath('//*[@id="standard-price"]/div/div/span[2]')[0].text
    except:
        try:
            price = "$" + dom.xpath('//*[@id="unit-price"]/div[1]/div[2]/span[2]')[0].text
        except:
            try:
                price = "$" + dom.xpath(
                    '//*[@id="root"]/div/div[3]/div/div/div[3]/div/div/div[1]/div/div/div/div/div[1]/div/span[2]')[
                    0].text
            except:
                price = "not available"

    try:
        about = dom.xpath('//*[@id="root"]/div/div[3]/div/div/div[3]/div/div/div[6]/ul/li[1]')[0].text + ". " + \
                dom.xpath('//*[@id="root"]/div/div[3]/div/div/div[3]/div/div/div[6]/ul/li[2]')[0].text + ". " + \
                dom.xpath('//*[@id="root"]/div/div[3]/div/div/div[3]/div/div/div[6]/ul/li[3]')[0].text
    except:
        about = "not available"

    try:
        rating = dom.xpath('//*[@id="root"]/div/div[3]/div/div/div[2]/div[1]/div[1]/div/div/div[5]/a[1]/@title')[0]
    except:
        try:
            rating = dom.xpath('//*[@id="root"]/div/div[3]/div/div/div[2]/div[1]/div[1]/div/div/div[4]/a[1]/@title')[0]
        except:
            rating = "not available"

    try:
        review_count = dom.xpath('//*[@id="product-details__review__target"]/span/text()[2]')[0]
    except:
        review_count = "not available"

    product_text = {"Product Info": "The name of the product is " + name + ". The price is " + price +
                                    ". The rating is " + rating + ". The number of reviews is " + review_count +
                                    ". The product information is as follows: " + about}

    consolidatedData.append(product_text)


##################################################
######## Generating CSV for product info #########
##################################################

dfConsolidated = pd.DataFrame(consolidatedData)
dfConsolidated.to_csv('ProductList.csv', index=False, header=True)
