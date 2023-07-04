import csv
import time
import scrapy
import os
import logging
from scrapy.crawler import CrawlerProcess

def trim_and_add_hyphens(string):
    trimmed_string = string.strip()
    split_string = trimmed_string.split()
    modified_string = "-".join(split_string)
    return modified_string

def input_output_folder():
    return f"{os.path.dirname(os.path.abspath(__file__))}/output"

log_file = os.path.join(input_output_folder(), 'error.log')
logging.basicConfig(
    filename=log_file,
    level=logging.ERROR,
    format='%(asctime)s [%(levelname)s] %(message)s'
)

class CreateShopbaseImportFileSpider(scrapy.Spider):
    name = 'create_shopbase_import_file'

    def start_requests(self):
        input_file_path = os.path.join(input_output_folder(), 
                                   'patanjali-ayurved-scrape.csv')
        with open(input_file_path, 'r') as file:
            reader = csv.DictReader(file)
            rows = list(reader)
            logging.info(f"Number of rows in output file: {len(rows)}")
            
            for row in rows:
                url = row['URL']
                last_breadcrumb = trim_and_add_hyphens(row['lastbreadcrumb'])
                heading = row['Heading']
                description = row['Description']
                sizes = row['Size'].split(',')
                image = row['Image']

                for size in sizes:
                    yield scrapy.Request(
                        url=url,
                        callback=self.parse,
                        meta={
                            'last_breadcrumb': last_breadcrumb,
                            'heading': heading,
                            'description': description,
                            'size': size.strip(),
                            'image': image
                        }
                    )
    '''
    https://help.shopbase.com/en/article/import-products-to-shopbase-by-csv-file-s0aqya/
    '''
    def parse(self, response):
        try:
            item = {
                'Product Id':'',
                'Variant Id':'',
                'Handle': response.meta['last_breadcrumb'],#required
                'Title': response.meta['heading'],#required
                'Body (Html)': response.meta['description'],
                'Vendor':'Patanjali',
                'Type':'',
                'Tags':'',#need to update based on breadcrumbs or url
                'Published':'TRUE',
                'Option Fulfill Value':'',
                'Custom Option':'[]',
                'Option1 Name':'Size',	
                'Option1 Value':response.meta['size'],
                'Option2 Name':'',	
                'Option2 Value':'',
                'Option3 Name':'',	
                'Option3 Value':'',
                'Variant Sku':'',
                'Variant Grams':'',#required
                'Variant Inventory Tracker':'',
                'Variant Inventory Qty':'',
                'Variant Inventory Policy':'continue',#required
                'Variant Fulfillment Service':'manual',#required
                'Variant Price':'0',#required
                'Variant Compare At Price':'0',
                'Variant Requires Shipping':'true',
                'Variant Taxable':'TRUE',
                'Variant Barcode':'',
                'Image Src': response.meta['image'],
                'Image Position':'',
                'Image Alt Text':response.meta['heading'],
                'Gift Card':'',
                'Google Shopping / Mpn':'',
                'Google Shopping / Age Group':'',
                'Google Shopping / Gender':'',
                'Google Shopping / Google Product Category':'',
                'Seo Title':'',
                'Seo Description':'',
                'Google Shopping / Adwords Grouping':'',
                'Google Shopping / Adwords Labels':'',
                'Google Shopping / Condition':'',
                'Google Shopping / Custom Product':'',
                'Google Shopping / Custom Label 0':'',
                'Google Shopping / Custom Label 1':'',
                'Google Shopping / Custom Label 2':'',
                'Google Shopping / Custom Label 3':'',
                'Google Shopping / Custom Label 4':'',
                'Variant Image':'','Variant Weight Unit':'',
                'Variant Tax Code':'',
                'Cost Per Item':'',
                'Available On Listing Pages':'TRUE',#required
                'Available On Sitemap Files':'TRUE',#required
                'Template':'',
                'Shipping Profile Name':'',
                'Variant Tag':'',
                'Facebook Pixel Id':'',
                'Facebook Access Token':'',
                'Product Stock Status':'',
                'Shipping Fee':'',
                'Base Cost Variant':''
            }
            yield item
        except Exception as e:
            logging.error(f"Error processing {response.url}: {str(e)}")

start_time = time.time()
output_file_path=f'file:{input_output_folder()}/shopbase-import.csv'
process = CrawlerProcess(settings={
    'FEED_FORMAT': 'csv',
    'FEED_URI': output_file_path,
    'LOG_ENABLED': False
})
process.spider_loader.spider_modules = ['spiders.create_shopbase_import_file']
process.spider_loader.ignore_missing_spiders = True
process.crawl(CreateShopbaseImportFileSpider)
process.start()

execution_time = time.time() - start_time
print(f"Script execution time: {execution_time} seconds")
