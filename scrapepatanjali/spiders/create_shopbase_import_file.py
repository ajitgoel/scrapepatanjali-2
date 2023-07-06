import csv
import time
import os
import logging
from utilities import trim_and_add_hyphens, input_output_folder

log_file = os.path.join(input_output_folder(), 'error.log')
logging.basicConfig(
    filename=log_file,
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s'
)

def process_input_file():
    input_file_path = os.path.join(input_output_folder(), 'patanjali-ayurved-scrape.csv')
    with open(input_file_path, 'r') as file:
        reader = csv.DictReader(file)
        rows = list(reader)
        logging.info(f"Number of rows in input file: {len(rows)}")
        
        for row in rows:
            url = row['URL']
            last_breadcrumb = trim_and_add_hyphens(row['lastbreadcrumb'])
            heading = row['Heading']
            description = row['Description']
            sizes = row['Size'].split(',')
            image = row['Image']
            tags = row['Tags']
            for size in sizes:
                item = process_row(url, last_breadcrumb, heading, description, size.strip(), image, tags)
                yield item

def process_row(url, last_breadcrumb, heading, description, size, image, tags):
    item = {
        'Product Id': '',
        'Variant Id': '',
        'Handle': last_breadcrumb,
        'Title': heading,
        'Body (Html)': description,
        'Vendor': 'Patanjali',
        'Type': '',
        'Tags': tags,
        'Published': 'TRUE',
        'Option Fulfill Value': '',
        'Custom Option': '[]',
        'Option1 Name': 'Size',	
        'Option1 Value': size,
        'Option2 Name': '',	
        'Option2 Value': '',
        'Option3 Name': '',	
        'Option3 Value': '',
        'Variant Sku': '',
        'Variant Grams': '',
        'Variant Inventory Tracker': '',
        'Variant Inventory Qty': '',
        'Variant Inventory Policy': 'continue',
        'Variant Fulfillment Service': 'manual',
        'Variant Price': '0',
        'Variant Compare At Price': '0',
        'Variant Requires Shipping': 'true',
        'Variant Taxable': 'TRUE',
        'Variant Barcode': '',
        'Image Src': image,
        'Image Position': '',
        'Image Alt Text': heading,
        'Gift Card': '',
        'Google Shopping / Mpn': '',
        'Google Shopping / Age Group': '',
        'Google Shopping / Gender': '',
        'Google Shopping / Google Product Category': '',
        'Seo Title': '',
        'Seo Description': '',
        'Google Shopping / Adwords Grouping': '',
        'Google Shopping / Adwords Labels': '',
        'Google Shopping / Condition': '',
        'Google Shopping / Custom Product': '',
        'Google Shopping / Custom Label 0': '',
        'Google Shopping / Custom Label 1': '',
        'Google Shopping / Custom Label 2': '',
        'Google Shopping / Custom Label 3': '',
        'Google Shopping / Custom Label 4': '',
        'Variant Image': '',
        'Variant Weight Unit': '',
        'Variant Tax Code': '',
        'Cost Per Item': '',
        'Available On Listing Pages': 'TRUE',
        'Available On Sitemap Files': 'TRUE',
        'Template': '',
        'Shipping Profile Name': '',
        'Variant Tag': '',
        'Facebook Pixel Id': '',
        'Facebook Access Token': '',
        'Product Stock Status': '',
        'Shipping Fee': '',
        'Base Cost Variant': ''
    }
    return item
#https://help.shopbase.com/en/article/import-products-to-shopbase-by-csv-file-s0aqya/
def generate_output_file():
    start_time = time.time()
    output_file_path = f'{input_output_folder()}/shopbase-import.csv'
    rows_processed = 0

    with open(output_file_path, 'w', newline='') as file:
        fieldnames = [
            'Product Id', 'Variant Id', 'Handle', 'Title', 'Body (Html)', 'Vendor', 'Type', 'Tags', 'Published',
            'Option Fulfill Value', 'Custom Option', 'Option1 Name', 'Option1 Value', 'Option2 Name', 'Option2 Value',
            'Option3 Name', 'Option3 Value', 'Variant Sku', 'Variant Grams', 'Variant Inventory Tracker',
            'Variant Inventory Qty', 'Variant Inventory Policy', 'Variant Fulfillment Service', 'Variant Price',
            'Variant Compare At Price', 'Variant Requires Shipping', 'Variant Taxable', 'Variant Barcode',
            'Image Src', 'Image Position', 'Image Alt Text', 'Gift Card', 'Google Shopping / Mpn',
            'Google Shopping / Age Group', 'Google Shopping / Gender', 'Google Shopping / Google Product Category',
            'Seo Title', 'Seo Description', 'Google Shopping / Adwords Grouping', 'Google Shopping / Adwords Labels',
            'Google Shopping / Condition', 'Google Shopping / Custom Product', 'Google Shopping / Custom Label 0',
            'Google Shopping / Custom Label 1', 'Google Shopping / Custom Label 2', 'Google Shopping / Custom Label 3',
            'Google Shopping / Custom Label 4', 'Variant Image', 'Variant Weight Unit', 'Variant Tax Code',
            'Cost Per Item', 'Available On Listing Pages', 'Available On Sitemap Files', 'Template',
            'Shipping Profile Name', 'Variant Tag', 'Facebook Pixel Id', 'Facebook Access Token', 'Product Stock Status',
            'Shipping Fee', 'Base Cost Variant'
        ]
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()

        for item in process_input_file():
            writer.writerow(item)
            rows_processed += 1

    execution_time = time.time() - start_time
    logging.info(f"Script execution time: {execution_time} seconds")
    logging.info(f"Number of rows processed: {rows_processed}")

generate_output_file()