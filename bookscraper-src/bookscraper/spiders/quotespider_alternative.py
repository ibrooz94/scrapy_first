import scrapy
from scrapy.http.response import Response
from typing import Optional

class QuotespiderSpider(scrapy.Spider):
    name = "quotealt"
    allowed_domains = ["quotes.toscrape.com"]
    start_urls = ["https://quotes.toscrape.com/js"]
    custom_settings = {
        "DOWNLOAD_HANDLERS": {
            "https": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
            "http": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
        },
        "CONCURRENT_REQUESTS": 90,
        "PLAYWRIGHT_MAX_PAGES_PER_CONTEXT": 150,
        "CLOSESPIDER_ITEMCOUNT": 1000,
        "PLAYWRIGHT_LAUNCH_OPTIONS":{
            "headless": True,
            "timeout": 90 * 1000
        }
    }


    def parse(self, response: Response, current_page: Optional[int] = None):

        self.logger.debug(f"CURRENT: {current_page}")
        for i in range(11):
            yield response.follow(
                url= response.urljoin(f'/js/page/{i}'),
                callback = self.parse_quote,
                meta={
                    "playwright": True,
                    "playwright_include_page": True,
                })

    async def parse_quote(self, response):
        page = response.meta["playwright_page"]
        await page.close()

        for quote in response.css('div.quote'):
            yield {
                'text': quote.css('span.text::text').get(),
                'author': quote.css('small.author::text').get(),
                'tags': quote.css('div.tags a.tag::text').get()
            }

