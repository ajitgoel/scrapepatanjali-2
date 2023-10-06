import os
import pandas as pd
from tabula import read_pdf

# Set the input folder containing the PDF files
input_folder = '/home/ajitgoel/temp/scrapepatanjali/scrapepatanjali/scrapepatanjali/spiders/output/product_composition_08262023/'

# Get a list of all PDF files in the folder
pdf_files = [file for file in os.listdir(input_folder) if file.endswith('.PDF')]

# Initialize an empty list to store the extracted data
extracted_data = []

# Loop through each PDF file
for pdf_file in pdf_files:
    pdf_path = os.path.join(input_folder, pdf_file)
    
    print(f"PDF PATH{pdf_path}")
    # Read tables from the PDF file
    tables = read_pdf(pdf_path, pages='all', multiple_tables=True, pandas_options={'header': None})
    
    print(f"no of tables {len(tables)}")
    # Assuming the second column is at index 1 (0-based index)
    for table in tables:
        if len(table.columns) > 1:
            extracted_data.extend(table.iloc[:, 1].tolist())

# Convert the extracted data to a DataFrame
data_df = pd.DataFrame(extracted_data, columns=['Second_Column_Data'])

# Set the output CSV file path
output_csv = 'output.csv'

# Save the DataFrame to a CSV file
data_df.to_csv(output_csv, index=False)

print(f"Data extracted from {len(pdf_files)} PDF files and saved to {output_csv}")
