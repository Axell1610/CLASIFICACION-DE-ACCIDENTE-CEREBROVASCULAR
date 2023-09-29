import scrapy
from scrapy.spider import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.exceptions import CloseSpider
from mercado.items import MercadoItem

class MercadoSpider(CrawlSpider):
	name = 'mercado'
	item_count = 0
	allowed_domain = ['www.mercadolibre.com.pe']
	start_urls = ['https://listado.mercadolibre.com.pe/laptops#D[A:laptops]']

	rules = {
		# Para cada item
		Rule(LinkExtractor(allow = (), restrict_xpaths = ('//li[@class="andes-pagination__button andes-pagination__button--next shops__pagination-button"]/a'))),
		Rule(LinkExtractor(allow =(), restrict_xpaths = ('//h2[@class="ui-search-item__title shops__item-title"]/a')),
							callback = 'parse_item', follow = False)
	}

	def parse_item(self, response):
		ml_item = MercadoItem()
		#info de producto
		ml_item['titulo'] = response.xpath('normalize-space(//h1[@class="ui-pdp-title"]/text()').extract_first()
		ml_item['modelo'] = response.xpath('normalize-space(/html/body/main/div/div/div[1]/div[1]/section[1]/div/section[1]/ul/li[1]/span)').extract()
		ml_item['marca'] = response.xpath('normalize-space(/html/body/main/div/div/div[1]/div[1]/section[1]/div/section[1]/ul/li[2]/span)').extract()
		ml_item['tecnologia'] = response.xpath('normalize-space(/html/body/main/div/div/div[1]/div[1]/section[1]/div/section[2]/ul/li[1]/span)').extract()
		ml_item['tipo'] = response.xpath('normalize-space(/html/body/main/div/div/div[1]/div[1]/section[1]/div/section[2]/ul/li[2]/span)').extract()
		ml_item['precio'] = response.xpath('normalize-space(//*[@id="ui-pdp-main-container"]/div[1]/div/div[1]/div[2]/div[3]/div[1]/div[1]/span[1]/span[3])').extract()
		ml_item['condicion'] = response.xpath('normalize-space(//*[@id="ui-pdp-main-container"]/div[1]/div/div[1]/div[2]/div[1]/div/div[1]/span').extract()
		ml_item['envio'] = response.xpath('normalize-space(//p[contains(@class, "shipping-method-title")]/text())').extract()
		ml_item['ubicacion'] = response.xpath('normalize-space(//p[contains(@class, "card-description")])').extract()
		ml_item['opiniones'] = response.xpath('normalize-space(//span[@class="review-summary-average"]/text())').extract()
		#imagenes del producto
		ml_item['image_urls'] = response.xpath('//figure[contains(@class, "gallery-image-container")]/a/img/@src').extract()
		ml_item['image_name'] = response.xpath('normalize-space(//h1[@class="item-title__primary "]/text())').extract_first()
		#info de la tienda o vendedor
		ml_item['vendedor_url'] = response.xpath('//*[contains(@class, "reputation-view-more")]/@href').extract()
		ml_item['tipo_vendedor'] = response.xpath('normalize-space(//p[contains(@class, "power-seller")]/text())').extract()
		ml_item['ventas_vendedor'] = response.xpath('normalize-space(//div[@class="feedback-title"]/text())').extract()
		self.item_count += 1
		if self.item_count > 5:
			raise CloseSpider('item_exceeded')
		yield ml_item
