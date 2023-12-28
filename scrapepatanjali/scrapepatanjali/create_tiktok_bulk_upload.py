# sudo python3 ~/temp/scrapepatanjali/scrapepatanjali/scrapepatanjali/create_tiktok_bulk_upload.py /home/ajitgoel/Downloads/patanjaliayurvedus-website-products.csv /home/ajitgoel/Downloads/tiktok-shop-bulk-upload.csv

import csv
import argparse
from collections import OrderedDict
import os

def check_file_permissions(file_path):
   if os.access(file_path, os.R_OK):
       print(f"Read permission is granted for file: {file_path}")
   else:
       print(f"Read permission is not granted for file: {file_path}")

   if os.access(file_path, os.W_OK):
       print(f"Write permission is granted for file: {file_path}")
   else:
       print(f"Write permission is not granted for file: {file_path}")

   if os.access(file_path, os.X_OK):
       print(f"Execute permission is granted for file: {file_path}")
   else:
       print(f"Execute permission is not granted for file: {file_path}")

def filter_csv(input_filename, output_filename):
    # os.chmod(input_filename, 0o644)
    # os.chmod(output_filename, 0o644)
    #check_file_permissions(input_filename)
    #check_file_permissions(output_filename)
    new_columns = ['Category', 'Brand', 'Product Name', 'Product Description', 'Package Weight(lb)', 
                   'Package Length(inch)', 'Package Width(inch)', 'Package Height(inch)', 'Delivery options',
                   'Identifier Code Type', 'Identifier Code', 'Variation 1', 'Variation 2', 'Variant Image', 
                   'Retail Price (Local Currency)', 'Quantity in Patanjali Ayurved US', 'Seller SKU', 
                   'Main Product Image', 'Product Image 2', 'Product Image 3', 'Product Image 4', 
                   'Product Image 5', 'Product Image 6', 'Product Image 7', 'Product Image 8', 
                   'Product Image 9', 'Size Chart', 'Skin Type', 'Country Of Origin', 'Shelf Life', 
                   'Alcohol Or Aerosol', 'Allergen Information', 'Net Weight', 'Volume', 'Ingredients', 
                   'Quantity Per Pack', 'Skincare', 'Benefits', 'Body Care Benefits', 'Cautions/Warnings Manufacturer', 
                   'Drug Labeling', 'US Certificate of Conformity', 'Declaration of Conformity', 
                   'Cosmetics Packaging Labelling', 'Product Status']
    
    tags = ["oil", "body-cleanser", "toothpaste", "hair-oil", "shower-gel", "conditioner", "mehandi,hair-color", 
          "hair-cleanser", "shampoo", "face-wash", "face-scrub", "face-pack", "foot-care", "face-cream", "eye-liner"]

    with open(input_filename, 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        header = next(csv_reader)
        rows = [row for row in csv_reader]
        rows_published_true = [row for row in rows if row[header.index('Published')] == 'TRUE']
        rows_selectedTags = [row for row in rows_published_true if any(tag in row[header.index('Tags')].split(',') for tag in tags)]
        handle_values = list(set([row[header.index('Handle')] for row in rows_selectedTags]))
        handle_rows = [row for row in rows if row[header.index('Handle')] in handle_values]    

    with open(output_filename, 'w', newline='') as new_file:
        csv_writer = csv.writer(new_file)
        csv_writer.writerow(new_columns)
        for row in handle_rows:
            if row[header.index('Published')] == 'TRUE':
                new_row = [''] * len(new_columns)
                new_row[new_columns.index('Category')] = row[header.index('Tags')]
                new_row[new_columns.index('Product Name')] = row[header.index('Title')]
                new_row[new_columns.index('Brand')] = 'Patanjali'
                new_row[new_columns.index('Product Description')] = row[header.index('Body (Html)')]
                new_row[new_columns.index('Package Weight(lb)')] = row[header.index('Body (Html)')]
                
                new_row[new_columns.index('Identifier Code Type')] = 'UPC'
                new_row[new_columns.index('Identifier Code')] = row[header.index('Variant Sku')]
                new_row[new_columns.index('Retail Price (Local Currency)')] = row[header.index('Variant Sku')]
                new_row[new_columns.index('Quantity in Patanjali Ayurved US')] = row[header.index('Variant Sku')]
                new_row[new_columns.index('Seller SKU')] = row[header.index('Variant Sku')]
                new_row[new_columns.index('Main Product Image')] = row[header.index('Variant Sku')]
                new_row[new_columns.index('Product Image 2')] = row[header.index('Variant Sku')]
                new_row[new_columns.index('Product Image 2')] = row[header.index('Variant Sku')]
                new_row[new_columns.index('Product Image 3')] = row[header.index('Variant Sku')]
                new_row[new_columns.index('Product Image 4')] = row[header.index('Variant Sku')]
                new_row[new_columns.index('Product Image 5')] = row[header.index('Variant Sku')]
                new_row[new_columns.index('Product Image 6')] = row[header.index('Variant Sku')]
                new_row[new_columns.index('Product Image 7')] = row[header.index('Variant Sku')]
                new_row[new_columns.index('Product Image 8')] = row[header.index('Variant Sku')]
                new_row[new_columns.index('Product Image 9')] = row[header.index('Variant Sku')]
                new_row[new_columns.index('Country Of Origin')] = 'India'
                new_row[new_columns.index('Manufacturer')] = 'Patanjali'
                new_row[new_columns.index('Product Status')] = 'Draft'
                csv_writer.writerow(new_row)
        
    return

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('input_filename')
    parser.add_argument('output_filename')
    args, unknown = parser.parse_known_args()

    filter_csv(args.input_filename, args.output_filename)
if __name__ == '__main__':
    main()