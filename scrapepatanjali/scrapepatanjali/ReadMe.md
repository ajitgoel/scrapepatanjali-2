Ubuntu: 
- sudo apt-get install python3 python3-dev python3-pip libxml2-dev libxslt1-dev zlib1g-dev libffi-dev libssl-dev
- pip3 install scrapy
- cd ~/temp/scrapepatanjali/ && source scrapy-env/bin/activate && rm ~/temp/scrapepatanjali/scrapepatanjali/scrapepatanjali/spiders/output/patanjali-ayurved-scrape.csv && cd ~/temp/scrapepatanjali/scrapepatanjali/ && scrapy crawl patanjali

- source scrapy-env/bin/activate && cd scrapepatanjali && cd ~/scrapepatanjali/scrapepatanjali/ && scrapy crawl ScrapePatanjaliBasedOnAmazonIn

class: "."
id: "#"

source scrapy-env/bin/activate && python3 scrapepatanjali/scrapepatanjali/create_shopbase_import_file.py

Run example spider: 
- cd ~/temp/scrapepatanjali/ && source scrapy-env/bin/activate && cd ~/temp/scrapepatanjali/scrapepatanjali/ && scrapy crawl example