import json
import sys
from urllib.request import urlopen

import config as cfg
import dashtable
import lxml
import lxml.html
import requests
from entities.categoria import Categoria
from entities.product import Product

from business import util
from business.logexecucao import LogExecucao

sys.path.append('./config')

class Crawler:
    def __init__(self):
        self.browserSession = None
        self.header = None
        self.cookie = None
        self.listaCodigos = []
        self.usePyQTRequest = False

    def GetRequest(self, url, usePyQT=False):
        if(self.browserSession is None):
            headers = {'User-Agent': cfg.configParams['USER_AGENT'] }
            if(headers is not None):
                return requests.get(url, headers=headers)
            else:
                return requests.get(url)
        else:
            return self.browserSession.get(url)

    def GetRequestString(self, url, usePyQT=False):
        getResult = self.GetRequest(url, usePyQT)
        if(usePyQT):
             return lxml.html.fromstring(getResult)
        else:
            return lxml.html.fromstring(getResult.content)

    def GetRequestStringEncoded(self, url, encode, usePyQT=False):
        getResult = self.GetRequest(url, usePyQT)
        if(usePyQT and self.usePyQTRequest):
            return lxml.html.fromstring(getResult)
        else:            
            getResult.encoding = encode
            return lxml.html.fromstring(getResult.content) 

    def RetornaLinksPaginas(self, html):
        listLinks = []
        for item in html.xpath(cfg.queryXPath['PAGINATION_BAR']):
            #SE O TEXT FOR NÚMERO ADICIONA
            if(str.isdigit(item.text)):
                listLinks.append(item.get('href'))
        return listLinks

    def EfetuaLogin(self):
        #EFETUA LOGIN SE NECESSARIO
        urlLogin = cfg.loginParams['URL_LOGIN']
        if(urlLogin != ''):
            session_requests = requests.session()
            result = session_requests.post(
                cfg.loginParams['URL_LOGIN'], 
                data = cfg.loginPayload
            )
            if(result.ok and str(result.status_code) == '200'):
                self.browserSession = session_requests       
            return result.status_code

    def GetElementObject(self, browser, xpathName):
        obj = None
        try:
            obj = browser.xpath(cfg.productXPaths[xpathName])
        except Exception:
            obj = None
        
        if(obj is None):
            try:
                return browser.xpath(cfg.altProductXPaths['ALT_' + xpathName])
            except Exception:
                return None

        return obj

    def ReturnIDProductFromURL(self, url):
        return url.split('?').split('=')[1]

    def GetElementValue(self, element, configXPathName):
        if('ATT_' in configXPathName):
            if('HREF' in configXPathName):
                return element.get('href').strip()
        elif('TXT' in configXPathName):
            return element.text_content().strip()
        elif('HTM' in configXPathName):
            return util.ModelarDescricao(util.CleanHtml(util.stringify_children(element)))

    def LoadAPIObject(self, url, idProd):
        url = url.replace('{codigo}', idProd)
        response = urlopen(url).read().decode('utf-8')
        responseJson = json.loads(response)
        return responseJson

    def ProductMapping(self, prod, xpath, value):
        if(value == 'N/A' or value is None):
            return

        if(xpath == 'STR_NOME'):
            prod.nome = value       
        elif(xpath == 'STR_CODIGO'):
            prod.codigo = value
        elif(xpath == 'LST_CATEG_BAR'):
            categoria = []
            for crumb in value:
                categoria.append(crumb.text_content().strip())
            prod.categoria = ' > '.join(categoria)
        elif(xpath == 'NR_PRECO_BASE'):
            if(prod.precoCheio == ''):
                prod.precoCheio = value  
        elif(xpath == 'NR_TOTAL_VENDAS'):
            if(prod.totalVendas == ''):
                valorVenda = util.ExtractNumber(value) 
                prod.totalVendas =  0 if valorVenda.lower() == 'novo' else valorVenda
        elif(xpath == 'HTM_DESCRICAO'):
            desc = util.stringify_children(value[0]).replace('\t','').replace('\n','').replace('<br>','\\LF')
            prod.descricao = util.ModelarDescricao(desc)
        elif(xpath == 'HTM_CARACTERISTICAS'):
            table_data = []
            if(len(value) == 0):
                return
            for item in value:
                table_data.append(['\LF' + item.text_content().strip().replace('\t','')])                

            if(table_data):
                prod.caracteristicas = dashtable.data2md(table_data).replace('\n','')
        elif(xpath == 'URL_FOTOS'):
            for foto in value:
                fixedUrl = foto.get('src')
                if(fixedUrl is not None and len(prod.urlImagem) <= 10):
                    prod.urlImagem.append(fixedUrl)


    def ListaTodosDepartamentos(self):
        listaSemDuplicadas = []
        if(len(cfg.executarCategorias) > 0):
            for item in cfg.executarCategorias:
                categoria = Categoria()
                categoria.href = item
                categoria.nome = item.split('/')[-1].split('#')[0]       

                itemDuplicado = next((True for item in listaSemDuplicadas if item.href == categoria.href), False)
                if(not itemDuplicado):
                    listaSemDuplicadas.append(categoria)
        return listaSemDuplicadas

    def ReturnProducts(self, urlPath):
        tempList = []
        try:  
            trys = 1        
            objProductsList = []            
            while(len(objProductsList) == 0 and trys < 2):
                result = self.GetRequestString(urlPath)
                objProductsList = result.xpath(cfg.queryXPath['PAGE_PROD_LIST'])
                trys += 1

            for prodBox in objProductsList:
                try:
                    produtoTemp = Product()   

                    href = prodBox.get('href').strip()                
                    produtoTemp.url = href
                    if(produtoTemp.url not in self.listaCodigos):
                        self.listaCodigos.append(produtoTemp.url)
                        tempList.append(produtoTemp)
                except Exception:
                    continue
                                    
        except Exception as ex:
            print('ERRO --> Retorn produtos:' + str(ex), 'ERRO')
            return None 
        return tempList
