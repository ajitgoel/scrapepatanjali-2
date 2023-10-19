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

INSERT INTO public."LatestInvoice-09262023_WithOtherInfo"
SELECT * FROM public."LatestInvoice-09262023";


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