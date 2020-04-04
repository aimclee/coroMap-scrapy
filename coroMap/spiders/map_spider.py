import scrapy
from coroMap.items import CoromapItem # items.py에서 CoromapItem 클래스를 가져온다.
from selenium import webdriver 
from scrapy.selector import Selector # 형(type)을 맞춰주기 위해
from selenium.webdriver.common.keys import Keys # selenium의 send_keys 메소드를 활용하기 위함.
from selenium.webdriver.common.action_chains import ActionChains #ActionChains를 활용하기 위함.
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


class MapSpider(scrapy.Spider):
    name = 'address' #spider's name
    start_urls = [ #start url
        "https://maps.vnpost.vn/corona/#/app"
    ]
    
    def __init__(self):
        scrapy.Spider.__init__(self)
        self.driver = webdriver.Chrome("C:/Users/aimclee/chromedriver")
    
    def parse(self, response): # self -> instance, response : response from request
        '''
        title = response.css('title::text').extract()
        yield {"titletext":title}
        '''
        self.driver.get(response.url)
        self.driver.implicitly_wait(3)
        # path = self.driver.find_elements_by_tag_name('path') #리스트로 값을 받아온다.
        # addresses = Selector(text=path)
        path = self.driver.find_elements_by_css_selector(".leaflet-marker-icon svg")
        path = self.driver.find_elements_by_xpath('//*[@id="Capa_1"]')
        path = self.driver.find_elements(By.XPATH, '//*[@id="Capa_1"]')

        # selector = Selector(text=path)
        # addresses = selector
        
        #path를 하나하나 클릭하며 크롤링 진행
        for address in path:
            # address.send_keys(Keys.ENTER) #클릭이 안되는 문제가 생김
            address.click()
            # address.send_keys('\n')
            # ActionChains().move_to_element(address).click(address).perform()
            # https://stackoverflow.com/questions/53698033/how-to-click-on-an-element-through-selenium-actionchain-and-python
            # ActionChains(self.driver).click().perform()
            item = CoromapItem()
            item['address'] = response.css(".leaflet-popup-content div:nth-child(2)::text").extract() 
            self.driver.find_element_by_css_selector(".leaflet-popup-close-button").click()
            yield item
        

        # address = response.css(".leaflet-popup-content div:nth-child(2)").extract() # ::text - extract text from html element
        # yield {'addressText': address} # address를 key로 title을 value값으로 yield(return)한다.

# .leaflet-pane div : 확진자 
# path : 클릭의 대상 (by selenium)
# div .leaflet-marker-icon style = "z-index:-600" ; => 232개 나옴.
