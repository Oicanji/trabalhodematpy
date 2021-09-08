from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from time import sleep
from dotenv import load_dotenv

from bs4 import BeautifulSoup

import pandas as pd

import os

from send_email import SendEmail

load_dotenv()

EMAIL = os.environ['EMAIL']
PASSWORD = os.environ['PASSWORD']
DRIVEPATH = os.environ['DRIVEPATH']
THISPATH = os.environ["THISPATH"]

pathXlsx = THISPATH+'\\T1_5.xlsx';

objs = []

types = []

val = []

def getXlsx():
    chrome_options = Options()
    chrome_options.add_argument('--no-sandbox')
    chrome_options = webdriver.ChromeOptions()
    preferences = {"download.default_directory": THISPATH ,
                "directory_upgrade": True,
                "safebrowsing.enabled": True }
    chrome_options.add_experimental_option("prefs", preferences)

    navegador = webdriver.Chrome(chrome_options=chrome_options)

    navegador.get(DRIVEPATH)
    navegador.find_element_by_id("identifierId").send_keys(EMAIL)
    navegador.find_element_by_id("identifierNext").click()
    sleep(2)
    navegador.find_element_by_name("password").send_keys(PASSWORD)
    navegador.find_element_by_id("passwordNext").click()
    sleep(4)
    navegador.find_element_by_xpath('//*[@id=":4"]/div/c-wiz/div[2]/c-wiz/div[1]/c-wiz/div/c-wiz/div[1]/c-wiz/c-wiz/div/c-wiz/div').click()
    sleep(1)

    navegador.find_element_by_xpath('//*[@id="drive_main_page"]/div/div[3]/div/div/div[2]/div/div[2]/div/div[5]').click()
    sleep(3)
    o = navegador.find_elements_by_class_name('a-v-T')

    down = o[10]
    down.click()
    sleep(10)
    navegador.close()

def attObjs():
    xls = pd.read_excel(pathXlsx)
    paises = xls.iloc[:,0:1]
    i = 0
    while i < len(paises):
        nameString = paises.values[i]
        objs.append(nameString[0])
        i+=1

def attTypes():
    xls = pd.read_excel(pathXlsx)
    typess = xls.iloc[:,7:9]
    i = 0
    while i < len(typess):
        nameString = typess.values[i]
        types.append(nameString[0])
        i+=1
    types.pop(i-1)

def attValue():
    xls = pd.read_excel(pathXlsx)
    valores = xls.iloc[:,8:9]
    i = 0
    while i < len(valores):
        nameString = valores.values[i]
        val.append(nameString[0])
        i+=1
    val.pop(i-1)

def exist():   
    if( os.path.exists(pathXlsx) ):
        attValue()
        attObjs()
        attTypes()
        return True
    else:
        getXlsx()
        return False

def facDay(name:str):
    callback = exist()

    if(not callback):
        callback = exist()
    
    if name in objs and callback:
        xls = pd.read_excel(pathXlsx)
        prod_day = xls.iloc[:,1:5]
        i = 0
        while objs[i] != name:
            i += 1
        prod_day = prod_day.loc[i]
        product_day = []
        for item in prod_day:
            product_day.append(item)
        soma = []
        i = 0
        while i < len(product_day):
            soma.append(product_day[i]*val[i])
            i += 1
        total = 0
        for item in soma:
            total = total + item
        return total
            
    else:
        return('404: Country no has find')

def facMed(name:str):
    callback = exist()

    if name in types and callback:
        xls = pd.read_excel(pathXlsx)
        med_all = xls.iloc[:,1:5]
        i = 0
        while(name != med_all.columns.values[i]):
            i+=1
        i+=1
        med_all = xls.iloc[:,i:i+1]
        soma = 0;
        for items in med_all.values:
            soma = items[0] + soma
        return soma
    else:
        return('404: Fuel no has find')

fac = []
def results():
    fac.append((facDay("Brasil")))
    fac.append(facDay("EUA"))
    fac.append(facDay("Rússia"))
    fac.append(facDay("Arábia Saudita"))
    fac.append(facDay("Canadá"))

    med = facMed("Biodiesel")

    sleep(5)
    msg = f"""Boa noite! \n
    Aqui é Ignacio e tenho algumas informações:
    Media dos Combutiveis
    Brasil - {fac[0]}
    EUA - {fac[1]}
    Rússia - {fac[2]}
    Arábia Saudita - {fac[3]}
    Canadá - {fac[4]}

    A media do Biodisel de todos os paises é {med}.

    Github@Oicanji
    https://github.com/Oicanji/trabalhodematpy
    """
    
    SendEmail(msg)

results()