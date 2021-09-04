import csv
import os
import re
import string
from os import listdir
from os.path import isfile, join
from pathlib import Path

import config as cfg
import lxml
import requests
import xlsxwriter
from ftfy import fix_encoding, fix_text

from business.logexecucao import LogExecucao


def ExtractLinksFromElements(productElements):
    tempList = []
    for liItem in productElements:           
        href = liItem.find_element_by_class_name('vip').get_attribute('href')       
        if(href == ''):
            continue
        tempList.append(href)
    return tempList

def RemoveWords(query):
    stopwords = cfg.wordExcludeList
    resultwords  = [word for word in re.split("\W+",query) if word.lower() not in stopwords]
    return ' '.join(resultwords)

def ExtractValideText(query):  
    return RemoveWords(fix_encoding(query))

def ChangeUrlEstructure(url, old, new):
    return url.replace(old, new)

def AppendToUrl(baseUrl, parameter, paramValue):    
    if(parameter not in baseUrl):
        return baseUrl + '/{0}/{1}'.format(parameter, paramValue)
    else:
        return baseUrl

def RemoveAllUrlParameter(baseUrl):
    return baseUrl.split('?')[0]
    
def ChangeURLParameter(baseUrl, parameter, paramValue, separator):    
    if(parameter not in baseUrl):
        return baseUrl + '{2}{0}={1}'.format(parameter, paramValue,separator)
    else:
        return baseUrl

def GetAllQueries():
    resultList = []
    PATH = cfg.configPaths['CFG_INPUT_FOLDER'] + 'input.txt'
    with open(PATH) as f:
        content = f.readlines()

    for x in content:
        resultList.append(x.strip())
    return resultList
    
def ExtractNumber(text):
    expressao = cfg.configParams['PAR_FIND_NUMBER_EXP']
    numbers = re.findall(expressao, text)
    if(len(numbers) > 0):
        return numbers[0]
    else:
        return text
    
def ExtractNumbersCompiled(text):
    p = re.compile(r'\b\d{1,3}(?:\.\d{3})*,\d+\b')
    return re.findall(p, text)

def GetTodayOutputFilePath(ext):
    return cfg.configPaths['CFG_CSV_FOLDER'] + cfg.configPaths['CFG_NOME_PLANILHA'] + "." + ext

def CleanOutputFile():
    filePath = GetTodayOutputFilePath('csv')
    my_file = Path(filePath)
    if my_file.is_file():
        os.remove(filePath)

def FixUrlPath(urlPath):
    return urlPath.replace(' ','%20')

def TransformCsvToExcel(path, nomeCategoria=None):
    generated = False
    my_file = Path(path)
    if(my_file.is_file()):
        if(nomeCategoria is not None):
            newPath = '/'.join(path.split('/')[:-1]) + '/' + nomeCategoria.lower() + '.csv'

        wb = xlsxwriter.Workbook(newPath.replace(".csv",".xlsx"))
        ws = wb.add_worksheet("Lista Produtos")          
        ws.set_column(5, 5, 60)

        wrap = wb.add_format()
        wrap.set_text_wrap()

        with open(path, mode="r" , encoding="utf-8") as csvfile:
            table = csv.reader(csvfile, delimiter=';')
            lista = list(table)
            rowCount = len(lista)
            generated = rowCount > 0
            i = 0        
            for row in lista:
                j = 0
                for col in row:
                    if(j in [3,4] and i > 0):
                        ws.write(i, j, col.replace('\LF','\n').strip(), wrap)
                    else:
                        ws.write(i, j, col)
                    
                    j += 1
                i += 1
        wb.close()
    return generated

def SaveFile(text, ext):
    fullPath = GetTodayOutputFilePath(ext)
    my_file = Path(fullPath)
    if not my_file.is_file():
        with open(fullPath, mode="a" , encoding="utf-8") as myfile:
            totalSize = int(cfg.configParams['HEADER_TOTAL_SIZE'])
            baseHeaderSize = len(cfg.configParams['CSV_HEADER'].split(';'))

            baixarImagens = cfg.configParams['BAIXAR_IMAGENS']
            generatedHeader = GerarHeaderDinamico(totalSize-baseHeaderSize,baixarImagens)
            
            myfile.write(cfg.configParams['CSV_HEADER'] + ';' + generatedHeader + ' \n')
            myfile.write(text)
    else:
        with open(fullPath, mode="a" , encoding="utf-8") as myfile:
            myfile.write(text)

def downloadImageWithRequests(imgUrl, localPath):
    try:
        f = open(localPath,'wb')
        f.write(requests.get(imgUrl).content)
    except Exception as ex:
        print('DOWNLOAD ERROR -> A imagem {0} não pode ser baixada. -- {1}'.format(imgUrl, str(ex)),'ERRO')
    finally:
        f.close()

def baixar(nome, foto):
    LOCAL_PATH = cfg.configPaths['CFG_IMAGE_FOLDER']
    imageFile = LOCAL_PATH + nome    
    downloadImageWithRequests(foto, imageFile)

def findDimensions(text):
    p = re.compile(r'(?P<l>\d+(\.\d+)?)\s*x\s*(?P<w>\d+(\.\d+)?)\s*x\s*(?P<h>\d+(\.\d+)?)')
    m = p.search(text)
    if (m):
        return m.group("l"), m.group("w"), m.group("h")
    return None
    
