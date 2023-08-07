import scrapy

from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import time

import csv
from collections import OrderedDict
import os
from urllib.parse import urlparse
import logging
import sys
import re
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utilities import trim_and_add_hyphens, input_output_folder

class PatanjaliSpider(scrapy.Spider):
    name = "patanjali"

    def start_requests(self):
        try:
            urls = [
                "https://www.patanjaliayurved.net/category/digestives/138",
                "https://www.patanjaliayurved.net/category/health-and-wellness/139",
                "https://www.patanjaliayurved.net/category/chyawanprash/150",
                "https://www.patanjaliayurved.net/category/badam-pak/151",
                "https://www.patanjaliayurved.net/category/ghee/152",
                "https://www.patanjaliayurved.net/category/honey/153",
                "https://www.patanjaliayurved.net/category/health-drinks/177",
                "https://www.patanjaliayurved.net/category/fruit-beverage/184",
                "https://www.patanjaliayurved.net/category/diet-food/218",
                "https://www.patanjaliayurved.net/category/biscuits-and-cookies/3",
                "https://www.patanjaliayurved.net/category/spices/11",
                "https://www.patanjaliayurved.net/category/candy/12",
                "https://www.patanjaliayurved.net/category/herbal-tea/13",
                "https://www.patanjaliayurved.net/category/jam/14",
                "https://www.patanjaliayurved.net/category/murabba/15",
                "https://www.patanjaliayurved.net/category/dalia-poha-and-vermicelli/130",
                "https://www.patanjaliayurved.net/category/flours/131",
                "https://www.patanjaliayurved.net/category/sauces-and-pickles/132",
                "https://www.patanjaliayurved.net/category/corn-flakes/183",
                "https://www.patanjaliayurved.net/category/dal-pulses/185",
                "https://www.patanjaliayurved.net/category/rice/186",
                "https://www.patanjaliayurved.net/category/noodles/190",
                "https://www.patanjaliayurved.net/category/oats/191",
                "https://www.patanjaliayurved.net/category/papad/192",
                "https://www.patanjaliayurved.net/category/namkeen/193",
                "https://www.patanjaliayurved.net/category/edible-oil/217",
                "https://www.patanjaliayurved.net/category/sweets/222",
                "https://www.patanjaliayurved.net/category/salt/230",
                "https://www.patanjaliayurved.net/category/sugar/231",
                "https://www.patanjaliayurved.net/category/dried-fruits-nuts/234",
                "https://www.patanjaliayurved.net/category/breakfast-cereals/243",
                "https://www.patanjaliayurved.net/category/kwath/5",
                #packages for diseases
                "https://www.patanjaliayurved.net/category/vati/16",
                "https://www.patanjaliayurved.net/category/bhasma/17",
                "https://www.patanjaliayurved.net/category/churna/18",
                "https://www.patanjaliayurved.net/category/guggul/19",
                "https://www.patanjaliayurved.net/category/parpati-ras/134",
                "https://www.patanjaliayurved.net/category/pishti/135",
                "https://www.patanjaliayurved.net/category/arishta/178",
                "https://www.patanjaliayurved.net/category/asava/179",
                "https://www.patanjaliayurved.net/category/syrup/181",
                "https://www.patanjaliayurved.net/category/godhan-ark/199",
                "https://www.patanjaliayurved.net/category/oil/208",
                "https://www.patanjaliayurved.net/category/lep/210",
                "https://www.patanjaliayurved.net/category/balm-inhaler/211",
                "https://www.patanjaliayurved.net/category/eye-ear-oral-care/248",
                "https://www.patanjaliayurved.net/category/agarbatti-and-dhoops/7",
                "https://www.patanjaliayurved.net/category/detergent-powder/33",
                "https://www.patanjaliayurved.net/category/detergent-cake/34",
                "https://www.patanjaliayurved.net/category/hand-wash-and-sanitizer/35",
                "https://www.patanjaliayurved.net/category/hawan-samagri/200",
                "https://www.patanjaliayurved.net/category/pooja-essentials/220",
                "https://www.patanjaliayurved.net/category/dishwash-bar-and-gel/221",
                "https://www.patanjaliayurved.net/category/toothpaste/22",
                "https://www.patanjaliayurved.net/category/tooth-brush/23",
                "https://www.patanjaliayurved.net/category/tooth-powder-manjan/147",  
                "https://www.patanjaliayurved.net/category/hair-care/24"
                "https://www.patanjaliayurved.net/category/hair-gel/219",
                "https://www.patanjaliayurved.net/category/body-care/25",
                "https://www.patanjaliayurved.net/category/eye-care/137",
                "https://www.patanjaliayurved.net/category/shishu-care/207",
                #Patanjali Publication
                "https://www.patanjaliayurved.net/category/swadeshi-samridhi-card/224",
                "https://www.patanjaliayurved.net/category/nutrition/233",
                "https://www.patanjaliayurved.net/category/nutrition-bar/235",
                "https://www.patanjaliayurved.net/category/spiritual/237",
                "https://www.patanjaliayurved.net/category/home/239",
                "https://www.patanjaliayurved.net/category/accessories/240",
                "https://www.patanjaliayurved.net/category/sports-wear/241",
                "https://www.patanjaliayurved.net/category/women-ethnic/242",
                "https://www.patanjaliayurved.net/category/copperware/245",
                "https://www.patanjaliayurved.net/category/dairy-frozen-items/247",
                "https://www.patanjaliayurved.net/category/notebook/256",
                "https://www.patanjaliayurved.net/category/bio-fertilizers/251",
                "https://www.patanjaliayurved.net/category/bio-pesticides/252",
                "https://www.patanjaliayurved.net/category/plant-growth-promoters/253",
                "https://www.patanjaliayurved.net/category/soil-testing/254",
                "https://www.patanjaliayurved.net/category/seeds/255",

            ]
            for url in urls:
                yield scrapy.Request(url, callback=self.parse_parent)
        except Exception as e:
            logging.error("An error occurred: %s", str(e))

    # def parse_LHS_Menu(self, response):
    #     child_urls = response.css('div.categorytree>ul>li>ul>li>a::attr(href)').getall()
    #     for child_url in child_urls:
    #         yield scrapy.Request(url=response.urljoin(child_url), callback=self.parse_child)

    def parse_parent(self, response):
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        self.driver = webdriver.Chrome(options=chrome_options)
        try:
            self.driver.get(response.url)
            time.sleep(2)  # Allow time for initial content to load
            # Handle popup if present
            try:
                popup_element = self.driver.find_element_by_xpath('//button[text()="No, thanks!"]')
                if popup_element:
                    popup_element.click()
                    time.sleep(2)  # Allow time for popup to close
            except:
                pass  # Popup not found, continue scraping

            # Scroll down the page to load more content
            for _ in range(5):  # Scroll down 5 times, adjust as needed
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(1)  # Allow time for more content to load

            # Extract the dynamically loaded content using JavaScript
            child_urls = self.driver.execute_script(
                'return Array.from(document.querySelectorAll("div#gridview>div>article>figure>a.figure-href"))'
            )
            for child_url in child_urls:
                yield scrapy.Request(
                    url=child_url.get_attribute('href'), callback=self.parse_child
                )
        except Exception as e:
            logging.error("An error occurred: %s", str(e))
        finally:
            self.driver.quit()

    def parse_child(self, response):
        lastbreadcrumb = response.css(
                "div.block-breadcrumb>ul.breadcrumb>li.active::text"
            ).get()
        heading = response.css("div.product-detail-section>h3::text").get()
        product_information_nested_text = response.xpath('//div[@class="product-information"]//div[@class=""]//*[normalize-space()]/text()').extract()
        product_information =' '.join(text.strip() for text in product_information_nested_text if text.strip())
        
        other_product_information_nested_text = response.xpath('//div[@id="accordion"]//*[normalize-space()]/text()').extract()
        other_product_information_complete_string=' '.join(text.strip() for text in other_product_information_nested_text if text.strip())
        keywords = ["Benefits ", "Ingredients ", "Other Product Info ", "How to use "]
        other_product_information = re.sub(f'({"|".join(keywords)})', r'\n<b>\1</b>\n', other_product_information_complete_string)
        
        variants = ", ".join(response.css(
                "div.col-md-5.col-sm-4.details-custom>div>select>option::text"
            ).getall())
        
        divs_with_images = response.css('div.col-xs-12.col-sm-12.col-md-6.col-lg-6 > div.row > div')
        if divs_with_images:
            productImages = [div.css('a > img::attr(src)').get() for div in divs_with_images]
            productImage = ','.join(productImages)
        else:
            productImage = response.css("#product-main::attr(src)").get()

        lastbreadcrumb = lastbreadcrumb.strip() if lastbreadcrumb is not None else ""
        heading = heading.strip() if heading is not None else ""
        variants = variants if variants is not None else ""
        productImage = productImage if productImage is not None else ""
        parsed_url = urlparse(response.url)
        path_parts = parsed_url.path.split('/')
        category = ','.join(path_parts[2:-2])
        data = {
            "url": response.url,
            'Tags': category,
            "lastbreadcrumb": lastbreadcrumb,
            "heading": heading,
            "cleaned-heading": re.sub(r'\s{3,}.*$', '', heading),
            "product-information": "<b>Product Information</b>\n"
            + product_information
            + other_product_information,
            "variants": variants,
            "product-image": productImage,
        }
        # if divs_with_images:
        #     for counter in productImages:
        #         yield scrapy.Request(counter, callback=self.parse_image)
        # else:
        #     yield scrapy.Request(productImage, callback=self.parse_image)
        
        filepath=os.path.join(input_output_folder(), "patanjali-ayurved-scrape.csv")
        if not os.path.isfile(filepath):
            with open(filepath, "w", newline="", encoding="utf-8") as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=data.keys())
                writer.writeheader()

        with open(filepath, 
                  "a", newline="", encoding="utf-8") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=data.keys())
            writer.writerow(data)

    def parse_image(self, response):
        file_name = response.url.split('/')[-1]
        folder_path = os.path.join(input_output_folder(), 'images')
    
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
        file_path = os.path.join(folder_path, file_name)
        with open(file_path, 'wb') as f:
            f.write(response.body)