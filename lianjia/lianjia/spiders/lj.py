import scrapy
from bs4 import BeautifulSoup
import json
from scrapy_redis.spiders import RedisSpider
from ..items import LianjiaItem
from copy import deepcopy
class LjSpider(RedisSpider):
    name = 'lj'
    allowed_domains = ['lianjia.com']
    #start_urls = ['https://wh.lianjia.com/sitemap/']
    redis_key = 'lj'

    def make_requests_from_url(self, url):
        return scrapy.Request(url)

    def parse(self, response):
        item = LianjiaItem()
        soup=BeautifulSoup(response.body,"html.parser")
        start_name = response.url.split('/')[2]
        urls_1=soup.find('div',attrs={'class':'city_nav'}).find_all('li')
        urls_1 = urls_1[::2]
        #找到所有城市
        # for url_1 in urls_1:
        #     #name = url_1.find('a').text    #城市名
        #     link_chs = 'https:'+url_1.find('a').get('href')    #链接
        #     yield scrapy.Request(link_chs,callback=self.parse)
        item['city'] = soup.find_all('p', attrs={"class": "title"})[1].text[:-3]
        #找到最下级的链接
        urls_2=soup.find('div', attrs={'class': 'div_con'}).find_all('li')
        for url_2 in urls_2:
            name2=url_2.find('a').text
            item['name']=name2
            urls_3 = url_2.find_all('dd')
            if len(urls_3) == 0:
                link_detail = 'https://' + start_name +url_2.find('a').get('href')
                yield scrapy.Request(link_detail, callback=self.all_items,meta={'item':deepcopy(item)})
            else:
                for url_3 in urls_3:
                    name2 = url_3.find('a').text
                    link_detail = 'https://' + start_name +url_3.find('a').get('href')
                    yield scrapy.Request(link_detail, callback=self.all_items,meta={'item':deepcopy(item)})
        pass



    def all_items(self,response):#从每个连接中提取我们要的信息
        item = response.meta['item']
        start_name = response.url.split('/')[2]
        soup=BeautifulSoup(response.body,"html.parser")
        all_fang=soup.find('ul',attrs={"class":"sellListContent"})#找到二手房区块
        if all_fang == None:
            return None
        else:
            all_fang=all_fang.find_all('li')
        for fang in all_fang:#提取信息
            item['des']=fang.find('div',attrs={"class":"title"}).find('a').text
            item['gz']=int(fang.find('div',attrs={"class":"followInfo"}).text.split(" / ")[0][:-3])
            html_link=fang.find('div',attrs={"class":"title"}).find('a').get('href')
            price=fang.find('div',attrs={"class":"priceInfo"})
            item['totalprice']=float(price.find('div',attrs={"class":"totalPrice totalPrice2"}).find('span').text)
            item['unitprice']=float(price.find('div',attrs={"class":"unitPrice"}).find('span').text[:-3].replace(",",""))
            jwd_url = 'https://{}/ershoufang/housestat?hid={}&rid={}'
            xqname=fang.find('div',attrs={"class":"positionInfo"}).find('a').text
            item['xqname']=xqname
            xqurl=fang.find('div',attrs={"class":"positionInfo"}).find('a').get('href')
            hid = html_link.split('/')[-1][:-5]
            rid = xqurl.split('/')[-2]
            jwd = jwd_url.format(start_name, hid, rid)
            yield scrapy.Request(jwd,callback=self.get_jwd,meta={'item':deepcopy(item),'html_link':deepcopy(html_link)})
        #提取下一页链接
        next_page = soup.find('div', attrs={"class": "contentBottom clear"}).find('div', attrs={
            "class": "page-box house-lst-page-box"})
        page_data = json.loads(next_page.get("page-data"))
        page_url = next_page.get("page-url")
        total_page = page_data.get("totalPage")
        now_page = page_data.get("curPage")
        if now_page<total_page:
            next_link="https://"+start_name+page_url.replace("{page}",str(now_page+1))
            yield scrapy.Request(next_link,callback=self.all_items,dont_filter=True,meta={'item':deepcopy(item)})

    def get_jwd(self,response):
        item = response.meta['item']
        html_link=response.meta['html_link']
        soup=json.loads(response.text)
        jwd=soup['data']['resblockPosition'].split(',')
        item['jd']=jwd[0]
        item['wd']=jwd[1]
        yield scrapy.Request(html_link, callback=self.every_html, meta={'item': deepcopy(item)})




    def every_html(self,response):#在每个二手房的详情页找数据
        item = response.meta['item']
        soup = BeautifulSoup(response.body, "html.parser")
        all_thing = soup.find('div', attrs={"class": "introContent"}).find('div', attrs={"class": "content"}).find_all(
            'li')
        jbsx={}
        for i in range(len(all_thing)):
            data = all_thing[i].span.string
            data2 = all_thing[i].text
            jbsx[data]=data2[4:]
        item['fwhx']=jbsx.get('房屋户型')
        item['szlc'] = jbsx.get('所在楼层')
        jzmj= jbsx.get('建筑面积')#有些无数据显示暂无数据
        if "暂无数据" in jzmj:
            item['jzmj']=None
        else:
            item['jzmj'] =float(jzmj[:-1])
        item['hxjg'] = jbsx.get('户型结构')
        tnmj= jbsx.get('套内面积',"暂无数据")
        if "暂无数据" in tnmj:
            item['tnmj']=None
        else:
            item['tnmj'] =float(tnmj[:-1])
        item['jzlx'] = jbsx.get('建筑类型')
        item['fwcx'] = jbsx.get('房屋朝向')
        item['jzjg'] = jbsx.get('建筑结构')
        item['zxqk'] = jbsx.get('装修情况')
        item['thbl'] = jbsx.get('梯户比例')
        item['pbdt'] = jbsx.get('配备电梯')
        item['yslx'] = jbsx.get('用水类型')
        item['ydlx'] = jbsx.get('用电类型')
        item['rqjg'] = jbsx.get('燃气价格')
            #item[thing[i]]=data[4:]
        hxfj=soup.find('div',attrs={"class":"layout-wrapper"})
        all_thing2 = soup.find('div', attrs={"class": "introContent"}).find('div', attrs={"class": "transaction"}).find_all(
            'li')
        jysx={}
        for j in range(len(all_thing2)-1):
            data = all_thing2[j].find_all('span')[0].text
            data2 = all_thing2[j].find_all('span')[1].text
            jysx[data]=data2
        item['gpsj'] = jysx.get('挂牌时间')
        item['jyqs'] = jysx.get('交易权属')
        item['scjy'] = jysx.get('上次交易')
        item['fwyt'] = jysx.get('房屋用途')
        item['fwnx'] = jysx.get('房屋年限')
        item['cqss'] = jysx.get('产权所属')
        item['dyxx'] = jysx.get('抵押信息').strip().replace(' ', '').replace('\n', '').replace('\r', '')
        item['fbbj'] = jysx.get('仿本备件')
        item['kt'] = 0.0
        item['ws'] = 0.0
        item['qt'] = 0.0
        if hxfj !=None:
            hxfj=hxfj.find_all('div',attrs={"class":"row"})
            for i in hxfj:#找出客厅、卧室、其它面积
                j = i.find_all("div")
                if j[0].text == "客厅":
                    item['kt'] = float(j[1].text[:-2])
                elif "卧室" in j[0].text:
                    item['ws'] += float(j[1].text[:-2])
                else:
                    item['qt'] += float(j[1].text[:-2])
            item['kt']=round(item['kt'],2)
            item['ws']=round(item['ws'],2)
            item['qt']=round(item['qt'],2)
        try:
            fyzp = soup.find('div', attrs={"class": "m-content"}).find('div', attrs={"class": "container"}).find('div',attrs={"class": "list"}).find_all('div')  # 找到二手房区块
            tu0=[]
            for k in fyzp:
                if k.find('img') == None:
                    continue
                tu = []
                tu.append(k.find('span').text)
                tu.append(k.find('img').get('alt'))
                tu.append(k.find('img').get('src'))
                tu0.append(tu)
            item['tu']=tu0
        except:
            item['tu'] =None
        yield item

