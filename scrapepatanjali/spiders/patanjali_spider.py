import scrapy
import csv
from collections import OrderedDict
import os

class PatanjaliSpider(scrapy.Spider):
    name = "patanjali"

    def start_requests(self):
        urls = [
            "https://www.patanjaliayurved.net/category/digestives/138",
            "https://www.patanjaliayurved.net/category/health-and-wellness/139",
            "https://www.patanjaliayurved.net/category/chyawanprash/150",
            "https://www.patanjaliayurved.net/category/badam-pak/151",
            "https://www.patanjaliayurved.net/category/ghee/152",
            "https://www.patanjaliayurved.net/category/honey/153",
            "https://www.patanjaliayurved.net/category/health-drinks/177",
            "https://www.patanjaliayurved.net/category/fruit-beverage/184",
            "https://www.patanjaliayurved.net/category/diet-food/218",
            "https://www.patanjaliayurved.net/category/biscuits-and-cookies/3",
            "https://www.patanjaliayurved.net/category/spices/11",
            "https://www.patanjaliayurved.net/category/candy/12",
            "https://www.patanjaliayurved.net/category/herbal-tea/13",
            "https://www.patanjaliayurved.net/category/jam/14",
            "https://www.patanjaliayurved.net/category/murabba/15",
            "https://www.patanjaliayurved.net/category/dalia-poha-and-vermicelli/130",
            "https://www.patanjaliayurved.net/category/flours/131",
            "https://www.patanjaliayurved.net/category/sauces-and-pickles/132",
            "https://www.patanjaliayurved.net/category/corn-flakes/183",
            "https://www.patanjaliayurved.net/category/dal-pulses/185",
            "https://www.patanjaliayurved.net/category/rice/186",
            "https://www.patanjaliayurved.net/category/noodles/190",
            "https://www.patanjaliayurved.net/category/oats/191",
            "https://www.patanjaliayurved.net/category/papad/192",
            "https://www.patanjaliayurved.net/category/namkeen/193",
            "https://www.patanjaliayurved.net/category/edible-oil/217",
            "https://www.patanjaliayurved.net/category/sweets/222",
            "https://www.patanjaliayurved.net/category/salt/230",
            "https://www.patanjaliayurved.net/category/sugar/231",
            "https://www.patanjaliayurved.net/category/dried-fruits-nuts/234",
            "https://www.patanjaliayurved.net/category/breakfast-cereals/243",
            "https://www.patanjaliayurved.net/category/kwath/5",
            "https://www.patanjaliayurved.net/category/vati/16",
            "https://www.patanjaliayurved.net/category/bhasma/17",
            "https://www.patanjaliayurved.net/category/churna/18",
            "https://www.patanjaliayurved.net/category/guggul/19",
            "https://www.patanjaliayurved.net/category/parpati-ras/134",
            "https://www.patanjaliayurved.net/category/pishti/135",
            "https://www.patanjaliayurved.net/category/arishta/178",
            "https://www.patanjaliayurved.net/category/asava/179",
            "https://www.patanjaliayurved.net/category/syrup/181",
            "https://www.patanjaliayurved.net/category/godhan-ark/199",
            "https://www.patanjaliayurved.net/category/oil/208",
            "https://www.patanjaliayurved.net/category/lep/210",
            "https://www.patanjaliayurved.net/category/balm-inhaler/211",
            "https://www.patanjaliayurved.net/category/eye-ear-oral-care/248",
            "https://www.patanjaliayurved.net/category/agarbatti-and-dhoops/7",
            "https://www.patanjaliayurved.net/category/hawan-samagri/200",
            "https://www.patanjaliayurved.net/category/pooja-essentials/220",
            "https://www.patanjaliayurved.net/category/dishwash-bar-and-gel/221",
            "https://www.patanjaliayurved.net/category/body-care/25",
            "https://www.patanjaliayurved.net/category/eye-care/137",
            "https://www.patanjaliayurved.net/category/shishu-care/207",
            "https://www.patanjaliayurved.net/category/swadeshi-samridhi-card/224",
            "https://www.patanjaliayurved.net/category/nutrition/233",
            "https://www.patanjaliayurved.net/category/nutrition-bar/235",
            "https://www.patanjaliayurved.net/category/spiritual/237",
            "https://www.patanjaliayurved.net/category/home/239",
            "https://www.patanjaliayurved.net/category/accessories/240",
            "https://www.patanjaliayurved.net/category/sports-wear/241",
            "https://www.patanjaliayurved.net/category/women-ethnic/242",
            "https://www.patanjaliayurved.net/category/copperware/245",
            "https://www.patanjaliayurved.net/category/dairy-frozen-items/247",
        ]
        for url in urls:
            #self.logger.info("url: " + url)
            yield scrapy.Request(url, callback=self.parse_parent)

    # def parse_LHS_Menu(self, response):
    #     child_urls = response.css('div.categorytree>ul>li>ul>li>a::attr(href)').getall()
    #     for child_url in child_urls:
    #         yield scrapy.Request(url=response.urljoin(child_url), callback=self.parse_child)

    def parse_parent(self, response):
        child_urls = response.css(
            "div#gridview>div>article>figure>a.figure-href::attr(href)"
        ).getall()
        #self.logger.info("child_urls: " + " ".join(child_urls))
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

        with open("patanjali-ayurved-scrape.csv", "a", newline="", encoding="utf-8") as csvfile:
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