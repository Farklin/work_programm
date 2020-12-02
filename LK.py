import requests
from bs4 import BeautifulSoup 
import time 
import openpyxl
import csv



class LK_Command: 

    # логин и пароль, авторизация 
    def __init__(self, login, password): 
        pass
        # self.login = login
        # self.password = password
    
        # session = requests.Session()
        # url = 'http://an.rem-mach.ru/login.php'
        # dann = dict(user_login = self.login, user_password = self.password)
        # session.get(url)
        # session.post(url, dann)

        # self.session = session


    def set_site_url(self):
        con = self.session.get("http://an.rem-mach.ru/edit_site_tab_url.php?site_id=" + self.number)
        html = BeautifulSoup(con.content, "html.parser")
        site_url = html.select('#site_url')
        self.site_url = site_url[0].get('value')
    
    def set_regions(self): 
        con = self.session.get("http://an.rem-mach.ru/keys_list.php?site_id=" + self.number)
        html = BeautifulSoup(con.content, "html.parser")
        self.regions = html.select('nobr>input')

    def set_price(self): 
        con = self.session.get("http://an.rem-mach.ru/edit_site_tab_budget.php?site_id=" + self.number)
        html = BeautifulSoup(con.content, "html.parser")
        price= html.select('#site_budg_seo')
        self.price = price[0].get('value')

    def downland_TR(self, number):
        self.number = number
        self.set_site_url() 
        self.set_regions() 
        
        regions = [] 
        for region in self.regions: 
            regions.append(region.get('value')) 

        self.regions_tr = regions 

        for region in regions: 
            con = self.session.get("http://an.rem-mach.ru/keys_list.php?download_list=1&site_id="+self.number+"&site_stat_region="+str(region))
            f=open(r''+ self.site_url + str(region) + '.csv',"wb")
            f.write(con.content)
            f.close()
    
    def analization_TR(self):
        
        compilation = [] 
        with open('waycon.ru615' +'.csv', newline='') as File:  
            reader = csv.reader(File)
            for val, row in enumerate(reader):
                if val != 0: 
                    position = row[0].split(';')[3]
                    if position == '-': 
                        position = int(0)
                    
                    url = row[0].split(';')[4]
                    phraze = row[0].split(';')[0]
                    compilation.append({
                        'url': url,
                        'position': position, 
                        'phraze': phraze, 
                    })

        self.compilation = compilation 


    # Вывести все слова в топе 
    def get_praze_top(self):
        for row in self.compilation: 
           if int(row['position']) > 10: 
               print(row['phraze']) 

    def group_phraze_in_url(self):
        mas = []
        group_phraze = [] 
        
        for row in self.compilation:
            url = row['url']
            for row_2 in self.compilation: 
                if url == row_2['url']: 
                    group_phraze.append(row_2['phraze'])
            mas.append({'url': url, 'keys': group_phraze })       
            group_phraze=[] 
        
        print(mas)

user = LK_Command('Jilcov', 'Jilcov435333')
#user.downland_TR('5202')
user.analization_TR()   
user.group_phraze_in_url()