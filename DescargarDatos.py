
# Navega en el portal de FONE Artículo 73 de la Ley General de Contabilidad Gubernamental
# El primer paso es la obtención del sitio completo, de esa primer navegación 
# se obtiene el listado de los trimestres disponibles 

from logging import exception
from click import FileError
import requests
from bs4 import BeautifulSoup
from pathlib import Path

gsDir = "./DWN"
gsTrim = ""
gsEdo = ""
gsArch = ""

def navegarEn(Url) : 
    page = requests.get(Url)
    return  BeautifulSoup(page.content, "html.parser")

def descargarArchivo(page):
    if(isinstance(page, str)):
        print("Descargando: " + page)
        Path(gsDir + '/' + gsEdo).mkdir(parents=True, exist_ok=True)
        nombre = gsDir + '/' + gsEdo + '/' + gsTrim + '-' + gsArch + '.zip'
        if Path(nombre).is_file() :
            print("Archivo Existente: " + nombre)
        archivo = requests.get(page)
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
                return descargarArchivo('https://sep.gob.mx' + el['href'])

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
            print("Archivo Encontrado: " + el.text + ' [' + el['href'] + ']')
            if(el['href'].endswith('.zip')):
                descargarArchivo('https://sep.gob.mx' + el['href'])
                continue
            res = navegarEn('https://sep.gob.mx' + el['href'])
            descargarArchivo(res)
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
            print("Encontrado: " + el.text + ' [' + el['href'] + ']')
            res = navegarEn('https://sep.gob.mx' + el['href'])
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
            {"trim": "1T2020",  "url": "https://sep.gob.mx/es/sep1/Primer_Trimestre_2020"},
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
