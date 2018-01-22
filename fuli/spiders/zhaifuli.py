# -*- coding: utf-8 -*-
import scrapy
from scrapy.selector import Selector
from ..items import FileItem
import re
import os


class ZhaifuliSpider(scrapy.Spider):
    name = "fuli"
    allowed_domains = ["yxpjwnet.com"]
    start_urls = ['http://yxpjwnet.com/zhaifuli',
                  'http://yxpjwnet.com/zhainanshe',
                  'http://yxpjwnet.com/xiurenwang',
                  'http://yxpjwnet.com/luyilu'
                  ]

    pattern_1 = re.compile('list_\d+_\d+.html$')
    pattern_2 = re.compile('\d{4}(_\d+)*.*html$')
    pattern_3 = re.compile('/(\w+)/\d{4}/\d{4}/\d+.html$')
    pattern_4 = re.compile('http://images.zhaofulipic.com:8818/allimg/(\d+)/.*-(\d+).jpg$')

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url, self.parse)

    def parse(self, response):
        for s in Selector(response=response).xpath('//a'):
            href = s.xpath('@href').extract_first()

            match1 = re.match(self.pattern_1, href)
            if match1:
                yield scrapy.Request(re.match('(http://.*/\w+/).*', response.url).group(1) + href, self.parse)

            match3 = re.match(self.pattern_3, href)
            if match3:
                title = s.xpath('@title').extract_first()
                root_dir = match3.group(1)
                if title:
                    yield scrapy.Request(
                        url=href if href.startswith('http://yxpjwnet.com') else 'http://yxpjwnet.com' + href,
                        meta={'title': title, 'root_dir': root_dir},
                        callback=self.parse_img)

    def parse_img(self, response):
        title = response.meta['title']
        root_dir = response.meta['root_dir']

        for s in Selector(response=response).xpath('//a'):
            href = s.xpath('@href').extract_first()
            match2 = re.match(self.pattern_2, href)
            if match2:
                yield scrapy.Request(url=re.match('(http://.*/\w+/(\d{4})/(\d{4})/).*', response.url).group(1) + href,
                                     meta={'title': title, 'root_dir': root_dir}, callback=self.parse_img)

        for s in Selector(response=response).xpath('//img'):
            src = s.xpath('@src').extract_first()

            match4 = re.match(self.pattern_4, src)
            if match4:
                item = FileItem()
                item['file_path'] = os.sep.join([root_dir, title, match4.group(2)]) + '.jpg'
                item['file_urls'] = [src, ]
                yield item
