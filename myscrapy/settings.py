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

CONCURRENT_ITEMS = 500

ITEM_PIPELINES = [
	# 'myscrapy.pipelines.MongoPipeline',
	# 'myscrapy.pipelines.TutorialPipeline',
	# 'myscrapy.pipelines.ExcelPipeline',
	# 'myscrapy.pipelines.PrintPipeline',
	# 'myscrapy.pipelines.JsonLinesItemPipeline',
	# 'myscrapy.pipelines.JsonItemPipeline',
	'myscrapy.pipelines.MonitorPipeline',
]

# COOKIES_ENABLED = True

DOWNLOAD_DELAY = 0.01    # 10 ms of delay
DOWNLOAD_TIMEOUT = 30

LOG_LEVEL = 'INFO'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'myscrapy (+http://www.yourdomain.com)'
