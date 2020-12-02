import eel
from LK_v2 import LK
from poisk_elementov import Page
import openpyxl 

@eel.expose
def get_function(number, flag_meta, flag_h1, flag_pages): 
    lk = LK(login = 'Jilcov', password = 'Jilcov435333')

    lk.autorization()

    lk.analization_report(number)

    reported = ''
    reported += '<br><br>' 
    reported += "<a target='_blank' href = 'http://an.rem-mach.ru/sites/" + number + "'>'http://an.rem-mach.ru/sites/" + number + "</a> <br>"
    for elem in lk.down_keys: 
        if not flag_pages: 
            if len(elem['keys']) > 0: 
                reported += '<br>Оптимизация страницы: ' + elem['url']  + '<br>'

                try: 
                    page = Page(elem['url'])
                except: 
                    pass 
            
                for el in lk.down_keys: 
                        for key in elem['keys']: 
                            if el['url'] == elem['url']: 
                                reported += key + '<br>'
        else: 
            reported += elem['url']  + '<br>' 


        if flag_meta: 
            try:
                page.get_meta()
                reported += '<br>'+'Meta:'
                reported += '<br>'+ '<strong>title:</strong> ' + page.title  + '<br>'
                reported += '<strong>description:</strong> ' + page.description + '<br>'
                reported += '<strong>keywords:</strong> ' + page.keywords + '<br>'
            except: 
                reported += '<br>'+'Meta:'
                reported += '<br>'+ 'не найдено'
        if flag_h1: 
            try: 
                page.get_h1()
                reported += '<br><br> Заголовок h1: ' + page.h1 + '<br><br>'
            except: 
                reported += '<br><br> Заголовок h1 не найден <br><br>'

    return reported


@eel.expose
def all(number):
    lk = LK(login = 'Jilcov', password = 'Jilcov435333')
    lk.autorization()
    lk.analization_report(number)

    mas_excel = [] 
    for elem in lk.down_keys: 
        
        if len(elem['keys']) > 0: 
            try: 
                page = Page(elem['url'])
            except: 
                pass 

        try:
            page.get_meta()
            title = page.title
            description = page.description
            keywords = page.keywords 
            url = page.url
            k = ''
            for key in elem['keys']: 
                k += key + ', ' 
        except: 
            title = ''
            description = ''
            keywords = '' 
            url = page.url
            k = ''
            for key in elem['keys']: 
                k += key + ', '
        mas_excel.append({ 'key': k, 'url': url, 'title': title, 'desc': description, 'keywords': keywords, })

    wb = openpyxl.Workbook()
    sheet = wb.active

    for row, product in enumerate(mas_excel): 
        for col, key in enumerate(product.keys()): 
            cell = sheet.cell(row=row+1, column=col+1) 
            cell.value = product[key]

    
    wb.save("Отчет meta.xlsx")
    return "Отчет готов" 

eel.init('web')
eel.start('main.html', size=(700, 700))

