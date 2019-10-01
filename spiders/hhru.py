# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import HtmlResponse
from vacparcer.items import VacparcerItem

class HhruSpider(scrapy.Spider):
    name = 'hhru'
    allowed_domains = ['hh.ru']
    start_urls = ['https://hh.ru/search/vacancy?area=113&st=searchVacancy&text=python']

    def parse(self, response: HtmlResponse):
        next_page = response.css('a.HH-Pager-Controls-Next::attr(href)').extract_first()
        yield response.follow(next_page,callback=self.parse)
        vacancy = response.css(
                    'div.vacancy-serp div.vacancy-serp-item div.vacancy-serp-item__row_header a.bloko-link::attr(href)').extract()
        for link in vacancy:
            yield response.follow(link,self.vacancy_parse)


    def vacancy_parse (self, response: HtmlResponse):
        item = VacparcerItem()
        item['name'] = response.css('div.vacancy-title h1.header::text').extract_first()
        salary = response.css('div.vacancy-title p.vacancy-salary::text').extract_first()
        item['salary'] = salary.replace('\xa0','')

        yield item