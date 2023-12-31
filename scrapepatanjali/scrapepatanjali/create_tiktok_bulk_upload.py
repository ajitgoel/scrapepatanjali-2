# cd ~/temp/scrapepatanjali/ && source scrapy-env/bin/activate && sudo python3 ~/temp/scrapepatanjali/scrapepatanjali/scrapepatanjali/create_tiktok_bulk_upload.py /home/ajitgoel/Downloads/patanjaliayurvedus-website-products.csv /home/ajitgoel/Downloads

import csv
import argparse
from operator import itemgetter
import psycopg2
import math

BRAND='Patanjali (7046974046302439169)'

def to_float(value):
    try:
        return float(value)
    except ValueError:
        return 0

def calculate_net_weight(weight):
    if weight < 10:
        return "10g"
    elif 10 <= weight < 20:
        return"20g"
    elif 20 <= weight < 30:
        return"30g"
    elif 30 <= weight < 50:
        return"50g"
    elif 50 <= weight < 100:
        return"100g"
    elif 100 <= weight < 150:
        return"150g"
    elif 150 <= weight < 200:
        return"200g"
    elif 200 <= weight < 250:
        return"250g"
    elif 250 <= weight < 300:
        return"300g"
    else:
        return"500g"

def calculate_volume(size):
    if 'ltr' in size:
       size = int(size.replace('ltr', '')) * 1000
    if 'kg' in size:
       size = int(size.replace('kg', '')) * 1000
    elif 'ml' in size:
        size = int(size.replace('ml', ''))
    elif 'gm' in size:
        size = int(size.replace('gm', ''))

    if size < 10:
        return "10ml"
    elif 10 <= size < 20:
        return"20ml"
    elif 20 <= size < 30:
        return"30ml"
    elif 30 <= size < 50:
        return"50ml"
    elif 50 <= size < 100:
        return"100ml"
    elif 100 <= size < 150:
        return"150ml"
    elif 150 <= size < 200:
        return"200ml"
    elif 200 <= size < 250:
        return"250ml"
    elif 250 <= size < 300:
        return"300ml"
    else:
        return"500ml"

def get_ingredients(handle, size):
  try:
      connection = psycopg2.connect(user="postgres",password="Meetha@1974",host="localhost",port="5432",
                                    database="postgres")
      cursor = connection.cursor()
      select_query = f'SELECT ingredients, allergy_guide_content, length_inches, width_inches, height_inches FROM "LatestInvoice09262023WithIngredients" WHERE handle = \'{handle}\''
      cursor.execute(select_query)
      results = cursor.fetchall()
      if results:
          if len(results) > 1:
              size = size.replace(" ", "-").lower()
              select_query = f'SELECT ingredients, allergy_guide_content, length_inches, width_inches, height_inches FROM "LatestInvoice09262023WithIngredients" WHERE handle_unique = \'{handle}-{size}\''
              cursor.execute(select_query)
              size_results = cursor.fetchall()
              return size_results[0] if size_results else None
          else:
              return results[0]
      else:
          return None
  except (Exception, psycopg2.Error) as error:
      print("Failed to fetch ingredients from ingredients table", error)

  finally:
      if connection:
          cursor.close()
          connection.close()

