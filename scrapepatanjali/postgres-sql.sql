select --a." Description of Goods ",b."PRODUCT DETAILS",a."Code2", b.code, 
a.*,b.pack from 
"LatestInvoice-09262023" a left outer join "Invoice-07062023" b
on a."Code2"=b.code

--PricingComparison between Invoice09262023 and Invoice07062023
select currentinvoice." Description of Goods ", 
previousinvoice."Price per Unit (USD)" "Previous unit price", 
currentinvoice." Unit price in USD "  "Current unit price", 
currentinvoice." Quantity in Pcs " "Total quantity ordered",
(previousinvoice."Price per Unit (USD)" * currentinvoice." Quantity in Pcs ") "Total amount that should have been charged", 
currentinvoice." Total amt. In USD " "Total amount Charged", 
(currentinvoice." Total amt. In USD " - (previousinvoice."Price per Unit (USD)" * currentinvoice." Quantity in Pcs ")) "Difference" 
from 
"LatestInvoice-09262023" currentinvoice left outer join "Invoice-07062023" previousinvoice
on currentinvoice."Code2"=previousinvoice.code

select currentinvoice." Description of Goods ", ingredients."Product Title" from 
"LatestInvoice-09262023" currentinvoice left outer join ingredients_list ingredients
--ON levenshtein(currentinvoice." Description of Goods " , ingredients."Product Title") < 3
ON levenshtein(regexp_replace(currentinvoice." Description of Goods ", '[^a-zA-Z0-9]', '', 'g'), 
               regexp_replace(ingredients."Product Title", '[^a-zA-Z0-9]', '', 'g')) < 3
order by ingredients."Product Title" asc

select currentinvoice." Description of Goods " as "Invoice title", currentinvoice." Pack Size " as "Invoice SKU",
ingredients."Product Title" as "Ingredients title",
ingredients."Product SKU" as "Ingredients SKU",
currentinvoice." Sr. Nos ", currentinvoice."Code1", currentinvoice."Code2", currentinvoice."Code3", 
currentinvoice." Description of Goods ", currentinvoice." Pack Size ", currentinvoice." HS CODE ", 
currentinvoice." Quantity Per Box ", currentinvoice." Quantity in Pcs ", currentinvoice." Unit price in USD ",
currentinvoice." Total amt. In USD ",
ingredients."Product Description", ingredients."Product Key features", ingredients."Product SKU", 
ingredients."Product UPC USA", ingredients."Product Dimension (L*W*H) Inches", 
ingredients.ingredients, ingredients."Artificial food colour (Yes/No)", ingredients."Allergy guide content"
from 
"LatestInvoice-09262023" currentinvoice left outer join ingredients_list ingredients
ON fuzzy_match_difflib(currentinvoice." Description of Goods ", ingredients."Product Title")>0.9
order by 
ingredients."Product Title" asc


select currentinvoice." Description of Goods " as "Invoice title", currentinvoice." Pack Size " as "Invoice SKU",
ingredients."Product Title" as "Ingredients title",
ingredients."Product SKU" as "Ingredients SKU",
currentinvoice." Sr. Nos ", currentinvoice."Code1", currentinvoice."Code2", currentinvoice."Code3", 
currentinvoice." Description of Goods ", currentinvoice." Pack Size ", currentinvoice." HS CODE ", 
currentinvoice." Quantity Per Box ", currentinvoice." Quantity in Pcs ", currentinvoice." Unit price in USD ",
currentinvoice." Total amt. In USD ",
ingredients."Product Description", ingredients."Product Key features", ingredients."Product SKU", 
ingredients."Product UPC USA", ingredients."Product Dimension (L*W*H) Inches", 
ingredients.ingredients, ingredients."Artificial food colour (Yes/No)", ingredients."Allergy guide content"
from 
"LatestInvoice-09262023" currentinvoice cross join ingredients_list ingredients
--ON fuzzy_match_difflib(REPLACE(currentinvoice." Description of Goods ", 'Patanjali', ''), 
--REPLACE(ingredients.product, 'Patanjali', ''))>0.1
where --currentinvoice." Sr. Nos " in (89) and 
currentinvoice." Sr. Nos " in (80,
81,
83,
87,
94
) and ingredients."Sr. No" in (50)
--currentinvoice." Description of Goods " IN ('Patanjali Rose Body Cleanser') and ingredients."Product Title" IN ('Patanjali Rose Body Cleanser')
order by ingredients."Product Title" asc

