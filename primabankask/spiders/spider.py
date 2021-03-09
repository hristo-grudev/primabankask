import scrapy

from scrapy.loader import ItemLoader
from w3lib.html import remove_tags

from ..items import PrimabankaskItem
from itemloaders.processors import TakeFirst


class PrimabankaskSpider(scrapy.Spider):
	name = 'primabankask'
	start_urls = ['https://www.primabanka.sk/aktuality']

	def parse(self, response):
		post_links = response.xpath('//p[@class="description"]/a[@class="button-more"]/@href').getall()
		yield from response.follow_all(post_links, self.parse_post)

		next_page = response.xpath('//a[@class="nextPage"]/@href').getall()
		yield from response.follow_all(next_page, self.parse)

	def parse_post(self, response):
		title = response.xpath('//h1/text()').get()
		description = response.xpath('//div[@class="articles detail	"]/div//text()[normalize-space()]').getall()
		description = [remove_tags(p).strip() for p in description]
		description = ' '.join(description).strip()
		date = response.xpath('//p[@class="date"]/span/text()').get()

		item = ItemLoader(item=PrimabankaskItem(), response=response)
		item.default_output_processor = TakeFirst()
		item.add_value('title', title)
		item.add_value('description', description)
		item.add_value('date', date)

		return item.load_item()
