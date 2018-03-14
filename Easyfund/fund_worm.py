import requests as rq
from bs4 import BeautifulSoup  as bs
from requests.exceptions import MissingSchema
from fund_info import fund_info as fi


# 天天基金网基金爬虫

class parse_fund(object):

    def __init__(self, code):
        self.code = code

    #  根据基金代码生成url

    def get_url(self, code):
        url = 'http://fund.eastmoney.com/%s.html?spm=search' % code
        return url

    # 根据url获取指定网页

    def get_soup(self, url):
        session = rq.Session()
        session.trust_env = False

        try:

            response = session.get(url)
            response.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}

            return bs(response.content, 'html.parser', from_encoding='utf-8')

        except MissingSchema:
            print
            'invalid url %s' % (url)
        except Exception as e:
            print(e)

    # 开始解析

    def start_parse(self):
        # 基金信息实例
        fund_info = fi()
        # 网页url
        url = self.get_url(self.code)
        # 网页实例
        page = self.get_soup(url)

        # 基金名称

        if page('div', class_='fundDetail-tit').__len__() > 0:
            fund_name = page('div', class_='fundDetail-tit')[0]
            fund_info.name = fund_name.get_text()
            print(fund_name)

            # 基金信息
            fund_info_item = page('div', class_='dataOfFund')
            # 基金涨跌信息
            fund_zd = fund_info_item[0]('dl', class_='floatleft fundZdf')
            spans = fund_zd[0].span['class']
            if 'ui-color-red' in spans:
                fund_z = fund_zd[0](id='gz_gszze')[0].text
            else:
                fund_z = '-' + fund_zd[0](id='gz_gszze')[0].text

            fund_d = fund_zd[0](id='gz_gszzl')[0].text
            print(fund_z, fund_d)
            print(fund_info.name)
            fund_info.set_raise_and_per(fund_z, fund_d)
            print(fund_info.rise_fall())

            # 基金走势图
            # <div class="estimatedchart hasLoading"> <img src="http://j4.dfcfw.com/charts/pic6/000254.png" alt="">   </div>
            picurl = page('div', class_='estimatedchart hasLoading')[0].img.get('src')
            fund_info.pic = picurl
            print(picurl)
            return fund_info
        else:
            fund_info.name = '不存在的基金'
            return fund_info