select i."Price per Unit (USD)" as "old price", d."Price per Unit (USD)" as "new price", 
d."PRODUCT DETAILS", d."PACK SIZE", d.* 
from "Invoice-07062023_WithAllProducts" i right outer join "draftinvoice-10162023" d on i.code=d.code 
order by i."Price per Unit (USD)" desc, d."PRODUCT DETAILS" asc

select i.category,d.description, d." Pack Size ", d."added-to-amazon",d."amazon-comments", addedtowebsite, 
d."patanjali-ayurved-url" , d.* 
from "Invoice-07062023_WithAllProducts" i right outer join "LatestInvoice-09262023_WithOtherInfo" d 
on i.code=d."Code2"
where d.description ilike '%Almond%'

select i.category,d.description, d." Pack Size ", d."added-to-amazon",d."amazon-comments", addedtowebsite, 
d."patanjali-ayurved-url" , d.* 
from "Invoice-07062023_WithAllProducts" i right outer join "LatestInvoice-09262023_WithOtherInfo" d 
on i.code=d."Code2" where d.description ilike '%Saundarya%'
--where addedtowebsite =0
select il."Product Title",il."Product UPC USA", * from ingredients_list il where 
--il."Product Title" ilike '%Rose%'
il."Product UPC USA" ilike '8904109420597'

SELECT TABLE_NAME, COLUMN_NAME FROM information_schema.columns WHERE COLUMN_NAME ILIKE '%upc%';

select " Unit price in USD ", * from public."LatestInvoice-09262023_WithOtherInfo" 

INSERT INTO public."LatestInvoice-09262023_WithOtherInfo"
SELECT * FROM public."LatestInvoice-09262023";

select count(*) from "LatestInvoice-09262023_WithOtherInfo" liwoi where addedtowebsite =1

select currentinvoice." Description of Goods " as "Invoice title", currentinvoice." Pack Size " as "Invoice SKU",
ingredients."Product Title" as "Ingredients title",
ingredients."Product SKU" as "Ingredients SKU",
currentinvoice." Sr. Nos ", currentinvoice."Code1", currentinvoice."Code2", currentinvoice."Code3", 
currentinvoice." Description of Goods ", currentinvoice." Pack Size ", currentinvoice." HS CODE ", 
currentinvoice." Quantity Per Box ", currentinvoice." Quantity in Pcs ", currentinvoice." Unit price in USD ",
currentinvoice." Total amt. In USD ",
ingredients."Product Description", ingredients."Product Key features", ingredients."Product SKU", 
ingredients."Product UPC USA", ingredients."Product Dimension (L*W*H) Inches", 
ingredients.ingredients, ingredients."Artificial food colour (Yes/No)", ingredients."Allergy guide content"
from 
"LatestInvoice-09262023" currentinvoice cross join ingredients_list ingredients
where currentinvoice." Description of Goods " in (
'Kesh Kanti Herbal Mehandi (Dark Brown)-T') and 
ingredients."Product Title" in (
'Patanjali Kesh Kanti Herbal Mehandi (Dark Brown)')
order by ingredients."Product Title" asc

SELECT * FROM pg_extension WHERE extname = 'plpython3u';
SELECT * FROM pg_extension WHERE extname LIKE 'plpython%';
SELECT * FROM pg_available_extensions WHERE name LIKE 'plpython3u%';

CREATE EXTENSION plpython3u;
SELECT version();

CREATE LANGUAGE plpython3u
SELECT * FROM pg_language;
SELECT fuzzy_match_difflib('test', 'test'); -- returns 1.0
CREATE OR REPLACE FUNCTION fuzzy_match_difflib(str1 text, str2 text)
   RETURNS float AS $$
   from difflib import SequenceMatcher as SM
   return SM(None, str1, str2).ratio()
   $$ LANGUAGE plpython3u;
  
CREATE FUNCTION fuzzy_match(text, text, int) RETURNS boolean AS $$
   import fuzzywuzzy.process
   return fuzzy_match(text1, text2, threshold) 
$$ LANGUAGE plpython3u;

CREATE OR REPLACE FUNCTION print_python_env() RETURNS void AS $$
import sys
plpy.notice(sys.executable)
plpy.notice(sys.path)
$$ LANGUAGE plpython3u;
SELECT print_python_env();

CREATE OR REPLACE FUNCTION google_shopping_scraper(search_term text)  
RETURNS SETOF text AS $$

import requests
import re
from html2text import html2text

url = f'https://www.google.com/search?q={search_term}&tbm=shop'
headers = {"User-Agent": "Mozilla/5.0"}
res = requests.get(url, headers=headers)
html_text = res.text
plain_text = html2text(html_text)

lines = plain_text.split('\n')
result = []