def AdicionarQuebraLinhaExcel(texto):
    texto = texto.split('\LF')
    baseFormula = '=CONCATENAR({0})'
    params = ''
    for item in texto:
        params += '"' + item + '"' + ',CARACT(10),'
    return baseFormula.format(params[:-10])

def CleanHtml(raw_html):
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', raw_html)
    return cleantext.replace(u'\xa0', u' ')

def ModelarDescricao(descricaoHtml):
    noWrap = descricaoHtml.replace('->',' - ').replace('</p><p>','\LF').replace('<br>','')
    noWrap = noWrap.replace('\r','').replace('\n','').replace('\t','')
    noWrap = CleanHtml(noWrap).strip()
    return noWrap.replace('&gt','').replace(';',':')

def stringify_children(node):
    if node is None or (len(node) == 0 and not getattr(node, 'text', None)):
        return ""
    node.attrib.clear()
    opening_tag = len(node.tag) + 2
    closing_tag = -(len(node.tag) + 3)
    finalHtml = lxml.html.tostring(node, encoding='unicode')[opening_tag:closing_tag]
    return fix_encoding(finalHtml)      

def getindexdefault(lista, elem, default):
    try:
        thing_index = lista.index(elem)
        return thing_index
    except ValueError:
        return default

def cleanInput(input):
    input = re.sub('\n+'," ", input)
    input = re.sub('\[[0-9]*\]', "", input)
    input = re.sub(' +', " ", input)
    input = bytes(input, "UTF-8")
    input = input.decode("ascii", "ignore")
    cleanInput = []
    input = input.split(' ')
    for item in input:
        item = item.strip(string.punctuation)
        if len(item) > 1 or (item.lower() == 'a' or item.lower() == 'i'):
            cleanInput.append(item)
    return cleanInput

def GerarHeaderDinamico(size, baixarImagens):
    header = ''    
    for number in range(size):
        header += ' imageUrl' + str(number+1) + ';'    

    if(baixarImagens == 'True'):
        for number in range(size):
            header += ' imagePath' + str(number+1) + ';'
    return header

def PreencherLacunasCabecalho(rowText):
    tamanhoAtual = len(rowText.split(';'))
    tamanhoEsperado = int(cfg.configParams['HEADER_TOTAL_SIZE'])
    restante = (tamanhoEsperado-tamanhoAtual)

    for index in range(restante):
        rowText += ' ;'
    return rowText + ' ;'

def RecordOutput(prod, outType, imagesList, variantsList, removeUrlParams=False, baixarImagem=False):        
    LOCAL_PATH = cfg.configPaths['CFG_IMAGE_FOLDER']
    header = cfg.configParams['CSV_HEADER'].split(';')
    generatedHeader = ''
    logOut = LogExecucao(0)
    templateZip = ''
    for number in range(len(header)):
        templateZip += '{' + str(number) + '}; '    

    if(baixarImagem):
        for foto in prod.urlImagem:
            if(removeUrlParams is True):
                foto = RemoveAllUrlParameter(foto)
            imgName = foto.split('/')[-1]
            imageFile = LOCAL_PATH + imgName
            prod.imageFile.append(imageFile)
            index = getindexdefault(imagesList, imgName, -1)        
            if(index == -1):
                try:                                
                    baixar(imgName, foto)
                    imagesList.append(imgName)
                except Exception as ex:
                    logOut.LogPrint('DOWNLOAD ERROR -> A imagem {0} não pode ser baixada.'.format(imgName),'ERRO')
            else:
                logOut.LogPrint('COLLISION ERROR -> A imagem {0} já existe.'.format(imgName),'ERRO') 
    
    variantsList = prod.variacoes
    if(len(variantsList) == 0):
        variantsList.append('')

    for variacao in variantsList:
        nome = prod.nome
        if(variacao != ''):
            nome = '{0} - {1}'.format(nome, fix_encoding(variacao))

        rowText = templateZip.format(
                    fix_encoding(prod.categoria), 
                    fix_text(nome), 
                    prod.precoCheio, 
                    prod.totalVendas,
                    prod.url)
        
        #rowText += ';'.join(prod.urlImagem)
        rowText = PreencherLacunasCabecalho(rowText)    
        if(baixarImagem):
            rowText += ';'.join(prod.imageFile)
            rowText = PreencherLacunasCabecalho(rowText)  
        rowText += ' \n'
        if(outType == 'CSV'):
            SaveFile(rowText, 'csv')

def GellAllImageFiles():
    LOCAL_PATH = cfg.configPaths['CFG_IMAGE_FOLDER']
    onlyfiles = [f for f in listdir(LOCAL_PATH) if isfile(join(LOCAL_PATH, f))]
    return onlyfiles

def gerarExcel(nomeCategoria=cfg.configPaths['CFG_NOME_PLANILHA']):
    fullPath = cfg.configPaths['CFG_CSV_FOLDER'] + cfg.configPaths['CFG_NOME_PLANILHA'] + ".csv"
    if(TransformCsvToExcel(fullPath, nomeCategoria)):
        print('Arquivo XLSX criado.', 'INFO')
    else:
        print('Nenhum arquivo xlsx foi gerado. Verifique o log.', 'ERROR')
