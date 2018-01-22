# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.contrib.pipeline.images import FilesPipeline
from scrapy.exceptions import DropItem
from scrapy.http import Request


class DownloadPipeline(FilesPipeline):

    def file_path(self, request, response=None, info=None):
        item = request.meta['item']
        return item['file_path']

    def get_media_requests(self, item, info):
        for file_url in item['file_urls']:
            yield Request(file_url, meta={'item': item})

    def item_completed(self, results, item, info):
        file_paths = [x['path'] for ok, x in results if ok]
        if not file_paths:
            raise DropItem("Item contains no files")
        return item
