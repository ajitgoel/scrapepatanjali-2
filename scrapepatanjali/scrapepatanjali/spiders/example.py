import scrapy


class ExampleSpider(scrapy.Spider):
    name = "example"
    allowed_domains = ["example.com"]
    start_urls = ["https://example.com"]

    def parse(self, response):
        h1 = response.css(
            "body>div>h1::text").get()
        self.logger.info("h1: " + h1)
