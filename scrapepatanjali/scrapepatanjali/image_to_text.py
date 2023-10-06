import requests
from PIL import Image
from io import BytesIO
import pytesseract
import sys

# Check if URLs are provided as command-line arguments
if len(sys.argv) < 2:
    print("Usage: python image_to_text.py <image_url1> <image_url2> ...")
    sys.exit(1)

# Loop through each URL provided as a command-line argument
for url in sys.argv[1:]:
    try:
        # Fetch the image from the URL
        response = requests.get(url)
        response.raise_for_status()
        image = Image.open(BytesIO(response.content))

        # Perform OCR using Tesseract
        extracted_text = pytesseract.image_to_string(image)

        # Print the extracted text for this URL
        print(f"Text extracted from {url}:\n{extracted_text}\n")

    except requests.exceptions.RequestException as e:
        print(f"Error fetching the image from {url}: {e}\n")
    except Exception as e:
        print(f"Error processing {url}: {e}\n")

