Ubuntu: 
- sudo apt-get install python3 python3-dev python3-pip libxml2-dev libxslt1-dev zlib1g-dev libffi-dev libssl-dev
- pip3 install scrapy
- cd ~/temp/scrapepatanjali/ && source scrapy-env/bin/activate && rm ~/temp/scrapepatanjali/scrapepatanjali/scrapepatanjali/spiders/output/patanjali-ayurved-scrape.csv && cd ~/temp/scrapepatanjali/scrapepatanjali/ && scrapy crawl patanjali
- cd ~/temp/scrapepatanjali/ && source scrapy-env/bin/activate && cd ~/temp/scrapepatanjali/scrapepatanjali/ && scrapy crawl patanjali

- source scrapy-env/bin/activate && cd scrapepatanjali && cd ~/scrapepatanjali/scrapepatanjali/ && scrapy crawl ScrapePatanjaliBasedOnAmazonIn

class: "."
id: "#"

cd ~/temp/scrapepatanjali/ && source scrapy-env/bin/activate && python3 ~/temp/scrapepatanjali/scrapepatanjali/scrapepatanjali/create_shopbase_import_file.py
cd ~/temp/scrapepatanjali/ && source scrapy-env/bin/activate && python3 ~/temp/scrapepatanjali/scrapepatanjali/scrapepatanjali/convert_psd_to_jpeg.py
cd ~/temp/scrapepatanjali/ && source scrapy-env/bin/activate && python3 /home/ajitgoel/temp/scrapepatanjali/scrapepatanjali/scrapepatanjali/create_composition_file_from_pdf_files.py

Run example spider: 
- cd ~/temp/scrapepatanjali/ && source scrapy-env/bin/activate && cd ~/temp/scrapepatanjali/scrapepatanjali/ && scrapy crawl example

image to text:
cd ~/temp/scrapepatanjali/ && source scrapy-env/bin/activate && python3 ~/temp/scrapepatanjali/scrapepatanjali/scrapepatanjali/image_to_text.py https://pbs.twimg.com/media/F48itZWbcAAHk91?format=jpg&name=large https://pbs.twimg.com/media/F48i5LmbcAAlrMs?format=jpg&name=900x900

all_text = response.xpath('//div[@class="sg-col-inner"]//text()').getall()
cleaned_text = ' '.join(text.strip() for text in all_text if text.strip())
yield {'text': cleaned_text}