import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
import selenium.webdriver.support.expected_conditions as EC
from time import sleep
from datetime import date


#################################################################################################################################################################################

options = Options()
options.add_experimental_option("detach", True)

navegador = webdriver.Chrome(ChromeDriverManager().install(), options=options)
navegador.get("https://scholar.google.com.br/")
sleep(5)
navegador.find_element(By.XPATH, '//*[@id="gs_hdr_tsi"]' ).send_keys('"coifa" AND ("motor foguete" OR "foguetemodelismo" OR "missilismo") AND ("coeficiente de arrasto" OR "força de arrasto" OR "força de sustentação" OR "coeficiente de sustentação") AND ("CFD" OR "Computational fluid dynamics" OR "Computer fluid dynamics" OR "Fluidodinâmica computacional")')
sleep(3)
navegador.find_element(By.XPATH, '//*[@id="gs_hdr_tsb"]' ).click()

sleep(50)

numero_de_resultados = navegador.find_element(By.XPATH, '//*[@id="gs_ab_md"]/div').text
print("\n")
print(numero_de_resultados)
print("\n")


#resultado = navegador.find_element(By.XPATH, '//*[@id="xjg4xek6VJUJ"]').text

#print(resultado)

navegador.execute_script("arguments[0].setAttribute('class', 'gs_cb_gen gs_in_cb')", WebDriverWait(navegador, 20).until(EC.presence_of_element_located((By.XPATH, '//*[@id="gs_bdy_sb_in"]/ul[4]/li[2]/a'))))
navegador.execute_script("arguments[0].setAttribute('aria-checked', 'false')", WebDriverWait(navegador, 20).until(EC.presence_of_element_located((By.XPATH, '//*[@id="gs_bdy_sb_in"]/ul[4]/li[2]/a'))))
navegador.execute_script("arguments[0].setAttribute('data-s', '0')", WebDriverWait(navegador, 20).until(EC.presence_of_element_located((By.XPATH, '//*[@id="gs_bdy_sb_in"]/ul[4]/li[2]/a'))))


link = navegador.find_element(By.XPATH, '//*[@id="gs_bdy_sb_in"]/ul[4]/li[2]/a').get_attribute('href') 
navegador.get(link)
sleep(2)


sleep(5)
print(navegador.current_url)
link_splited = navegador.current_url.split('as_vis=1')

numero_de_resultados_2 = navegador.find_element(By.XPATH, '//*[@id="gs_ab_md"]/div').text
print("Esse é o número de resultados\n")
print(numero_de_resultados_2.split(" ")[1])
print("\n")

numero_de_artigos = navegador.find_elements(By.CLASS_NAME, 'gs_or')
print("esse é o numero de artigos:")
print(len(numero_de_artigos))
print("\n")


loops = int(int(numero_de_resultados_2.split(" ")[1])/10) 

print("\n")
print(loops)
print("\n")


j = 1
lista_aux = []
lista=[]
elemento = True

while(elemento):

    for i in (range(10)):
        print(i)
        string = str(i+1)

        try:
            teste = navegador.find_element(By.XPATH, '/html/body/div/div[10]/div[2]/div[3]/div[2]/div[' + string + "]/div[1]/div").get_attribute('class')

    
            if (teste == 'gs_ggsd'):
                titulo = navegador.find_element(By.XPATH, '/html/body/div/div[10]/div[2]/div[3]/div[2]/div[' + string + ']/div[2]/h3/a').text
                texto_completo = navegador.find_element(By.XPATH, '/html/body/div/div[10]/div[2]/div[3]/div[2]/div[' + string + ']/div[2]/h3/a').get_attribute('href')
            else:
                titulo = navegador.find_element(By.XPATH, '/html/body/div/div[10]/div[2]/div[3]/div[2]/div[' + string + ']/div/h3/a').text
                texto_completo = navegador.find_element(By.XPATH, '/html/body/div/div[10]/div[2]/div[3]/div[2]/div[' + string + ']/div/h3/a').get_attribute('href')
    

            lista_aux.append(titulo)
            lista_aux.append(texto_completo)

            lista.append(lista_aux)

            lista_aux = []
            
            print(titulo)
            print(texto_completo)
            print("\n")

        except:
            print("deu erro")
            elemento = False


    print("passei aqui")
    print(link)
    print("\n")

    print("esse é o j")
    print(j)
    
    next_page = link_splited[0] + 'start=' + str((j)*10) + link_splited[1] + '&as_vis=1'

    print(next_page)
    
    navegador.get(next_page)

    print("PASSEI AQUI")
    j = j + 1

print(lista)

import xlsxwriter     
      
book = xlsxwriter.Workbook('C:\\Users\\rafae\\Downloads\\Google Scholar.xlsx')     
sheet = book.add_worksheet()  
   

for i in range(len(lista)):
    sheet.write(i, 0, lista[i][0])
    sheet.write(i, 1, lista[i][1])

book.close()