from webdriver_manager.chrome import ChromeDriverManager

from selenium import webdriver
from selenium.webdriver.chrome .service import  Service

from selenium.webdriver.chrome.options import Options

from selenium.webdriver.common.by import By 
import xlsxwriter
from datetime import datetime
from xlsxHandler import XlsxHandler
import copy

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

    options.add_argument('headless')

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





def init_generate():    
    driver = init_chrome()# ("https://javhd.today/pornstar/tanaka-nene/")
    # input("Pulsa ENTER para salir")

    # url = "https://javhd.today/pornstar/tanaka-nene/"
    # url = "https://www4.javhdporn.net/pornstar/nene-tanaka/"
    
    # driver.get(url)

    listaVideo = {}
    listaActress ={}

    linkActress = "https://www4.javhdporn.net/pornstar/kokoro-ayase/"
    linkMain = "https://www4.javhdporn.net/pornstars/"


    conter= 0
    conterMax = 10

    nameFileFull =  linkMain.split("/")
    act = ''
    for name in nameFileFull:
        if name != '':
            ant = act  
            act = name
    nameFile = f"{ant}-{act}-{conterMax}"
    print(nameFile)
    
    xlsxHand = XlsxHandler(nameFile)


    try:
        while linkMain != "" and conter<conterMax:

            driver.get(linkMain)
            
            linkSendAct = copy.copy(linkMain)

            actressIndex = driver.find_elements(By.CLASS_NAME, "star") 
            
            #save url to actr pages
            actressURL = []
            for a in actressIndex:
                print (a.text)
                actressSelector =    a.find_element(By.CSS_SELECTOR, 'a').get_attribute("href")
                actressURL.append(actressSelector)
            # print(actressIndex[0].text)

            navigation = driver.find_element(By.CLASS_NAME, 'pagination')
            buttonNavigate = navigation.find_elements(By.CSS_SELECTOR, 'a')
                    
            currentAnt = False
                    
            linkMain =''
            for b in buttonNavigate:
                    if currentAnt:
                        linkMain = b.get_attribute('href')
                        break
                    if b.get_attribute('class') =='current' and not currentAnt:
                        currentAnt = True
            print(linkMain)


            #for each actrURL iterat 
            for url in actressURL:
                driver.get(url)    
                
                # print(actressSelector)
                # print(actressSelector.text)
                
                linkActress = url # actressSelector.get_attribute("href")
                print("linkActress")
                print(linkActress)

                while linkActress != '':
                    driver.get(linkActress)

                    listaVideo ={}
                    listaActress = {}

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

                        url_thumb = video.find_element(By.CSS_SELECTOR,".loaded").get_attribute('data-lazy-src')
                        # print(url_thumb)
                        lActress = []

                        for a in actress:
                            lActress.append(a.get_attribute('title'))


                        listaVideo[code] = (name, url_thumb )
                        listaActress[code] = lActress
                        # print(code)
                        # print(name)
                        # print(lActress)
                        # print(thumb)
                    # print(listaVideo)
                    # print(listaActress)
                    # print (listaVideo)
                    #write the file
                    xlsxHand.writeExcel(listaVideo,listaActress,linkSendAct)
                    
                    navigation = driver.find_element(By.CLASS_NAME, 'pagination')
                    buttonNavigate = navigation.find_elements(By.CSS_SELECTOR, 'a')
                    
                    currentAnt = False
                    
                    linkActress =''
                    for b in buttonNavigate:
                            if currentAnt:
                                linkActress = b.get_attribute('href')
                                break
                            if b.get_attribute('class') =='current' and not currentAnt:
                                currentAnt = True
                    print(linkActress)
                    # break
            conter+=1


            # linkMain = ""
            print (linkMain)
            # conter+=1
            # if conter == 2: 
            #     break
    finally:
        xlsxHand.close()
    # exit
    #guardar info en xlsx
    driver.quit



if __name__ == '__main__':
    init_generate()






