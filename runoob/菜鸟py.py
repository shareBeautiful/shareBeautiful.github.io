import requests
import json
import time
from parsel import Selector


class Runoob():
    __num = 1

    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (compatible; Baiduspider/2.0;+http://www.baidu.com/search/spider.html)'
        }
        self.file = open('data.js', 'a', encoding='utf-8')
        self.file.write('var data = [ \n')

    def get_html(self, url):
        try:
            res = requests.get(url, headers=self.headers)
            return res.content.decode('utf-8')
        except Exception as e:
            print(e)

    def parse_html(self, html):
        doc = Selector(text=html)
        table = doc.xpath('//*[@id="content"]/table')
        trs = table.xpath('.//tr')
        data = []
        root_url = 'http://www.runoob.com/jsref/'
        for (i, tr) in enumerate(trs):
            id = str(i)
            code = tr.xpath('.//td[1]/a/text()').extract_first()
            intro = tr.xpath('.//td[2]/text()').extract_first()
            link = tr.xpath('.//td[1]/a/@href').extract_first()
            if not code:
                continue
            data.append({
                'id': id,
                'code': code,
                'intro': intro.strip(),
                'link': root_url + link
            })
        res = dict()
        res['id'] = str(self.__num)
        res['title'] = ''.join(
            doc.xpath('//*[@id="content"]/h1//text()').extract()).strip()
        res['data'] = data
        self.__num = self.__num + 1
        return res

    def save_data(self, data):
        self.file.write(json.dumps(data, ensure_ascii=False, indent=4))
        self.file.write(',\n')
        self.file.flush()
        print(f'保存--\t {data.get("title")} \t--成功！')

    def run(self, url):
        html = self.get_html(url)
        data = self.parse_html(html)
        if data:
            self.save_data(data)


if __name__ == '__main__':
    urls = [
        'http://www.runoob.com/jsref/jsref-obj-global.html',  # 全局函数
        'http://www.runoob.com/jsref/jsref-obj-array.html',  # 数组对象
        'http://www.runoob.com/jsref/jsref-obj-string.html',  # 字符串对象
        'http://www.runoob.com/jsref/jsref-obj-math.html',  # 数学对象
        'http://www.runoob.com/jsref/jsref-obj-number.html',  # 数字对象
        'http://www.runoob.com/jsref/jsref-obj-boolean.html',  # 布尔对象
        'http://www.runoob.com/jsref/jsref-obj-date.html',  # 日期对象
        "https://www.runoob.com/jsref/obj-location.html",  # location属性
        "https://www.runoob.com/jsref/dom-obj-event.html", # 电脑事件
        # jQuery 方法
        'https://www.runoob.com/jquery/jquery-ref-selectors.html', # jq 选择器
        'http://www.runoob.com/jquery/jquery-ref-html.html',  # jquery html/css方法
        'http://www.runoob.com/jquery/jquery-ref-effects.html',  # jquery 效果方法
        'http://www.runoob.com/jquery/jquery-ref-traversing.html',  # jquery 遍历方法
        'https://www.runoob.com/jquery/jquery-ref-events.html',  # jq 事件
        'http://www.runoob.com/jquery/jquery-ref-misc.html',  # jquery 杂选方法
        'https://www.runoob.com/jquery/jquery-ref-prop.html',  # jquery 属性
        'https://www.runoob.com/jquery/jquery-ref-ajax.html'    # jq ajax 方法

    ]
    
    with open('./data.js', 'w') as f:
        f.write('')
        f.flush()
    ru = Runoob()
    for i in urls:
        ru.run(i)
    ru.file.write('\n];')
    ru.file.close()
    print('--- 爬取完成！！！ 即将推出...---')
    time.sleep(5)
