import requests
from bs4 import BeautifulSoup as bs

''' Класс страница основные атрибуты url, title, description,  keywords ''' 
class Page: 


    def __init__(self, url, title='None', description='None', keywords = 'None', keys=[]): 
        self.url = url
        self.title = title 
        self.description = description 
        self.keywords = keywords 
        user_agent = {'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 5.1; hu-HU; rv:1.7.8) Gecko/20050511 Firefox/1.0.4'}

        self.req = requests.get(self.url,headers=user_agent)
        self.keys = keys
        # вхождение ключевых слов 
        self.entry_key = ''


    # найти meta на старнице
    def get_meta(self): 


        html = bs(self.req.content, 'html.parser')

        self.title = html.select('title')[0].text

        metas = html.select('meta') 

        for meta in metas: 
            if meta.get('name') == 'description' or meta.get('name') == 'Description' or meta.get('name') == 'DESCRIPTION': 
                self.description = meta.get('content')
                break
            else: 
                self.description = 'нету описания'

        for meta in metas: 
            if meta.get('name') == 'keywords' or meta.get('name') == 'Keywords' or meta.get('name') == 'KEYWORDS': 
                self.keywords = meta.get('content')
                break 
            else: 
                self.keywords = 'нету ключевого слова'

    #найти h1 
    def get_h1(self): 
        html = bs(self.req.content, 'html.parser')
        self.h1 = html.select('h1')[0].text
        #print (f"{self.url} {self.h1}")

    # найти заголвоки h2 и вхождения в них 
    def get_h2(self, phraza=''): 
        if phraza != '': 
            html = bs(self.req.content, 'html.parser')
            self.h2 = html.select('h2')
            for h2 in self.h2:
                if h2.text.find(phraza) != -1: 
                    print (f"{self.url} {h2}")
        else: 
            html = bs(self.req.content, 'html.parser')
            self.h2 = html.select('h2')
            for h2 in self.h2:
                print (f"{self.url} {h2}")

    #найти элементы на странице
    def search_element(self, tag_search_elem): 
        self.found_element =  []

        html = bs(self.req.content, 'html.parser')
        self.found_element = html.select(tag_search_elem)  

    # вывод элементов найденых на странице 
    def print_search_element(self): 
        for elem in self.found_element: 
            print(elem)

   # найти alt на странице 
    def alt(self):
        print("ALT изображений----------------------: ")
        self.search_element('img')
        for image in self.found_element: 
            if image.get('src').find('https:/') == -1 and image.get('src').find('http:/') == -1: 
                url = 'http://'+self.url.split('/')[2]

                if image.get("alt") != '': 
                    print(f'{url}{image.get("src")} ALT картинки: {image.get("alt")}')
                else:
                    print(f'{url}{image.get("src")} у картинки нету alt')

            else:
                if image.get("alt") != '': 
                    print(f'{image.get("src")} ALT картинки: {image.get("alt")}')
                else:
                    print(f'{image.get("src")} у картинки нету alt')

    def title_entry_key(self ): 
        pass 
        # mas_title_split = self.title.split(' ')
        # mas_description_split = self.title.split(' ')


        # mas_key_split = []
        # for key in self.keys: 
        #     for word in key.split(' '): 
        #         if word not in mas_key_split: 
        #             mas_key_split.append(word)
    
        # for key_word in mas_key_split: 
        #     if key_word in mas_title_split: 
        #         pass
        #     else: 
        #         self.entry_key += 'title: ' + key_word + '\n'

        #     if key_word in mas_description_split: 
        #         pass
        #     else: 
        #         self.entry_key += 'description: ' + key_word  + '\n'


        
