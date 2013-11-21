# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo
from myscrapy.export import ExportExcel

class TutorialPipeline(object):
    def process_item(self, item, spider):
        return item


class MongoPipeline(object):

	def process_item(self, item, spider):
		# print dict(item)
		conn = pymongo.Connection('127.0.0.1', 27017)
		conn['test']['cat'].save(dict(item))
		return item


class ExcelPipeline(object):

	def process_item(self, item, spider):
		ExportExcel( item )
		return item