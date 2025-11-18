from scrapy.http import HtmlResponse


def extract_html_title(scrapy_response):
    if not isinstance(scrapy_response, HtmlResponse):
        raise TypeError()
    title = scrapy_response.xpath('//title/text()').get()
    return title.strip() if title else None

