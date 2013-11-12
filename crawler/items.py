# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field

class newsItem(Item):
    titular = Field()
    bajada = Field()
    noticia = Field()
    link = Field()
    medio = Field()

class productItem(Item):
    marca = Field()
    modelo = Field()
    descripcion = Field()
    precio = Field()
    sku = Field()
    
    categorias = Field()
    
    tienda = Field()
    link = Field()
    
    actualizacion = Field()