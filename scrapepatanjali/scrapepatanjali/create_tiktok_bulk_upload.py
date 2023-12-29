# sudo python3 ~/temp/scrapepatanjali/scrapepatanjali/scrapepatanjali/create_tiktok_bulk_upload.py /home/ajitgoel/Downloads/patanjaliayurvedus-website-products.csv /home/ajitgoel/Downloads/tiktok-shop-bulk-upload.csv

import csv
import argparse
from collections import OrderedDict
import os
from operator import itemgetter
import psycopg2

def get_ingredients(handle):
  try:
      connection = psycopg2.connect(user="postgres",password="Meetha@1974",host="localhost",port="5432",
                                    database="postgres")
      cursor = connection.cursor()
      select_query = """SELECT ingredients,"{}" FROM "{}" WHERE handle = %s""".format("allergy-guide-content", "LatestInvoice09262023WithIngredients")

      cursor.execute(select_query, (handle,))
      result = cursor.fetchone()
      if result is not None:
          return result
      else:
          return None
  except (Exception, psycopg2.Error) as error:
      print("Failed to fetch ingredients from ingredients table", error)

  finally:
      if connection:
          cursor.close()
          connection.close()

def filter_csv(input_filename, output_filename):
    new_columns = ['Category', 'Brand', 'Product Name', 'Product Description', 'Package Weight(lb)', 
                   'Package Length(inch)', 'Package Width(inch)', 'Package Height(inch)', 'Delivery options',
                   'Identifier Code Type', 'Identifier Code', 'Variation 1', 'Variation 2', 'Variant Image', 
                   'Retail Price (Local Currency)', 'Quantity in Patanjali Ayurved US', 'Seller SKU', 
                   'Main Product Image', 'Product Image 2', 'Product Image 3', 'Product Image 4', 
                   'Product Image 5', 'Product Image 6', 'Product Image 7', 'Product Image 8', 
                   'Product Image 9', 'Size Chart', 'Skin Type', 'Country Of Origin', 'Shelf Life', 
                   'Alcohol Or Aerosol', 'Allergen Information', 'Net Weight', 'Volume', 'Ingredients', 
                   'Quantity Per Pack', 'Skincare Benefits', 'Body Care Benefits', 'Cautions/Warnings', 
                   'Manufacturer', 'Drug Labeling', 'US Certificate of Conformity', 'Declaration of Conformity', 
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
        handle_rows_filtered = list(filter(lambda row: row[header.index('Image Position')], handle_rows))
        handle_rows_ordered = sorted(handle_rows_filtered, key=itemgetter(header.index('Handle'), header.index('Image Position')))

    with open(output_filename, 'w', newline='') as new_file:
        csv_writer = csv.writer(new_file)
        csv_writer.writerow(new_columns)
        for row in handle_rows:
            handle=row[header.index('Handle')]
            result=get_ingredients(handle)
            tags = row[header.index('Tags')].split(',')
            if any(tag.strip().lower() in ["toothpaste"] for tag in tags):
                category = "Nasal & Oral Care/Toothpastes (601696)"
            elif any(tag.strip().lower() in ["shampoo", "conditioner", "hair-cleanser"] for tag in tags):
                category = "Haircare & Styling/Shampoo & Conditioner (601469)"
            elif any(tag.strip().lower() in ["eye-liner"] for tag in tags):
                category = "Makeup/Eyeliner & Lipliner (601587)"
            elif any(tag.strip().lower() in ["mehandi", "hair-color"] for tag in tags):
                category = "Haircare & Styling/Hair Dye (601516)"
            elif any(tag.strip().lower() in ["sun-screen"] for tag in tags):
                category = "Skincare/Facial Sunscreen & Sun Care (601602)"
            elif any(tag.strip().lower() in ["hair-oil"] for tag in tags):
                category = "Haircare & Styling/Hair Treatments/Scalp Treatments (981512)"
            elif any(tag.strip().lower() in ["oil"] for tag in tags):
                category = "Bath & Body Care/Body & Massage Oil (873736)"
            elif any(tag.strip().lower() in ["face-scrub"] for tag in tags):
                category = "Skincare/Face Scrubs & Peels (601613)"
            elif any(tag.strip().lower() in ["foot-care"] for tag in tags):
                category = "Hand, Foot & Nail Care/Hand Lotions, Creams & Scrubs (601480)"
            elif any(tag.strip().lower() in ["body-cleanser", "shower-gel"] for tag in tags):
                category = "Bath & Body Care/Body Wash & Soap (601493)"
            elif any(tag.strip().lower() in ["face-cream", "face-pack", "face-wash"] for tag in tags):
                category = "Skincare/Facial Cleansers (601609)"

            if row[header.index('Published')] == 'TRUE':
                new_row = [''] * len(new_columns)
                new_row[new_columns.index('Category')] = category
                new_row[new_columns.index('Product Name')] = row[header.index('Title')]
                new_row[new_columns.index('Brand')] = 'Patanjali'
                new_row[new_columns.index('Product Description')] = row[header.index('Body (Html)')]
                try:
                    weight_lbs = float(row[header.index('Variant Grams')]) * 0.00220462
                except ValueError:
                    weight_lbs = ''
                new_row[new_columns.index('Package Weight(lb)')] = weight_lbs

                new_row[new_columns.index('Identifier Code Type')] = 'UPC'
                new_row[new_columns.index('Identifier Code')] = row[header.index('Variant Sku')]
                new_row[new_columns.index('Retail Price (Local Currency)')] = row[header.index('Variant Price')]
                new_row[new_columns.index('Quantity in Patanjali Ayurved US')] = row[header.index('Variant Inventory Qty')]
                new_row[new_columns.index('Seller SKU')] = handle
                new_row[new_columns.index('Country Of Origin')] = 'India'
                new_row[new_columns.index('Ingredients')] = result[0]
                new_row[new_columns.index('Allergen Information')] = "" if str(result[1]).lower() in ["no", "", None] else result[1]

                new_row[new_columns.index('Manufacturer')] = 'Patanjali'
                new_row[new_columns.index('Product Status')] = 'Draft'

                filtered_handle_rows_ordered = list(filter(lambda x: x[header.index('Handle')] == handle, handle_rows_ordered))
                image_srcs = [row[header.index('Image Src')] for row in filtered_handle_rows_ordered]
                
                new_row[new_columns.index('Main Product Image')] = image_srcs[0]
                new_row[new_columns.index('Product Image 2')] = image_srcs[1] if len(image_srcs) > 1 else ''
                new_row[new_columns.index('Product Image 3')] = image_srcs[2] if len(image_srcs) > 2 else ''
                new_row[new_columns.index('Product Image 4')] = image_srcs[3] if len(image_srcs) > 3 else ''
                new_row[new_columns.index('Product Image 5')] = image_srcs[4] if len(image_srcs) > 4 else ''
                new_row[new_columns.index('Product Image 6')] = image_srcs[5] if len(image_srcs) > 5 else ''
                new_row[new_columns.index('Product Image 7')] = image_srcs[6] if len(image_srcs) > 6 else ''
                new_row[new_columns.index('Product Image 8')] = image_srcs[7] if len(image_srcs) > 7 else ''
                new_row[new_columns.index('Product Image 9')] = image_srcs[8] if len(image_srcs) > 8 else ''

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