import scrapy
import time

class recipeSpider(scrapy.Spider):
    name = 'recipe'
    #allowed_domains = ['recipe.cc']
    start_urls = ['https://icook.tw/categories/104']

    def parse(self, response):
        target = response.xpath('//a[@class = "browse-recipe-link"]')
        print(target)
        for tag in target:
            print(tag)
            ticks = time.time()
            title = tag.xpath('.//span[contains(@class, "browse-recipe-name")]/text()').extract_first()
            href = tag.xpath('.//@href').extract_first()
           # yield{
           #     'title': title,
           #     'href': href
           # }
            yield response.follow(url=href, meta={'Title': title[11:-1], 'sequence': ticks}, callback=self.parse_content)
        a_next = response.xpath('//a[contains(@rel, "next")]/@href').extract_first()
        if a_next:
            #a_next = 'https://icook.tw' + a_next
            yield response.follow(a_next, callback=self.parse)



    def parse_content(self, response):
        title = response.meta['Title']
        x = response.meta['sequence']
        ingredients = response.xpath('//div[@class="ingredient"]')
        for ingredient in ingredients:
            name = ingredient.xpath('.//a[@class="ingredient-search"]/text()').extract_first()
            unit = ingredient.xpath('.//div[@class="ingredient-unit"]/text()').extract_first()
            if response.url and title and name and unit:
                yield{
                    'Title': title,
                    'Ingredient': name,
                    'Unit': unit,
                    'sequence':x,
                }

