import os
import csv
from pdf2image import convert_from_path
import pytesseract

# Set the input folder containing the scanned PDFs
input_folder = '/home/ajitgoel/temp/scrapepatanjali/scrapepatanjali/scrapepatanjali/spiders/output/product_composition_08262023/'

# Set the output CSV file path
output_csv = 'convert_pdf_files_into_text_output.csv'

# Initialize an empty list to store extracted data
extracted_data = []

# Function to convert PDF to text using OCR
def pdf_to_text(pdf_path):
    images = convert_from_path(pdf_path)
    text = ""
    for img in images:
        text += pytesseract.image_to_string(img)
    return text.strip()

# Loop through each PDF file in the input folder
for pdf_file in os.listdir(input_folder):
    if pdf_file.endswith('.PDF'):
        pdf_path = os.path.join(input_folder, pdf_file)
        
        # Convert PDF to text using OCR
        text = pdf_to_text(pdf_path)
        
        # Append file name and extracted text to the list
        extracted_data.append([pdf_file, text])

# Write the extracted data to a CSV file
with open(output_csv, 'w', newline='', encoding='utf-8') as csv_file:
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(['File_Name', 'Extracted_Text'])
    csv_writer.writerows(extracted_data)

print(f"Text extracted from scanned PDFs and saved to {output_csv}")