for i in range(len(lines)):
    if "$" in lines[i] and " from " in lines[i]:
        line_parts = filter(None, [lines[i].strip(), lines[i+1].strip(), lines[i+2].strip()])
        line = ': '.join(line_parts)

        for j in range(i-1, -1, -1):
           if lines[j].startswith("["):
               index_of_line = j
               break
           
        joined_lines = ''.join(lines[index_of_line:])
        matches = re.findall(r'(?<!!)(\[(.*?)\])', joined_lines, re.DOTALL | re.IGNORECASE)
        for match in matches:
         if "![" not in match[1] and "compare prices" not in match[1].lower() and "cleanse" not in match[1].lower():
             line += ': ' + match[1]
             break
        result.append(line)
return result

$$ LANGUAGE plpython3u;
SELECT * FROM google_shopping_scraper('Patanjali Giloy Juice 500ml');
select currentinvoice.id as "id", currentinvoice.description as "description", 
currentinvoice.pack_size as "pack_size",
google_shopping_scraper(currentinvoice.description || ' ' || currentinvoice.pack_size) 
as "price",
LOCALTIMESTAMP as "datetime"
into public.google_shopping_prices
from 
"LatestInvoice-09262023" currentinvoice
select * from google_shopping_prices order by  description, pack_size, price

CREATE TYPE review AS (
    review_date text,
    review_stars text,
    review_name text,
    review_comment text
);

CREATE OR REPLACE FUNCTION patanjaliayurved_reviews_scraper(url text) 
RETURNS TABLE (review_date DATE, review_stars TEXT, review_name TEXT, review_comment TEXT) AS $$
import requests
from bs4 import BeautifulSoup
import random
from datetime import datetime

headers = {"User-Agent": "Mozilla/5.0"}
if not url:
   return []
res = requests.get(url, headers=headers)
html_text = res.text
soup = BeautifulSoup(html_text, 'html.parser')
review_wrappers = soup.find_all('div', {'class': 'review-wrap'})
names = ['Ajit', 'Kumar', 'Shyam', 'Ram', 'Laxman', 'Jesus', 'Kesari', 'Ramprasad', 'Tiger', 'Aamir']
result = []
for wrapper in review_wrappers:
   review = {'review_date': None, 'review_stars': None, 'review_name': None, 'review_comment': None}
   review_date = wrapper.find('div', {'class': 'review-header'}).find('div', {'class': 'review-top-right'}).find('span')
   review_stars_div = wrapper.find('div', {'class': 'review-header'}).find('div', {'class': 'review-mid'}).find('div', {'class': 'review-stars'}).find('div', {'class': 'ratingtars'}).find('div', {'class': 'review-rating-block'}).find('div', {'class': 'rating-block'})
   if review_stars_div:
   	i_elements = review_stars_div.find_all('i')
   	star_count = len(i_elements)
   	review['review_stars'] = star_count
   
   review_name_b = wrapper.find('div', {'class': 'review-header'}).find('div', {'class': 'review-top-right'}).find('b')
   if review_name_b:
       review_name = review_name_b.text.strip()
       if review_name == '':
          review_name = random.choice(names)
   else:
       review_name = random.choice(names)
       
   review_comment = wrapper.find('div', {'class': 'review-text'})
   if review_date:
   	date_str = review_date.text.strip().replace("at ", "")
   	date_obj = datetime.strptime(date_str, "%d-%m-%Y %I:%M %p")
   	formatted_date = date_obj.strftime("%m/%d/%Y")
   	review['review_date'] = formatted_date

   review['review_name'] = review_name
   if review_comment:
       review['review_comment'] = review_comment.text.strip()
   result.append(review)
return result
$$ LANGUAGE plpython3u;


INSERT INTO public.reviews (date_of_review, rating, name_of_customer, review)
SELECT 
 r.review_date, 
 r.review_stars, 
 r.review_name, 
 r.review_comment 
FROM "LatestInvoice-09262023_WithOtherInfo"
CROSS APPLY patanjaliayurved_reviews_scraper(
"LatestInvoice-09262023_WithOtherInfo"."patanjali-ayurved-url") AS r

select * from patanjaliayurved_reviews_scraper(
'https://www.patanjaliayurved.net/product/natural-personal-care/hair-care/hair-oil/patanjali-almond-hair-oil/540')

SELECT 
   SPLIT_PART('a|b|c', '|', 1) AS part1,
   SPLIT_PART('a|b|c', '|', 2) AS part2,
   SPLIT_PART('a|b|c', '|', 3) AS part3;


  
select count(distinct id) from google_shopping_prices order by  description, pack_size, price

delete from public.google_shopping_prices

