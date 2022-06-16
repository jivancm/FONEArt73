
# Navega en el portal de FONE Artículo 73 de la Ley General de Contabilidad Gubernamental
# El primer paso es la obtención del sitio completo, de esa primer navegación 
# se obtiene el listado de los trimestres disponibles 

from logging import exception
from click import FileError
import requests
import socket
from bs4 import BeautifulSoup
from pathlib import Path
from urllib3.exceptions import (NewConnectionError, MaxRetryError)

gsDir = "./DWN"
gsTrim = ""
gsEdo = ""
gsArch = ""
gsUrl = ""
gsPath = ""
gsTrys = 0

def navegarEn(Url):
    global gsUrl
    if Url == gsUrl :
        gsTrys += 1
    else:
        gsUrl = Url
        gsTrys = 1
    try:
        page = requests.get(gsUrl)
    except (
            requests.exceptions.ConnectionError,
            socket.gaierror,
            NewConnectionError,
            MaxRetryError,
            TimeoutError
        ) as error:
            if gsTrys < 10:
                print('Reintentando descarga: [' + gsUrl + ']')
                return navegarEn(gsUrl)
            else:
                print("Se intentó " + gsTrys + " veces navegar en " + gsUrl + "sin éxito.")
                return BeautifulSoup("<html><body>No encontrado</body></html>", "html.parser")
    return  BeautifulSoup(page.content, "html.parser")

def descargarArchivo(page):
    global gsPath
    global gsTrys
    if(isinstance(page, str)):
        print("Descargando: " + page)
        Path(gsDir + '/' + gsEdo).mkdir(parents=True, exist_ok=True)
        nombre = gsDir + '/' + gsEdo + '/' + gsTrim + '-' + gsArch + '.zip'
        if(nombre == gsPath) : 
            gsTrys += 1
        else:
            gsTrys = 1
            gsPath = nombre
        if Path(gsPath).is_file() :
            print("Archivo Existente: " + nombre)
        try:
            archivo = requests.get(page)
        except (
            requests.exceptions.ConnectionError,
            socket.gaierror,
            NewConnectionError,
            MaxRetryError,
            TimeoutError
        ) as error:
            if gsTrys < 10:
                print('Reintentando descarga: [' + gsArch + ']')
                return descargarArchivo(page)
            else:
                print("Se intentó " + gsTrys + " veces descargar el archivo " + page + "sin éxito.")
                return False
        try:
            with open(nombre, 'wb') as f:
                f.write(archivo.content)
                print("Guardado: " + nombre)
                return True
        except FileError:
            return False
    else:
        for el in page.find_all('a') :
            txt = el.string
            if txt == 'Descargar archivo' :
                url = ('https://sep.gob.mx' if el['href'].startswith('/') else '') + el['href']
                return descargarArchivo(url)

def descargarEdo(pagEdo): 
    catalogos = [
                    "analíticodeplazas","catálogodetabuladores",
                    "catálogodepercepcionesydeducciones",
                    "movimientosdeplazas","plazasdocentes,administrativasydirectivas",
                    "personalconpagosretroactivoshastapor45díasnaturales",
                    "personalconlicencia","personalcomisionado",
                    "personalconlicenciaprejubilatoria","personaljubilado",
                    "plaza/función",
                    "registrofederaldecontribuyentesdetrabajadoresconpagosretroactivosconunperiodomayora45días",
                    "personalfederalizadoporregistrofederaldecontribuyentes",
                    "trabajadoresquetramitaronlicenciaprejubilatoriaenelperiodo",
                    "trabajadoresjubiladosenelperiodo",
                    "trabajadoresquecobranconrfc/curpconformatoincorrecto",
                    "analíticodecategorías/plazasautorizadasconsutabulador",
                    "catálogodecategoríasytabuladores",
                    "incompatibilidadgeográfica"
                ]
    catalogosResumen = [
                        "analitico", "tabuladores", "percepciones", "movimientos", "plazas", 
                        "pagosretroactivos", "licencias", "comisiones", "prejubilatoria", 
                        "jubilados", "plazafuncion", "pagosretroactivos2","rfc", 
                        "prejubilatoria2", "jubilados2", "rfcincorrecto", "analitico2", 
                        "tabuladores2", "incompatibilidad"
                    ]
    encontrados = [False,False,False,False,False,False,False,False,False,False,
                   False,False,False,False,False,False,False,False,False,False]
    for el in pagEdo.find_all('a', href=True):
        txt = el.string
        if txt != None :
            txt = txt.replace(' ', '').lower()
        else:
            continue
        try: 
            idx = catalogos.index(txt)
            global gsArch
            gsArch = catalogosResumen[idx]
            encontrados[idx] = 1
            url = ('https://sep.gob.mx' if el['href'].startswith('/') else '') + el['href']
            print("Archivo Encontrado: " + el.text + ' [' + url + ']')
            
            descargarArchivo(url if url.endswith('.zip') else navegarEn(url))
        except ValueError:
            continue

