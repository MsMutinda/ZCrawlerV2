import scrapy
#  from scrapy.linkextractors import LinkExtractor

from ..items import ProductscrawlerItem

class ProductSpider(scrapy.Spider):
    name = 'productspider'
    start_urls = [
        'https://naivas.online/'
    ]

    def parse(self, response):
        items = ProductscrawlerItem()

        PRODUCT_DETAILS_SELECTOR = '.product-container'
        NAME_SELECTOR = 'h5 a::text'
        PRICE_SELECTOR = 'span.price::text'
        URL_SELECTOR = 'a::attr(href)'
        # IMAGE_SELECTOR = 'link::attr(href)'
        IMAGE_SELECTOR = '.product-thumbnail a img::attr(src)'

        for productdetail in response.css(PRODUCT_DETAILS_SELECTOR):
            name = productdetail.css(NAME_SELECTOR).extract_first()
            price = productdetail.css(PRICE_SELECTOR).extract_first().split(' ')[1]
            image = productdetail.css(IMAGE_SELECTOR).extract_first()
            category = productdetail.css(URL_SELECTOR).extract_first().split('/')[3].replace("-", " ")
            unit_text = name.split(" ")[-1]
            unit_int = name.split(" ")[-2]
            # unit_text = ''
            # unit_int = ''
            
            brand = name.split(' ')[0]
            # yield ProductscrawlerItem(name=name, price=price, category=category, unit_text=unit_text, unit_int=unit_int)

            yield {
                'name': name,
                'price': price,
                'image': image,
                'category' : category,
                'unit_text': unit_text,
                'unit_int': unit_int,

                'brand': brand
            }


        # BRAND_DETAILS_SELECTOR = '.product-right'
        # BRAND_SELECTOR = 'span::text'

        # for branddetail in response.css(BRAND_DETAILS_SELECTOR):
        #     brand = branddetail.css(BRAND_SELECTOR).extract_first()

        #     yield {
        #         'brand': brand,
        #     }


#         yield items