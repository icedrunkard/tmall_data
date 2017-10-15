# -*- coding: utf-8 -*-
"""
python version 3.4 64bit，windows7，2017/10/15更新

分析：销量等内容通过jsonp协议传输，Chrome浏览器F12抓包得出内容页网址为url2，需带cookie访问获得

step1:先访问主页面，建立对话，获取cookie
step2:通过已建立的对话访问内容页，获取数据
step3:分析数据

反爬机制：同一ip访问次数过多会弹出登陆页面
相应措施：使用ip代理，每一次请求会换一个新ip

"""
import codecs
from HEADERS import headers,proxies
import requests
from bs4 import BeautifulSoup
import time
import re
import json
from multiprocessing import Pool



def getTmallOnly(page):
    #url_test_ip="http://2017.ip138.com/ic.asp"
    
    u1="https://only.tmall.com/search.htm?spm=a1z10.3-b-s.w5001-15720337047.11.46f16db0OUW5Io&pageNo="
    u2="https://only.tmall.com/i/asynSearch.htm?mid=w-14571687321-0&pageNo="
    
    url1=u1+str(page)#主页面网址
    url2=u2+str(page)#jsonp请求页面网址
    headers['Referer']=url1
    
    
    #r_test=s.get(url_test_ip,proxies=proxies)   #测试代理ip是否变化
    #print(r_test.text)
    
    
    length=1
    while length>0:
        s=requests.session()
        r1=s.get(url1)#第一次访问，建立session
        r2=s.get(url2,headers=headers,proxies=proxies)#第二次访问，获取数据
        r1.close()
        r2.close()
        print('page',page,len(r2.text))
        if len(r2.text)>10000:#如果页面内容长，则爬取成功
            
            #with open('html/{}.html'.format(page),'w') as f:  #此处可将抓取的页面输出
                #f.write(r2.text)

            length=0#爬取成功则跳出循环
        else:
            time.sleep(0.2)# wait 0.2 second
            continue #爬取失败则重新爬取
    return r2.text

def get_info(page):

    html=getTmallOnly(page)

    soup=BeautifulSoup(html,'lxml')
    
    for piece in soup.find_all('div',class_=re.compile('item4line1'))[:15]:#每页15行
        
        for product in piece.find_all('dl',class_=re.compile('item')):#每行4项产品
            
            id=product.attrs['data-id'].replace('\\','').replace('"','')
            name=product.find('dd',class_=re.compile('detail')).get_text(strip=True)
            price=product.find('div',class_=re.compile('cprice-area')).get_text(strip=True)
            sale_num=product.find('div',class_=re.compile('sale-area')).get_text(strip=True)
            
            item={'page':page,#商品页数
                  'id':id,#商品id
                  'name':name,#商品名称
                  'price':price,#商品价格
                  'sale_num':sale_num,#商品销量
                      }
            item_str=json.dumps(item,ensure_ascii=False)


            with codecs.open('odata.json','a+','utf8') as f:#数据存储，json格式
                f.write(item_str)

                       
def main():
    
    pages=43#商品总页数
    pool=Pool(processes=8)#进程数
    
    for i in range(1,pages+1):
        pool.apply_async(get_info,(i,))
    
    pool.close()
    pool.join()
    
if __name__ == '__main__':
    main()




