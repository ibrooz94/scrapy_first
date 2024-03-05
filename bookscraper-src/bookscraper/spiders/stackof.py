from typing import Generator, Optional

from scrapy import Spider
from scrapy.http.response import Response


class BooksSpider(Spider):
    """Extract all books, save screenshots."""

    name = "stackof"
    custom_settings = {
        "TWISTED_REACTOR": "twisted.internet.asyncioreactor.AsyncioSelectorReactor",
        "DOWNLOAD_HANDLERS": {
            "https": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
            "http": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
        },
        "CONCURRENT_REQUESTS": 32,
        "PLAYWRIGHT_MAX_PAGES_PER_CONTEXT": 4,
        "CLOSESPIDER_ITEMCOUNT": 1,
        "PLAYWRIGHT_LAUNCH_OPTIONS":{
            "headless": False,
            "timeout": 90 * 1000,  # 90 seconds
        }
    }
    start_urls = ["http://books.toscrape.com"]

    def parse(self, response: Response, current_page: Optional[int] = None) -> Generator:
        page_count = response.css(".pager .current::text").re_first(r"Page \d+ of (\d+)")
        page_count = int(page_count)
        for page in range(2, page_count + 1):
            self.logger.debug(f"*** Page Details {page} - {page_count}")
            yield response.follow(f"/catalogue/page-{page}.html", cb_kwargs={"current_page": page}, callback=self.parse)

        current_page = current_page or 1
        books = response.css('article.product_pod a')
        for book in books[:3]:
            yield response.follow(
                book,
                callback=self.parse_book,
                meta={
                    "playwright": True,
                    "playwright_include_page": True,
                    "playwright_context": f"page-{current_page}",
                },
            )

    async def parse_book(self, response: Response) -> dict:
        page = response.meta["playwright_page"]
        await page.close()
        return {
            "url": response.url,
            "title": response.css("h1::text").get(),
            "price": response.css("p.price_color::text").get(),
            "breadcrumbs": response.css(".breadcrumb a::text").getall(),
        }