def navegaEdo(trim):
    estados = [
                "aguascalientes", "bajacalifornia", "bajacaliforniasur", "campeche",
                "chiapas", "chihuahua", "coahuila", "colima", "durango", "estadodeméxico",
                "guanajuato", "guerrero", "hidalgo", "jalisco", "michoacán", "morelos",
                "nayarit", "nuevoleón", "oaxaca", "puebla", "querétaro", "quintanaroo",
                "sanluispotosí", "sinaloa", "sonora", "tabasco", "tamaulipas", "tlaxcala",
                "veracruz", "yucatán", "zacatecas"
            ]
    encontrados = [False,False,False,False,False,False,False,False,False,False,False,False,
                   False,False,False,False,False,False,False,False,False,False,False,False,
                   False,False,False,False,False,False,False]
    for el in trim.find_all('a', href=True) :
        txt = el.string
        if txt != None :
            txt = txt.replace(' ', '').lower()
        else:
            continue
        try: 
            idx = estados.index(txt)
            global gsEdo
            gsEdo = estados[idx]
            encontrados[idx] = 1
            url = ('https://sep.gob.mx' if el['href'].startswith('/') else '') + el['href']
            print("Encontrado: " + el.text + ' [' + url + ']')
            res = navegarEn(url)
            descargarEdo(res)
        except ValueError:
            continue

def navegaTrim():
    urls = [
#            {"trim": "1T2022",  "url": "https://sep.gob.mx/es/sep1/Primer_Trimestre_2022"},
#            {"trim": "1T2021",  "url": "https://sep.gob.mx/es/sep1/Primer_Trimestre_2021"},
#            {"trim": "2T2021",  "url": "https://sep.gob.mx/es/sep1/Segundo_Trimestre_2021"},
#            {"trim": "3T2021",  "url": "https://sep.gob.mx/es/sep1/Tercer_Trimestre_2021"},
#            {"trim": "4T2021",  "url": "https://sep.gob.mx/es/sep1/Cuarto_Trimestre_2021"},
#            {"trim": "1T2020",  "url": "https://sep.gob.mx/es/sep1/Primer_Trimestre_2020"},
            {"trim": "2T2020",  "url": "https://sep.gob.mx/es/sep1/Segundo_Trimestre_2020"},
            {"trim": "3T2020",  "url": "https://sep.gob.mx/es/sep1/Tercer_Trimestre_2020"},
            {"trim": "4T2020",  "url": "https://sep.gob.mx/es/sep1/Cuarto_Trimestre_2020"},
            {"trim": "1T2019",  "url": "https://sep.gob.mx/es/sep1/Primer_Trimestre_2019"},
            {"trim": "2T2019",  "url": "https://sep.gob.mx/es/sep1/Segundo_Trimestre_2019"},
            {"trim": "3T2019",  "url": "https://sep.gob.mx/es/sep1/Tercer_Trimestre_2019"},
            {"trim": "4T2019",  "url": "https://sep.gob.mx/es/sep1/Cuarto_Trimestre_2019"},
            {"trim": "1T2018",  "url": "https://sep.gob.mx/es/sep1/Primer_Trimestre_2018"},
            {"trim": "2T2018",  "url": "https://sep.gob.mx/es/sep1/Segundo_Trimestre_2018"},
            {"trim": "3T2018",  "url": "https://sep.gob.mx/es/sep1/Tercer_Trimestre_2018"},
            {"trim": "4T2018",  "url": "https://sep.gob.mx/es/sep1/Cuarto_Trimestre_2018"},
            {"trim": "1T2017",  "url": "https://sep.gob.mx/es/sep1/Primer_Trimestre_2017"},
            {"trim": "2T2017",  "url": "https://sep.gob.mx/es/sep1/Segundo_Trimestre_2017"},
            {"trim": "3T2017",  "url": "https://sep.gob.mx/es/sep1/Tercer_Trimestre_2017"},
            {"trim": "4T2017",  "url": "https://sep.gob.mx/es/sep1/Cuarto_Trimestre_2017"},
            {"trim": "1T2016",  "url": "https://sep.gob.mx/es/sep1/PRIMER_TRIMESTRE_FONE_2016"},
            {"trim": "2T2016",  "url": "https://sep.gob.mx/es/sep1/Segundo_Trimestre_2016"},
            {"trim": "3T2016",  "url": "https://sep.gob.mx/es/sep1/Tercer_Trimestre_2016"},
            {"trim": "4T2016",  "url": "https://sep.gob.mx/es/sep1/Cuarto_Trimestre_2016"},
            {"trim": "1T2015",  "url": "http://sep.gob.mx/es/sep1/PRIMER_TRIMESTRE_2015"},
            {"trim": "2T2015",  "url": "http://sep.gob.mx/es/sep1/SEGUNDO_TRIMESTRE_2015"},
            {"trim": "3T2015",  "url": "http://sep.gob.mx/es/sep1/TERCER_TRIMESTRE_2015"},
            {"trim": "4T2015",  "url": "http://sep.gob.mx/es/sep1/CUARTO_TRIMESTRE_2015"}
        ]
    for url in urls :
        print(url)
        global gsTrim 
        gsTrim = url['trim']
        trim = navegarEn(url['url'])
        print("Iniciando: " + url['trim'])
        navegaEdo(trim)

Path(gsDir).mkdir(parents=True, exist_ok=True)

navegaTrim()
