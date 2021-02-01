import scrapy
from ..items import Chrono24Item
import pandas as pd
import requests
#from scrapy.http import HtmlResponse
from bs4 import BeautifulSoup

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'
}


BaseUrl = 'https://www.chrono24.com/'

class Chrono24SpiderSpider(scrapy.Spider):
    name = 'chrono24_spider'
    start_urls = ['https://www.chrono24.fr/rolex/index.htm'
                  'https://www.chrono24.com/patekphilippe/index.htm',
                  'https://www.chrono24.com/audemarspiguet/index.htm',
                  'https://www.chrono24.com/richardmille/index.htm']

    
    def parse(self, response):
        items=Chrono24Item()
        products_links=[]
        for products in response.css('.full-height'):
            link = BaseUrl + products.attrib['href']
            products_links.append(link)
            #name = products.css('.article-title::text').get().strip()
            #price = products.css('.article-price strong::text').get().strip()
            
        
        for link in products_links:
            r1 = requests.get(link, headers=headers)
            soup = BeautifulSoup(r1.content, 'lxml')
            
            try:
                name = soup.find('div', class_="media-flex-body").text.strip()
            except:
                name = ''
                
                
            try:
                priceChar = soup.find('span', class_="d-block").text.strip().replace('$','').replace(',','.')
                price = float(priceChar)
            except:
                priceChar = ''
                price = 'Price on request'
                # response2 = HtmlResponse(url=link) 
                    
                 #name = response2.css('h1::text').get()
            try:
                df = pd.read_html(r1.text)
                table = df[1]
            except Exception as e:
                print(e)
                continue  

                      # Select brand
            brand_table = table[table[0] == 'Brand'][1].values
            try:
                    brand = list(brand_table)[0]
            except:
                    brand = ''
                
                # Select Model
            model_table = table[table[0] == 'Model'][1].values
            try:
                    model = list(model_table)[0]
            except:
                    model = ''
                # Select Reference
            reference_table = table[table[0] == 'Reference number'][1].values
            try:
                    reference = list(reference_table)[0]
            except:
                    reference = ''
                
                # Select Material
            material_table = table[table[0] == 'Case material'][1].values
            try:
                    material = list(material_table)[0]
            except:
                    material = ''

                # Select  Condition
            condition_table = table[table[0] == 'Condition'][1].values
            try:
                    condition = list(condition_table)[0]
            except:
                    condition = ''

                #  Select Dial
            dial_table = table[table[0] == 'Dial'][1].values
            try:
                    dial = list(dial_table)[0]
            except:
                    dial = ''


            items['name']=name
            items['price']=price
            items['brand']=brand
            items['model']=model
            items['reference']=reference
            items['material']=material
            items['condition']=condition
            items['dial']=dial
        
            yield items
        
        next_page = response.css('.paging-next').attrib['href']
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)

 #brand       
#In [4]: response.css('tr:nth-child(3) .text-link').css('::text').get().strip()
#Out[4]: 'Rolex'
#case Material
#In [5]: response.css('tr:nth-child(8) td+ td').css('::text').get().strip()
#Out[5]: 'Rose gold'

#Reference
#In [15]: response.css('tr:nth-child(5) .text-link').css('::text').get().strip()
#Out[15]: '116285BBR'
