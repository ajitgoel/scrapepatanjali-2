import scrapy
import csv
from collections import OrderedDict
import os
import logging
from ..utilities import trim_and_add_hyphens, input_output_folder

log_file = os.path.join(input_output_folder(), 
                        'ScrapePatanjaliBasedOnAmazonIn-error.log')
logging.basicConfig(
    filename=log_file,
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s'
)

class ScrapePatanjaliBasedOnAmazonInSpider(scrapy.Spider):
    name = "ScrapePatanjaliBasedOnAmazonIn"

    def start_requests(self):
        urls = [
            "https://www.amazon.in/stores/page/B531389F-CB73-4E5B-AB7D-23F147C4D3D1?ingress=2&amp;visitId=d57f9c60-0950-46a6-aed4-6b01b1e8f39a&amp;ref_=ast_bln",
            "https://www.amazon.in/stores/page/06C69A72-DE48-41E7-9171-FC6CF9AB36C0?ingress=2&amp;visitId=d57f9c60-0950-46a6-aed4-6b01b1e8f39a&amp;ref_=ast_bln",
            "https://www.amazon.in/stores/page/02E279EA-C387-4C93-B998-76492BFF2AD2?ingress=2&amp;visitId=d57f9c60-0950-46a6-aed4-6b01b1e8f39a&amp;ref_=ast_bln",
            "https://www.amazon.in/stores/page/17886851-FCEF-4490-ABCD-9E1088364180?ingress=2&amp;visitId=d57f9c60-0950-46a6-aed4-6b01b1e8f39a&amp;ref_=ast_bln",
            "https://www.amazon.in/stores/page/DE23F8EF-E3B1-4EC3-BF57-927FE8ED859F?ingress=2&amp;visitId=d57f9c60-0950-46a6-aed4-6b01b1e8f39a&amp;ref_=ast_bln",
            "https://www.amazon.in/stores/page/63B63173-026F-44CB-B486-07CB6A15EFCC?ingress=2&amp;visitId=d57f9c60-0950-46a6-aed4-6b01b1e8f39a&amp;ref_=ast_bln",
            "https://www.amazon.in/stores/page/0EEA2A67-2EBE-484B-A258-34D1F8D3BDEF?ingress=2&amp;visitId=d57f9c60-0950-46a6-aed4-6b01b1e8f39a&amp;ref_=ast_bln",
            "https://www.amazon.in/stores/page/ABD8759E-9AE3-4D9E-BF28-3F02155482B3?ingress=2&amp;visitId=d57f9c60-0950-46a6-aed4-6b01b1e8f39a&amp;ref_=ast_bln",
            "https://www.amazon.in/stores/page/0CA42D0F-B4DC-4EEC-8AF4-12F5AF68F968?ingress=2&amp;visitId=d57f9c60-0950-46a6-aed4-6b01b1e8f39a&amp;ref_=ast_bln",
            "https://www.amazon.in/stores/page/4DD9A958-2095-431B-B7FE-9AD36D247D2F?ingress=2&amp;visitId=d57f9c60-0950-46a6-aed4-6b01b1e8f39a&amp;ref_=ast_bln",
            "https://www.amazon.in/stores/page/8223ABF0-8921-47E9-AC04-720EEA1B0B11?ingress=2&amp;visitId=d57f9c60-0950-46a6-aed4-6b01b1e8f39a&amp;ref_=ast_bln",
            "https://www.amazon.in/stores/page/BD6AEF8D-BD66-4101-9D45-41066FB2F7DE?ingress=2&amp;visitId=d57f9c60-0950-46a6-aed4-6b01b1e8f39a&amp;ref_=ast_bln",
            "https://www.amazon.in/stores/page/837D9ED9-0D22-46AF-B82C-8DB6BF6BC2BD?ingress=2&amp;visitId=d57f9c60-0950-46a6-aed4-6b01b1e8f39a&amp;ref_=ast_bln",
            "https://www.amazon.in/stores/page/D9937BE0-7052-4418-9BAC-C5795B4828AE?ingress=2&amp;visitId=d57f9c60-0950-46a6-aed4-6b01b1e8f39a&amp;ref_=ast_bln",
            "https://www.amazon.in/stores/page/3CA37A80-1D48-4944-B5BB-49D89F6B6A83?ingress=2&amp;visitId=d57f9c60-0950-46a6-aed4-6b01b1e8f39a&amp;ref_=ast_bln"
        ]
        for url in urls:
            yield scrapy.Request(url, callback=self.parse_parent)

    # def parse_LHS_Menu(self, response):
    #     child_urls = response.css('div.categorytree>ul>li>ul>li>a::attr(href)').getall()
    #     for child_url in child_urls:
    #         yield scrapy.Request(url=response.urljoin(child_url), callback=self.parse_child)

    def parse_parent(self, response):
        child_urls = response.css(
            "ul[class*=ProductGrid__grid__] li div a::attr(href)"
        ).getall()
        self.logger.info("child_urls: " + " ".join(child_urls))
        for child_url in child_urls:
            yield scrapy.Request(
                url=child_url, callback=self.parse_child
            )

    def parse_child(self, response):
        lastbreadcrumb = response.css(
                "div.block-breadcrumb>ul.breadcrumb>li.active::text"
            ).get()
        heading = response.css("div.product-detail-section>h3::text").get()
        productInformation = ''.join(response.css("div.product-information>div>p>font::text").get())
        benefits = ''.join(response.css("div#collapse1>div>div>font::text").getall())
        ingredients = ''.join(response.css("div#collapse2>div>div>font::text").getall())
        howToUse = ''.join(response.css("div#collapse3>div>div>font::text").getall())
        otherProductInfo = ''.join(response.css("div#collapse4>div.panel-body>font::text").getall())
        variants = ", ".join(response.css(
                "div.col-md-5.col-sm-4.details-custom>div>select>option::text"
            ).getall())
        
        productImage = response.css("#product-main::attr(src)").get()
        
        lastbreadcrumb = lastbreadcrumb if lastbreadcrumb is not None else ""
        heading = heading if heading is not None else ""
        benefits_string = benefits if benefits is not None else ""
        ingredients_string = ingredients if ingredients is not None else ""
        howToUse_string = howToUse if howToUse is not None else ""
        otherProductInfo_string=otherProductInfo if otherProductInfo is not None else ""
        variants = variants if variants is not None else ""
        productImage = productImage if productImage is not None else ""

        data = {
            "url": response.url,
            #'breadcrumb1': response.css('div.block-breadcrumb>ul.breadcrumb>li:nth-child(2)>a::text').get(),
            #'breadcrumb2': response.css('div.block-breadcrumb>ul.breadcrumb>li:nth-child(3)>a::text').get(),
            "lastbreadcrumb": lastbreadcrumb,
            "heading": heading,
            "product-information": "<b>Product Information</b>"
            + productInformation
            + "\n<b>Benefits</b>"
            + benefits_string
            + "\n<b>Ingredients</b>"
            + ingredients_string
            + "\n<b>How to use</b>"
            + howToUse_string
            + "\n<b>Other Product Info</b>"
            + otherProductInfo_string,
            "variants": variants,
            "product-image": productImage,
        }
        if productImage != "":
            yield scrapy.Request(productImage, callback=self.parse_image)

        output_file_path = f'{input_output_folder()}/patanjali-ayurved-scrape-based-on-amazon-in.csv'
        with open(output_file_path, "a", newline="", 
                  encoding="utf-8") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=data.keys())
            writer.writerow(data)

    def parse_image(self, response):
        file_name = response.url.split('/')[-1]
        folder_path = 'images'
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
        file_path = os.path.join(folder_path, file_name)
        with open(file_path, 'wb') as f:
            f.write(response.body)