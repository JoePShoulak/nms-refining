import scrapy


def recipe_to_dict(recipe):
    attrib = recipe.css('li').attrib
    return {
        'input': attrib['data-ing'],
        'input_count': attrib['data-ingn'],

        'output': recipe.css('span.itemlink::text').get(),
        'output_quantity': attrib['data-out'],

        'process_name': attrib['data-recp'],
        'process_speed': attrib['data-time'],
    }


def parse_recipes(response):
    recipes = response.css('div.mw-parser-output ul li[data-recp]')
    for recipe in recipes:
        yield recipe_to_dict(recipe)


class RawMaterialSpider(scrapy.Spider):
    name = 'raw_materials'
    start_urls = ['https://nomanssky.fandom.com/wiki/Category:Raw_Materials']

    def parse(self, response, **kwargs):
        for link in response.css('div.mw-category-group a::attr(href)'):
            yield response.follow(link.get(), callback=parse_recipes)
