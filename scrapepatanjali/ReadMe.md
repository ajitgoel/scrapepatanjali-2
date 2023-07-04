Ubuntu: 
- sudo apt-get install python3 python3-dev python3-pip libxml2-dev libxslt1-dev zlib1g-dev libffi-dev libssl-dev
- cd ~/scrapepatanjali/scrapepatanjali/ && scrapy crawl PatanjaliBasedOnPatanjaliAyurvedWebsite --loglevel=INFO --logfile=log.txt
- cd ~/scrapepatanjali/scrapepatanjali/ && scrapy crawl PatanjaliBasedOnAmazonInWebsite --loglevel=INFO --logfile=log.txt

class: "."
id: "#"

source scrapy-env/bin/activate && cd scrapepatanjali && python3 scrapepatanjali/spiders/create_shopbase_import_file.py --loglevel=INFO --logfile=log.txt

Run example spider: 
- source scrapy-env/bin/activate && cd ~/temp/scrapepatanjali/scrapepatanjali/ && scrapy crawl example --loglevel=INFO --logfile=log.txt