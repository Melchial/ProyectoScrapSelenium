from webdriver_manager.chrome import ChromeDriverManager

from selenium import webdriver
from selenium.webdriver.chrome .service import  Service

from selenium.webdriver.chrome.options import Options

from selenium.webdriver.common.by import By 
import xlsxwriter
from datetime import datetime

def init_chrome():
    
    ruta = ChromeDriverManager(path='./chromedriver').install()

    options = Options() #instancia de options
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
    options.add_argument(f"user-agent={user_agent}")
    options.add_argument("--window-size=1000,1000")
    options.add_argument("--start-maximized")    
    options.add_argument("--disable-web-security")
    options.add_argument("--disable-extensions") 
    options.add_argument("--disable-notifications") 
    options.add_argument("--ignore-certificate-errors") 
    options.add_argument("--no-sandbox") 
    options.add_argument("--log-level=3")
    options.add_argument("--allow-running-insecure-content") 
    options.add_argument("--no-default-browser-check") 
    options.add_argument("--no-first-rub") 
    options.add_argument("--no-proxy-server") 
    options.add_argument("--disable-blink-features=AutomationControlled") 

    exp_opt = [
        'enable-automation',
        'ignore-certificate-errors',
        'enable-logging'
    ]

    options.add_experimental_option("excludeSwitches", exp_opt)

    prefs = {
        "profile.default_content_setting_values.notifications" : 2,
        "intl.accept_languages" : ["es-ES", "es"],
        "credentials_enable_service": False
    }

    options.add_experimental_option("prefs", prefs)

    s = Service(ruta)


    driver = webdriver.Chrome(service=s, options=options)
    return driver
if __name__ == '__main__':
    driver = init_chrome()# ("https://javhd.today/pornstar/tanaka-nene/")
    # input("Pulsa ENTER para salir")

    # url = "https://javhd.today/pornstar/tanaka-nene/"
    # url = "https://www4.javhdporn.net/pornstar/nene-tanaka/"
    
    # driver.get(url)

    listaVideo = {}
    listaActress ={}

    linkNext = "https://www4.javhdporn.net/pornstar/kokoro-ayase/"
    
    while linkNext != '':
        driver.get(linkNext)

        nombre_video = driver.find_elements(By.CLASS_NAME, "loop-video") 
        # print(nombre_video)
        for video in nombre_video:
            # titulo = video.find_element(By.CSS_SELECTOR,"span.video-title" )
            
            codename = video.find_element(By.CLASS_NAME,"entry-header").text#.split(" ")
            # titulo = video.find_element(By.CLASS_NAME,"entry-header").text.split(" ")[1]
            # thumb = video.find_element(By.CLASS_NAME,"video-preview").get_attribute("data-mediabook")
            
            actress = video.find_elements(By.CLASS_NAME,"byline")#.split(" ")
            code = codename.split(" ")[0]
            name = codename.removeprefix(f"{code} ")

            lActress = []

            for a in actress:
                lActress.append(a.get_attribute('title'))

            listaVideo[code] = name
            listaActress[code] = lActress
            # print(code)
            # print(name)
            # print(lActress)
            # print(thumb)
        # print(listaVideo)
        # print(listaActress)
        
        navigation = driver.find_element(By.CLASS_NAME, 'pagination')
        buttonNavigate = navigation.find_elements(By.CSS_SELECTOR, 'a')
        
        currentAnt = False
        
        linkNext =''
        for b in buttonNavigate:
                if currentAnt:
                    linkNext = b.get_attribute('href')
                    break
                if b.get_attribute('class') =='current' and not currentAnt:
                    currentAnt = True
                
                

        print(linkNext)

    
    # exit
    #guardar info en xlsx


    workbook = xlsxwriter.Workbook("Data_Vid.xlsx")
    worksheetTitulo = workbook.add_worksheet("ListaMaster")
    worksheetActress = workbook.add_worksheet("ListaActr")

    row = 0
    column = 0

    # worksheet.write("A1", "Hello world")
    date_format = workbook.add_format()
    date_format.set_num_format('dd/mm/yyyy hh:mm AM/PM')

    worksheetTitulo.write(row,column,'Codigo')
    column+=1
    worksheetTitulo.write(row,column,'Titulo')

    row += 1

    for f in listaVideo:
        
        column = 0
        worksheetTitulo.write (row,column,f)
        column +=1
        worksheetTitulo.write (row,column,listaVideo[f])
        
        row +=1

    row = 0
    column = 0
    worksheetActress.write(row,column,'Codigo')
    column+=1
    worksheetActress.write(row,column,'Titulo')

    row += 1
    for f in listaActress:
        
        for a in listaActress[f]:
            column = 0
            worksheetActress.write (row,column,f)
            column +=1
            worksheetActress.write (row,column,a)
            row +=1

        # row +=1

    workbook.close()




    driver.quit









