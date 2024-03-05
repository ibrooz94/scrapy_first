import scrapy
from scrapy_playwright.page import PageMethod
from scrapy.http.response import Response


class QuotespiderSpider(scrapy.Spider):
    name = "quotespider"
    allowed_domains = ["quotes.toscrape.com"]
    start_urls = ["https://quotes.toscrape.com/js"]
    custom_settings = {
        "DOWNLOAD_HANDLERS": {
            "https": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
            "http": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
        },
        "PLAYWRIGHT_LAUNCH_OPTIONS":{
            "headless": False,
        }
    }
    def start_requests(self):
        yield scrapy.Request(self.start_urls[0], meta=dict(
            playwright = True,
            playwright_include_page = True,
            playwright_page_methods = [
                PageMethod('wait_for_selector', 'div.quote')
            ],
            errback = self.errback
        ))

    async def parse(self, response: Response):
        page = response.meta["playwright_page"]
        await page.close()

        for quote in response.css('div.quote'):
            yield {
                'text': quote.css('span.text::text').get(),
                'author': quote.css('small.author::text').get(),
                'tags': quote.css('div.tags a.tag::text').get()
            }

        next_page = response.css('.next>a ::attr(href)').get()
        if next_page is not None:
            yield scrapy.Request(response.urljoin(next_page), meta=dict(
            playwright = True,
            playwright_include_page = True,
            playwright_page_methods = [
                PageMethod('wait_for_selector', 'div.quote')
            ]
        ))

    async def errback(self, failure):
        page = failure.request.meta["playwright_page"]
        await page.close()
