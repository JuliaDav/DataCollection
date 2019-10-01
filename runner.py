from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from vacparcer import settings
from vacparcer.spiders.hhru import HhruSpider
from vacparcer.spiders.sjru import SjruSpider

if __name__ == '__main__':
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)
    process = CrawlerProcess(settings=crawler_settings)
    process.crawl(SjruSpider)
    process.crawl(HhruSpider)
    process.start()