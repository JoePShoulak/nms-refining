import scrapy

attr_dict = {
    'input': 'data-ing',
    'input_count': 'data-ingn',
    'output_quantity': 'data-out',
    'process_name': 'data-recp',
    'process_speed': 'data-time'
}


def recipe_to_dict(recipe):
    attrib = recipe.css('li').attrib
    data = {'output': recipe.css('span.itemlink::text').get()}

    for key in attr_dict:
        temp = {key: attrib[attr_dict[key]]}
        data.update(temp)

    return data


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
