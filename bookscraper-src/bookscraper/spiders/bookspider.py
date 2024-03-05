import scrapy
from scrapy.crawler import CrawlerProcess
from ..items import BookscraperItem


class BookSpider(scrapy.Spider):
    name = "bookspider"
    allowed_domains = ["books.toscrape.com"]
    start_urls = ["https://books.toscrape.com"]
    custom_settings = {
        # 'FEEDS': {'booksdata.json': {'format': 'json', 'overwrite': True }},
        'ITEM_PIPELINES': {'bookscraper.pipelines.BookscraperPipeline': 300}
        }

    def parse(self, response):
        books = response.css('article.product_pod')

        for book in books:
            detail_page = book.css('h3 a::attr(href)').get()

            if 'catalogue/' in detail_page:
                detail_page_url = response.urljoin(detail_page)
            else:
                detail_page_url = response.urljoin("/catalogue/" + detail_page)
            yield response.follow(detail_page_url, callback=self.parse_bookpage)

        next_page = response.css('li.next a::attr(href)').get()

        if next_page is not None:
            if 'catalogue/' in next_page:
                next_page_url = next_page
            else:
                next_page_url = "/catalogue/" + next_page

            yield response.follow(next_page_url, callback=self.parse)

    def parse_bookpage(self, response):
        result = BookscraperItem()

        result['url'] = response.url
        result['title'] = response.css('.product_main h1::text').get()
        result['price'] = response.css('.product_main .price_color::text').get()

        yield result

if __name__ == "__main__":
    process = CrawlerProcess()
    process.crawl(BookSpider)
    process.start()