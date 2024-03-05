import scrapy
from scrapy.crawler import CrawlerProcess
from ..items import ChartascraperItem


class ChartaSpider(scrapy.Spider):
    name = "chartaspider"
    allowed_domains = ["www.charta-der-vielfalt.de"]
    start_urls = ["https://www.charta-der-vielfalt.de/en/diversity-charter-association/signatory-data-base/list/"]
    custom_settings = {
        'FEEDS': {'chartadata.xlsx': {'format': 'xlsx', 'overwrite': True }}, 
        'ITEM_PIPELINES': {'bookscraper.pipelines.ChartascraperPipeline': 300,
                           'bookscraper.pipelines.SaveToDatabasePipeline': 400
                           }
        }

    def parse(self, response):
        articles = response.css(".t_default-item .item-text")

        for article in articles:
            detail_page = article.css("h2 a::attr(href)").get()
            detail_page_url = response.urljoin(detail_page)

            yield response.follow(detail_page_url, callback=self.parse_detailpage)
        
        next_page = response.css('.paginate__item')[-1]
        next_page_url = next_page.css('a::attr(href)').get()

        if next_page_url:
            yield response.follow(next_page_url, callback=self.parse)


    def parse_detailpage(self, response):
        table_rows = response.css('table tr')
        address_div = response.xpath('//address/div')

        result = ChartascraperItem()

        result['url'] = response.url

        result['signatory'] = table_rows[0].css('td::text')[1].get() if len(table_rows) >= 1 else None
        result['federal_state'] = table_rows[1].css('td::text')[1].get() if len(table_rows) >= 2 else None
        result['organizational_size'] = table_rows[2].css('td::text')[1].get() if len(table_rows) >= 3 else None
        result['segment'] = table_rows[3].css('td::text')[1].get() if len(table_rows) >= 4 else None

        result['name'] = address_div[0].xpath('./div[1]/strong/text()').get() 
        result['position'] = address_div[0].xpath('./div[2]/text()').get()

        result['street'] = address_div[1].xpath('div[1]/text()').get()
        result['city'] = address_div[1].xpath('div[2]/text()').get()
        result['phone'] = address_div[1].xpath('div[3]/text()').get()
        result['email'] = address_div[1].xpath('div[4]/a').get()

        result['website'] = address_div[2].css('a::text').get() if len(address_div) >= 3 else None
        
        yield result

if __name__ == "__main__":
    process = CrawlerProcess()
    process.crawl(ChartaSpider)
    process.start()