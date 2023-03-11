# from scrapy.linkextractors import LinkExtractor
# from ..items import ProductscrawlerItem
from urllib.parse import parse_qs, quote, unquote, urlencode, urlparse
import scrapy

# API_KEY = '0f606d9a-6020-4599-a260-b42566fb19cb'
# API_KEY = '43806c69-3fae-4ccf-b28b-c8461be31f94'
# API_KEY = '7d36a9c2-bc49-4764-9518-916e664fcd89'
API_KEY = 'ec4a888c-2b01-4c68-afda-66207b0294e5'


def get_scrapeops_url(url):
    payload = {'api_key': API_KEY, 'bypass': 'cloudflare', 'url': url}
    proxy_url = 'https://proxy.scrapeops.io/v1/?' + urlencode(payload)
    return proxy_url


class ProductSpider(scrapy.Spider):
    name = "productspider"

    def start_requests(self):
        start_urls = [
            'https://naivas.online/food-cupboard',
            # 'https://naivas.online/vegatable-cooking-oils',
            'https://naivas.online/health-and-wellness',
            'https://naivas.online/electronics',
            # 'https://naivas.online/cleaning',
            'https://naivas.online/naivas-liquor',
            'https://naivas.online/fresh-food',
            # 'https://naivas.online/kitchen-dining',
        ]

        for url in start_urls:
            yield scrapy.Request(url=get_scrapeops_url(url), callback=self.parse_url)


    def parse_url(self, response):
        PRODUCT_DETAILS_SELECTOR = '.product-container'
        NAME_SELECTOR = 'h5 a::text'
        PRICE_SELECTOR = 'span.price::text'
        URL_SELECTOR = 'a::attr(href)'
        BRAND_URL_SELECTOR = '.grid-hover-btn a::attr(href)'
        IMAGE_SELECTOR = '.product-thumbnail > a > img::attr(data-original)'

        for productdetail in response.css(PRODUCT_DETAILS_SELECTOR):
            name = productdetail.css(NAME_SELECTOR).extract_first()
            price = productdetail.css(PRICE_SELECTOR).extract_first().split(' ')[1]
            image = productdetail.css(IMAGE_SELECTOR).extract_first()
            category = productdetail.css(URL_SELECTOR).extract_first().split('/')[3].replace("-", " ")
            unit_text = name.split(" ")[-1]
            unit_int = name.split(" ")[-2]

            # visit the brand url to get brand
            brandurl = productdetail.css(BRAND_URL_SELECTOR).extract_first()
            if brandurl:
                yield scrapy.Request(get_scrapeops_url(brandurl), callback=self.parse_brandurl)
                # brand = self.parse_brandurl(get_scrapeops_url(brandurl))


            yield {
                'name': name,
                'price': price,
                'image': image,
                'category' : category,
                'unit_text': unit_text,
                'unit_int': unit_int,
                # 'brand': brand
            }


        # follow next page with the yet-to-be-loaded products on the website
        this_url = unquote(response.request.url)
        parsed_url = urlparse(this_url)
        currenturl = parse_qs(parsed_url.query)['url'][0]

        for page in range(2, 11):
            if 'page=' in currenturl:
                currenturl = currenturl.split('?page')[0]

            next_page = currenturl + '?page=' + str(page)
            # next_page = quote(f'"{next_page}"')
            # next_page = f'https://.....?page={page}'

            if next_page:
                # yield response.follow(next_page, callback=self.parse_url)
                yield scrapy.Request(url=get_scrapeops_url(next_page), callback=self.parse_url)

    
    def parse_brandurl(self, response):
    # def parse_brandurl(self, response, brandurl):
        BRANDNAME_SELECTOR = '.product-attributes .product-manufacturer a span::text'
        brand = response.css(BRANDNAME_SELECTOR).extract_first()
        print('brand is: \n', brand)
        
        yield {'brand' : brand}