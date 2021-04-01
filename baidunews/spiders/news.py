import scrapy
from baidunews.items import  BaidunewsItem
from scrapy.http import  Request
import re

class NewsSpider(scrapy.Spider):
    name = 'news'
    allowed_domains = ['baidu.com']
    start_urls = ['http://news.baidu.com/widget?id=LocalNews&ajax=json']
    allid = ['LocalHouseNews', 'LocalNews', 'civilnews', 'InternationalNews', 'FinanceNews', 'EnterNews', 'SportNews',
             'AutoNews', 'HouseNews', 'InternetNews', 'InternetPlusNews', 'TechNews', 'EduNews', 'GameNews',
             'DiscoveryNews', 'HealthNews', 'LadyNews', 'SocialNews', 'MilitaryNews', 'PicWall']
    allurl = []
    for k in range(len(allid)):
        thisurl = "http://news.baidu.com/widget?id=" + allid[k] + "&ajax=json"
        allurl.append(thisurl)

    def parse(self, response):
        # print(self.allurl)
        # for j in range(len(self.allid)):
        #     thisid=self.allid[j]
        #     thisurl="http://news.baidu.com/widget?id="+thisid+"&ajax=json"
        #     yield Request  如果需要每几分钟爬一次 while TRUE   time.sleep(1000)

        for j in range(len(self.allurl)):
            try:
                url=self.allurl[j]
                print("开始爬取第"+str(j)+"个栏目块！")
                yield Request(url,callback=self.next)
            except Exception as err:
                print(err)
    def next(self,response):
        data=response.body.decode('UTF-8','ignore')
        pat='"url":"(.*?)"'
        pat2='"m_relate_url":"(.*?)"'
        url1=re.compile(pat,re.S).findall(data)
        url2=re.compile(pat2, re.S).findall(data)
        if len(url1)!=0 :
            url_target=url1
        if len(url2) != 0:
            url_target = url2
        for i in range(len(url_target)):
            # print(url_target[i])
            url_href=re.sub("\\\/", "/", url_target[i])
            # print(url_href)
            yield Request(url_href,callback=self.next2,dont_filter=True)
    def next2(self,response):
        item=BaidunewsItem()
        item["link"]=response.url
        item["title"]=response.xpath("/html/head/title/text()").extract()
        item["cotent"]=response.body
        yield item
