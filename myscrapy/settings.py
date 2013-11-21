# Scrapy settings for myscrapy project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'myscrapy'

SPIDER_MODULES = ['myscrapy.spiders']
NEWSPIDER_MODULE = 'myscrapy.spiders'

ITEM_PIPELINES = [
	'myscrapy.pipelines.MongoPipeline',
]

# COOKIES_ENABLED = True

DOWNLOAD_DELAY = 0.25    # 250 ms of delay

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'myscrapy (+http://www.yourdomain.com)'