def create_beauty_personal_care_file(input_filename, output_filename):
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

    TAGS_BEAUTY_PERSONAL_CARE = ["oil", "body-cleanser", "toothpaste", "hair-oil", "shower-gel", "conditioner",
                                 "mehandi", "hair-color", "hair-cleanser", "shampoo", "face-wash", "face-scrub",
                                 "face-pack", "foot-care", "face-cream", "eye-liner", "kajal", "eye-care",
                                 #"sun-screen", "agarbatti-and-dhoops"
                                 ]

    with open(input_filename, 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        header = next(csv_reader)
        rows = [row for row in csv_reader]
        rows_published_true = [row for row in rows if row[header.index('Published')] == 'TRUE']
        rows_selectedTags = [row for row in rows_published_true if any(tag in row[header.index('Tags')].split(',')
                                                                       for tag in TAGS_BEAUTY_PERSONAL_CARE)]
        handle_values = list(set([row[header.index('Handle')] for row in rows_selectedTags]))
        handle_rows = [row for row in rows if row[header.index('Handle')] in handle_values]   
        handle_rows_filtered = list(filter(lambda row: row[header.index('Image Position')], handle_rows))
        handle_rows_ordered = sorted(handle_rows_filtered, key=itemgetter(header.index('Handle'),
                                                                          header.index('Image Position')))

    with (open(f'{output_filename}/tiktok_bulk_upload_beauty_personal_care_file.csv', 'w', newline='') as new_file):
        csv_writer = csv.writer(new_file, quoting=csv.QUOTE_ALL)
        csv_writer.writerow(new_columns)
        for row in handle_rows:
            if row[header.index('Published')] == 'TRUE':
                handle=row[header.index('Handle')]
                size=row[header.index('Option1 Value')]
                
                result=get_ingredients(handle, size)
                tags = row[header.index('Tags')].split(',')
                weight = to_float(row[header.index('Variant Grams')])
                new_row = [''] * len(new_columns)
                if any(tag.strip().lower() in ["toothpaste"] for tag in tags):
                    category = "Nasal & Oral Care/Toothpastes (601696)"
                elif any(tag.strip().lower() in ["shampoo", "conditioner", "hair-cleanser"] for tag in tags):
                    category = "Haircare & Styling/Shampoo & Conditioner (601469)"
                elif any(tag.strip().lower() in ["eye-liner", "kajal", "eye-care"] for tag in tags):
                    category = "Makeup/Eyeliner & Lipliner (601587)"
                elif any(tag.strip().lower() in ["mehandi", "hair-color"] for tag in tags):
                    category = "Haircare & Styling/Hair Dye (601516)"
                elif any(tag.strip().lower() in ["sun-screen"] for tag in tags):
                    category = "Skincare/Facial Sunscreen & Sun Care (601602)"
                elif any(tag.strip().lower() in ["hair-oil"] for tag in tags):
                    category = "Haircare & Styling/Hair Treatments/Scalp Treatments (981512)"
                elif any(tag.strip().lower() in ["oil"] for tag in tags):
                    category = "Bath & Body Care/Body & Massage Oil (873736)"
                    new_row[new_columns.index('Volume')] = calculate_volume(size)
                elif any(tag.strip().lower() in ["face-scrub"] for tag in tags):
                    category = "Skincare/Face Scrubs & Peels (601613)"
                elif any(tag.strip().lower() in ["foot-care"] for tag in tags):
                    category = "Hand, Foot & Nail Care/Hand Lotions, Creams & Scrubs (601480)"
                    new_row[new_columns.index('Volume')] = calculate_volume(size)
                elif any(tag.strip().lower() in ["body-cleanser", "shower-gel"] for tag in tags):
                    category = "Bath & Body Care/Body Wash & Soap (601493)"
                elif any(tag.strip().lower() in ["face-cream", "face-pack", "face-wash"] for tag in tags):
                    category = "Skincare/Facial Cleansers (601609)"
                    
                new_row[new_columns.index('Category')] = category
                new_row[new_columns.index('Product Name')] = row[header.index('Title')]
                new_row[new_columns.index('Brand')] = BRAND
                new_row[new_columns.index('Product Description')] = row[header.index('Body (Html)')]
                new_row[new_columns.index('Package Weight(lb)')] = math.ceil(weight)
                new_row[new_columns.index('Net Weight')] = calculate_net_weight(weight/0.00220462)

                new_row[new_columns.index('Identifier Code Type')] = 'UPC (3)'
                new_row[new_columns.index('Identifier Code')] = row[header.index('Variant Sku')]
                new_row[new_columns.index('Retail Price (Local Currency)')] = row[header.index('Variant Price')]
                new_row[new_columns.index('Quantity in Patanjali Ayurved US')] = row[header.index('Variant Inventory Qty')]
                new_row[new_columns.index('Seller SKU')] = handle[:49]
                new_row[new_columns.index('Country Of Origin')] = 'India'
                new_row[new_columns.index('Ingredients')] = result[0].replace(',',';')
                new_row[new_columns.index('Allergen Information')] = result[1].replace(',',';')
                new_row[new_columns.index('Package Length(inch)')] = 1 if to_float(result[2])<1 else to_float(result[2])
                new_row[new_columns.index('Package Width(inch)')] = 1 if to_float(result[3])<1 else to_float(result[3])
                new_row[new_columns.index('Package Height(inch)')] = 1 if to_float(result[4])<1 else to_float(result[4])
                new_row[new_columns.index('Quantity Per Pack')] = '1'
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
                #Please upload a clear photo of the product labelling showing the list of ingredients, any applicable warnings or instructions of use
                new_row[new_columns.index('Cosmetics Packaging Labelling')] = image_srcs[1] if len(image_srcs) > 1 else ''
                csv_writer.writerow(new_row)
        
    return

def create_food_beverages_file(input_filename, output_filename):
    new_columns = ['Category', 'Brand', 'Product Name', 'Product Description', 'Package Weight(lb)',
                   'Package Length(inch)', 'Package Width(inch)', 'Package Height(inch)', 'Delivery options',
                   'Identifier Code Type', 'Identifier Code', 'Variation 1', 'Variation 2', 'Variant Image',
                   'Retail Price (Local Currency)', 'Quantity in Patanjali Ayurved US', 'Seller SKU',
                   'Main Product Image', 'Product Image 2', 'Product Image 3', 'Product Image 4', 'Product Image 5',
                   'Product Image 6', 'Product Image 7', 'Product Image 8', 'Product Image 9', 'Size Chart',
                   'Country Of Origin', 'Allergen Information', 'Net Weight', 'Volume', 'Ingredients',
                   'Alcohol Percentage', 'Age Warning', 'Organic', 'Year of Production', 'Packaging Type',
                   'Manufacturer', 'Storage Type', 'Flavor', 'Food Labeling', 'Product Status']
    TAGS_FOOD_BEVERAGES = ["badam-pak", "biscuits-and-cookies", "breakfast-cereals", "chyawanprash",
                           "dalia-poha-and-vermicelli", "digestives", "dosa", "edible-oil", "eye-care",
                           "ghee", "health-drinks", "honey", "idli", "noodles", "rice", "salt", "soya-chunks", "spices"]
    with open(input_filename, 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        header = next(csv_reader)
        rows = [row for row in csv_reader]
        rows_published_true = [row for row in rows if row[header.index('Published')] == 'TRUE']
        rows_selectedTags = [row for row in rows_published_true if any(tag in row[header.index('Tags')].split(',') for tag in TAGS_FOOD_BEVERAGES)]
        handle_values = list(set([row[header.index('Handle')] for row in rows_selectedTags]))
        handle_rows = [row for row in rows if row[header.index('Handle')] in handle_values]   
        handle_rows_filtered = list(filter(lambda row: row[header.index('Image Position')], handle_rows))
        handle_rows_ordered = sorted(handle_rows_filtered, key=itemgetter(header.index('Handle'), header.index('Image Position')))

    with open(f'{output_filename}/tiktok_bulk_upload_food_beverages_file.csv', 'w', newline='') as new_file:
        csv_writer = csv.writer(new_file, quoting=csv.QUOTE_ALL)
        csv_writer.writerow(new_columns)
        for row in handle_rows:
            if row[header.index('Published')] == 'TRUE':
                handle=row[header.index('Handle')]
                size=row[header.index('Option1 Value')]
                
                result=get_ingredients(handle, size)
                tags = row[header.index('Tags')].split(',')
                weight = to_float(row[header.index('Variant Grams')])
                new_row = [''] * len(new_columns)
                if any(tag.strip().lower() in ["badam-pak", "chyawanprash"] for tag in tags):
                    category = "Instant Food/Canned, Jarred & Packaged Foods (918280)"
                elif any(tag.strip().lower() in ["biscuits-and-cookies"] for tag in tags):
                    category = "Snacks/Biscuits, Cookies & Wafers (700553)"
                elif any(tag.strip().lower() in ["breakfast-cereals", "dalia-poha-and-vermicelli", "dosa", "idli", "noodles"] for tag in tags):
                    category = "Staples & Cooking Essentials/Pasta, Noodles & Vermicelli (918024)"
                elif any(tag.strip().lower() in ["digestives"] for tag in tags):
                    category = "Snacks/Candy (921736)"
                elif any(tag.strip().lower() in ["edible-oil", "ghee"] for tag in tags):
                    category = "Staples & Cooking Essentials/Oils (918920)"
                elif any(tag.strip().lower() in ["health-drinks"] for tag in tags):
                    category = "Drinks/Juice & Smoothies (916744)"
                elif any(tag.strip().lower() in ["honey"] for tag in tags):
                    category = "Staples & Cooking Essentials/Honey & Maple Syrup (920328)"
                elif any(tag.strip().lower() in ["rice"] for tag in tags):
                    category = "Staples & Cooking Essentials/Rice (917896)"
                elif any(tag.strip().lower() in ["salt"] for tag in tags):
                    category = "Staples & Cooking Essentials/Salt (919304)"
                elif any(tag.strip().lower() in ["spices"] for tag in tags):
                    category = "Staples & Cooking Essentials/Herbs, Spices & Seasonings (919176)"
                elif any(tag.strip().lower() in ["soya-chunks"] for tag in tags):
                    category = "Staples & Cooking Essentials/Dried Foods (963336)"

                new_row[new_columns.index('Category')] = category
                new_row[new_columns.index('Product Name')] = row[header.index('Title')]
                new_row[new_columns.index('Brand')] = BRAND
                new_row[new_columns.index('Product Description')] = row[header.index('Body (Html)')]
                new_row[new_columns.index('Package Weight(lb)')] = math.ceil(weight)
                new_row[new_columns.index('Net Weight')] = calculate_net_weight(weight/0.00220462)

                new_row[new_columns.index('Identifier Code Type')] = 'UPC (3)'
                new_row[new_columns.index('Identifier Code')] = row[header.index('Variant Sku')]
                new_row[new_columns.index('Retail Price (Local Currency)')] = row[header.index('Variant Price')]
                new_row[new_columns.index('Quantity in Patanjali Ayurved US')] = row[header.index('Variant Inventory Qty')]
                new_row[new_columns.index('Seller SKU')] = handle[:49]
                new_row[new_columns.index('Country Of Origin')] = 'India'
                new_row[new_columns.index('Ingredients')] = result[0].replace(',',';')
                new_row[new_columns.index('Allergen Information')] = result[1].replace(',',';')
                new_row[new_columns.index('Package Length(inch)')] = 1 if to_float(result[2])<1 else to_float(result[2])
                new_row[new_columns.index('Package Width(inch)')] = 1 if to_float(result[3])<1 else to_float(result[3])
                new_row[new_columns.index('Package Height(inch)')] = 1 if to_float(result[4])<1 else to_float(result[4])
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
                new_row[new_columns.index('Age Warning')] = 'No'
                # Please upload a clear product labeling photo showing the product name, the list of ingredients, declaration of allergens, nutrition facts labels, name and address of the manufacturer or distributor, net content quantity and weight and country of origin in English language.
                new_row[new_columns.index('Food Labeling')] = image_srcs[1] if len(image_srcs) > 1 else ''

                csv_writer.writerow(new_row)
    return

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('input_filename')
    parser.add_argument('output_filename')
    args, unknown = parser.parse_known_args()

    create_beauty_personal_care_file(args.input_filename, args.output_filename)
    create_food_beverages_file(args.input_filename, args.output_filename)
if __name__ == '__main__':
    main()