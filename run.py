import math

import config as cfg
from business import util
from business.crawler import Crawler
from business.logexecucao import LogExecucao
from entities.product import Product

try:
    totalCategorias = 0
    categoriasProdutos = {}
    logOut = LogExecucao(totalCategorias)
    PAGE_SIZE = cfg.configParams['PAGE_SIZE']
    habilitarDownloads = cfg.configParams['BAIXAR_IMAGENS']
    gerarExcelPorCategoria = cfg.configParams['GERAR_EXCEL_POR_CATEGORIA'] == 'True'

    # CLEAN OUTPUT FOLDER
    util.CleanOutputFile()

    # LOAD ALL IMAGE NAMES
    imageList = util.GellAllImageFiles()

    browserSession = None
    crawler = Crawler()
    crawler.usePyQTRequest = False

    try:
        nomeCategoria = 'N/A'
        # RETORNA OS LINKS DE TODOS DEPARTAMENTOS
        listaDepartamentos = crawler.ListaTodosDepartamentos()
        totalProdCont = 0
        prodProcessados = 0
        forceStop = False
        categoriasProcessadas = 0
        limiteProdutos = cfg.configParams['LIMITE_PRODUTOS']
        totalCategorias = len(listaDepartamentos)

        for categoria in listaDepartamentos:
            forceStop = False
            nomeCategoria = categoria.nome
            urlCategoriaMod = categoria.href
            logOut.LogPrint('CATEGORIA ATUAL: ' + nomeCategoria +
                            '-> ' + util.fix_text(urlCategoriaMod), 'INFO')
            categoriasProdutos[nomeCategoria] = 0

            browser = crawler.GetRequestString(urlCategoriaMod)

            # GET RETURNED PRODUCTS COUNT
            count = 1
            pagesNumber = 1
            valideUrlList = []

            if cfg.configParams['POSSUI_CONT_PRODUTOS']:
                try:
                    objRes = browser.xpath(cfg.queryXPath['RESULT_COUNT'])
                    count = int(util.ExtractNumber(
                        objRes[0].text_content().strip().replace('.', '')))
                    logOut.LogPrint('Result count: ' + str(count), 'INFO')
                    totalProdCont += count
                except Exception:
                    logOut.LogPrint(
                        'Nenhum produto localizado nesta categoria.', 'INFO')

            if PAGE_SIZE == 48:
                pagesNumber = math.ceil(float(count)/float(PAGE_SIZE))
            logOut.LogPrint('Número de páginas existentes: ' +
                            str(pagesNumber), 'INFO')

            # NEXTPAGE LINK
            objNextPage = browser.xpath(cfg.queryXPath['LNK_NEXT_PAGE'])
            if not objNextPage or len(objNextPage) == 0:
                break
            pageUrlBase = objNextPage[0].get('href')
            if 'http' not in pageUrlBase:
                break

            pageIndex = 1
            linkParts = pageUrlBase.split('_Desde')
            basePaginUrl = linkParts[0] + '_Desde_PAGEINDEX_'
            pageUrl = urlCategoriaMod

            # PAGES LOOP
            while pageIndex <= pagesNumber:
                try:
                    if forceStop:
                        logOut.LogPrint('FORCE STOP!!!', 'INFO')
                        break

                    logOut.LogPrint(
                        '*** Processando página número:' + str(pageIndex) + ' *** ', 'INFO')
                    if pageIndex > 0:
                        pageUrl = basePaginUrl.replace(
                            'PAGEINDEX', str(1 + PAGE_SIZE*pageIndex))
                    else:
                        pageUrl = urlCategoriaMod
                    valideProductList = crawler.ReturnProducts(pageUrl)

                    if valideProductList is not None:
                        logOut.LogPrint(
                            'URLs de produtos encontradas:' + str(len(valideProductList)), 'INFO')
                    else:
                        break

                    # PRODUCTS LOOP
                    for prod in valideProductList:
                        try:
                            logOut.LogPrint(
                                'URL Produto Atual:' + prod.url, 'INFO')
                            browser = crawler.GetRequestStringEncoded(
                                prod.url, 'UTF-8', usePyQT=False)

                            variantsList = []
                            allPaths = list(cfg.productXPaths)

                            for xpath in allPaths:
                                value = 'N/A'
                                mapping = True
                                obj = crawler.GetElementObject(browser, xpath)
                                if obj is not None and len(obj) > 0:
                                    if 'STR_RESUMO' in xpath:
                                        value = obj[0]
                                    elif 'STR_' in xpath:
                                        value = obj[0].text_content().strip()
                                    elif 'NR_' in xpath:
                                        value = obj[0].text_content().strip()
                                    elif 'HTM_' in xpath:
                                        value = obj
                                    elif 'URL_' in xpath:
                                        value = obj
                                    elif 'LST_' in xpath:
                                        value = obj
                                    elif 'OBJ_' in xpath:
                                        value = obj

                                if type(value) is not list and value is not None:
                                    logOut.LogPrint(
                                        xpath + ':' + value.strip(), 'INFO')

                                crawler.ProductMapping(prod, xpath, value)

                            # FAZER GRAVACAO APENAS UMA VEZ
                            util.RecordOutput(prod, 'CSV', imageList, variantsList,
                                              removeUrlParams=True, baixarImagem=habilitarDownloads)
                            prod = None
                            logOut.LogPrint('', 'INFO')
                            logOut.LogPrint(
                                '---------- FIM PRODUTO ----------', 'INFO')
                            logOut.LogPrint('', 'INFO')
                            prodProcessados += 1
                            logOut.LogPrint(
                                'Produtos processados: ' + str(prodProcessados), 'INFO')

                            if prodProcessados >= limiteProdutos:
                                forceStop = True
                                prodProcessados = 0
                                break
                        except Exception as pe:
                            logOut.LogPrint(
                                'Erro em produto: Xpath(' + xpath + ') - ' + str(pe), 'ERROR')
                except Exception as et:
                    logOut.LogPrint('Erro na página:' + str(et), 'ERROR')
                finally:
                    pageIndex = pageIndex + 1
                    logOut.LogPrint(
                        '========== Indo para próxima página. ========== ', 'INFO')

            categoriasProcessadas += 1
            logOut.execucaoAtual = categoriasProcessadas
            if valideProductList is not None:
                categoriasProdutos[nomeCategoria] = int(
                    categoriasProdutos[nomeCategoria]) + len(valideProductList)

            if gerarExcelPorCategoria:
                util.GerarExcel(nomeCategoria)
                util.CleanOutputFile()

        logOut.LogPrint('Total de produtos: ' + str(totalProdCont), 'INFO')
    except Exception as fe:
        logOut.LogPrint('Erro na consulta:' + str(fe), 'ERROR')
    finally:
        logOut.LogPrint('', 'INFO')
        logOut.LogPrint(
            '========== Query list end. Calling next query URL. ========== ', 'INFO')
        logOut.LogPrint('', 'INFO')
except Exception as e:
    print('Erro:' + str(e))
finally:
    print('----- END OF CRAWLER -----')
    # GENERATE THE XLSL FILE BASED ON CSV
    if not gerarExcelPorCategoria:
        util.GerarExcel()

    logOut.LogPrint('', 'INFO')
    logOut.LogPrint('----- CATEGORIAS PROCESSADAS -----', 'INFO')
    for nome, valor in categoriasProdutos.items():
        logOut.LogPrint(
            'Categoria:{0} -- Produtos:{1}'.format(nome, valor), 'INFO')
