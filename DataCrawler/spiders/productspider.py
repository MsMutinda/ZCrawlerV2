import scrapy
from urllib.parse import urlencode

#  from scrapy.linkextractors import LinkExtractor
# from ..items import ProductscrawlerItem


# API_KEY = '0f606d9a-6020-4599-a260-b42566fb19cb'
API_KEY = '43806c69-3fae-4ccf-b28b-c8461be31f94'

def get_scrapeops_url(url):
    payload = {'api_key': API_KEY, 'url': url, 'bypass': 'cloudflare'}
    proxy_url = 'https://proxy.scrapeops.io/v1/?' + urlencode(payload)
    return proxy_url


class ProductSpider(scrapy.Spider):
    name = "productspider"

    def start_requests(self):
        start_urls = [
            'https://naivas.online/food-cupboard',
            'https://naivas.online/vegatable-cooking-oils',
            'https://naivas.online/health-and-wellness',
            'https://naivas.online/electronics',
            'https://naivas.online/cleaning',
            'https://naivas.online/naivas-liquor',
            'https://naivas.online/fresh-food',
            'https://naivas.online/kitchen-dining',
            'https://naivas.online/party',
            'https://naivas.online/pet',
        ]

        for url in start_urls:
            yield scrapy.Request(url=get_scrapeops_url(url), callback=self.parse_url)

    def parse_url(self, response):
        PRODUCT_DETAILS_SELECTOR = '.product-container'
        NAME_SELECTOR = 'h5 a::text'
        PRICE_SELECTOR = 'span.price::text'
        URL_SELECTOR = 'a::attr(href)'
        BRAND_URL = '.grid-hover-btn a::attr(href)'
        IMAGE_SELECTOR = '.product-thumbnail > a > img::attr(data-original)'

        for productdetail in response.css(PRODUCT_DETAILS_SELECTOR):
            name = productdetail.css(NAME_SELECTOR).extract_first()
            price = productdetail.css(PRICE_SELECTOR).extract_first().split(' ')[1]
            image = productdetail.css(IMAGE_SELECTOR).extract_first()
            category = productdetail.css(URL_SELECTOR).extract_first().split('/')[3].replace("-", " ")
            unit_text = name.split(" ")[-1]
            unit_int = name.split(" ")[-2]
            # unit_text = ''
            # unit_int = ''

            # visit the brand url to get brand
            brand = productdetail.css(BRAND_URL).extract_first()
            # brand = ''


            yield {
                'name': name,
                'price': price,
                'image': image,
                'category' : category,
                'unit_text': unit_text,
                'unit_int': unit_int,

                'brand': brand
                # 'alldetails': alldetails
            }





# class ProductSpider(scrapy.Spider):
#     name = 'productspider'
#     start_urls = [
#         'https://naivas.online/flour/',
#         'https://naivas.online/vegetable-cooking-oils',
#         'https://naivas.online/rice-and-cereals',
#         'https://naivas.online/fresh-milk',
#         'https://naivas.online/energy-drink',
#         # 'https://www.carrefour.ke/mafken/en/c/FKEN1701240',

#     ]

#     def parse(self, response):
#         # items = ProductscrawlerItem()

#         PRODUCT_DETAILS_SELECTOR = '.product-container'
        
#         NAME_SELECTOR = 'h5 a::text'
#         # PRICE_SELECTOR = 'span.price::text'
#         # URL_SELECTOR = 'a::attr(href)'
#         # # IMAGE_SELECTOR = 'link::attr(href)'
#         # IMAGE_SELECTOR = '.product-thumbnail a img::attr(src)'



#         for productdetail in response.css(PRODUCT_DETAILS_SELECTOR):
#             # alldetails = productdetail.css(NAME_SELECTOR).extract()

#             name = productdetail.css(NAME_SELECTOR).extract_first()
#             # price = productdetail.css(PRICE_SELECTOR).extract_first().split(' ')[1]
#             # image = productdetail.css(IMAGE_SELECTOR).extract_first()
#             # category = productdetail.css(URL_SELECTOR).extract_first().split('/')[3].replace("-", " ")
#             # unit_text = name.split(" ")[-1]
#             # unit_int = name.split(" ")[-2]
#             # unit_text = ''
#             # unit_int = ''
            
#             # brand = name.split(' ')[0]
#             # yield ProductscrawlerItem(name=name, price=price, category=category, unit_text=unit_text, unit_int=unit_int)

#             yield {
#                 'name': name,
#                 # 'price': price,
#                 # 'image': image,
#                 # 'category' : category,
#                 # 'unit_text': unit_text,
#                 # 'unit_int': unit_int,

#                 # 'brand': brand
#                 # 'alldetails': alldetails
#             }


        # BRAND_DETAILS_SELECTOR = '.product-right'
        # BRAND_SELECTOR = 'span::text'

        # for branddetail in response.css(BRAND_DETAILS_SELECTOR):
        #     brand = branddetail.css(BRAND_SELECTOR).extract_first()

        #     yield {
        #         'brand': brand,
        #     }

            # print(alldetails)
#         yield items