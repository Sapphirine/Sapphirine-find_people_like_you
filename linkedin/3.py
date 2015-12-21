from scrapy.contrib.spiders.init import InitSpider
from scrapy.http import Request, FormRequest
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import Rule
from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from linkedpy.items import *
#The library is too complicated so had to import all
class LinkedPySpider(InitSpider):
    name = 'LinkedPy'
    allowed_domains = ['linkedin.com']
    login_page = 'https://www.linkedin.com/uas/login'
    start_urls = ["https://www.linkedin.com"]
    def init_request(self):
        return Request(url=self.login_page, callback=self.login)
    def login(self, response):
        return FormRequest.from_response(response,
                    formdata={'session_key': 'mailbox', 'session_password': 'password'},
                callback=self.check_login_response)
    def check_login_response(self, response):
    if "Sign Out" in response.body:
        self.log("Start")
        return self.initialized()
    else:
        self.log("Stop")
    def parse(self, response):
    hxs = HtmlXPathSelector(response)
    self.log("Succeed")
    sites = hxs.select('style="top: 24px; min-width: 974px; background-image: url("https://static.licdn.com/scds/common/u/images/apps/profile/topcard_backgrounds/texture_default_blue.jpg"); background-size: auto; background-position: 50% 0px;"')
    #Steve Wozniak's webpage css to start
    items = []
    for site in sites:
        item = LinkedpyItem()
        item['title'] = site.select('h2/a/text()').extract()
        item['people'] = site.select('h2/a/prof').extract()
        item['business'] = site.select('h2/a/business()').extract()
        item['school'] = site.select('h2/a/graduation').extract
        item['link'] = site.select('h2/a/@href').extract()
        items.append(item)
    return items