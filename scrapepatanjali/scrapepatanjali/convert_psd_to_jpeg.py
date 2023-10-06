from PIL import Image
import os
import logging
import sys
import uuid

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utilities import input_output_folder

def generate_unique_filename(base_name, output_folder):
    name, ext = os.path.splitext(base_name)
    counter = 1
    new_name = base_name
    while os.path.exists(os.path.join(output_folder, new_name)):
        new_name = f"{name}_{counter}{ext}"
        counter += 1
    return new_name

def generate_guid_filename(base_name, output_folder):
    name, ext = os.path.splitext(base_name)
    guid = uuid.uuid4().hex
    new_name = f"{name}_{guid}{ext}"
    while os.path.exists(os.path.join(output_folder, new_name)):
        guid = uuid.uuid4().hex
        new_name = f"{name}_{guid}{ext}"
    return new_name

def convert_psd_to_jpeg(psd_path, output_folder, quality=85):
    try:
        img = Image.open(psd_path)
        img = img.convert("RGB")

        jpeg_filename = os.path.splitext(os.path.basename(psd_path))[0] + ".jpg"
        jpeg_path = os.path.join(output_folder, jpeg_filename)

        if os.path.exists(jpeg_path):
            jpeg_filename = generate_guid_filename(jpeg_filename, output_folder)
            jpeg_path = os.path.join(output_folder, jpeg_filename)
        img.save(jpeg_path, "JPEG", quality=quality, optimize=True)
        logging.info(f"Converted {psd_path} to {jpeg_path}")
    except Exception as e:
        logging.error(f"Error converting {psd_path}: {e}")

def batch_convert(folder_path, output_folder, quality=85):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for root, dirs, files in os.walk(folder_path):
        for filename in files:
            if filename.lower().endswith(".psd"):
                psd_path = os.path.join(root, filename)
                convert_psd_to_jpeg(psd_path, output_folder, quality=quality)

if __name__ == "__main__":
    input_folder = f'{input_output_folder()}/files-received_from_patanjali_08142023'
    output_folder = f'{input_output_folder()}/converted_jpeg_files'
    jpeg_quality = 85
    batch_convert(input_folder, output_folder, quality=jpeg_quality)
