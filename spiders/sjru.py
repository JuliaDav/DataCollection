# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import HtmlResponse
from vacparcer.items import VacparcerItem

class SjruSpider(scrapy.Spider):
    name = 'sjru'
    allowed_domains = ['superjob.ru']
    start_urls = ['https://www.superjob.ru/vacancy/search/?keywords=python']

    def parse(self, response: HtmlResponse):
        next_page = response.xpath('//a[@class="icMQ_ _1_Cht _3ze9n f-test-button-dalshe f-test-link-dalshe"]/@href').extract_first()
        yield response.follow(next_page, callback=self.parse)
        vacancy = response.xpath(
            '//div[@class="_3syPg _1_bQo _2FJA4"]/div/a/@href').extract()
        for link in vacancy:
            yield response.follow(link, self.vacancy_parse)

    def vacancy_parse(self, response: HtmlResponse):
        item = VacparcerItem()
        item['name'] = response.xpath('//h1[@class="_3mfro rFbjy s1nFK _2JVkc"]/text()').extract_first()
        salary = response.xpath('//span[@class="_3mfro _2Wp8I ZON4b PlM3e _2JVkc"]//text()').extract()
        salary = ''.join(salary)
        item['salary'] = salary.replace('\xa0', '')
        yield item
