# -*- coding: utf-8 -*-

from scrapy.item import Item, Field

class ProductItem(Item):
    # fixed
    source		= Field()
    itemId 		= Field()
    name 		= Field()
    brand 		= Field()
    category	= Field()
    attr		= Field()
    # unfixed
    url			= Field()
    img 		= Field()
    relateSKU	= Field()
    tm_skuprice	= Field()
    # for sorting
    comment		= Field()
    price		= Field()
    tm_moonSellCount = Field()
    date		= Field()
    history		= Field()
    # for monitor spider
    surl        = Field()
    gid         = Field()
    main        = Field()


class TmCatItem(Item):
    cat = Field()