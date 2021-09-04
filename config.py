'''
ADICIONE ABAIXO AS URLS DAS CATEGORIAS
'''
executarCategorias = [
    'https://lista.mercadolivre.com.br/amortecedor-cofap-150#D[A:amortecedor%20cofap%20150]',
    'https://lista.mercadolivre.com.br/manopla-onix#D[A:manopla%20onix]'
]

configParams = {    
    #BASICO
    'PAGE_SIZE':48,
    'HEADER_TOTAL_SIZE':5,
    'BAIXAR_IMAGENS':True,
    'LIMITE_PRODUTOS':100,
    'POSSUI_CONT_PRODUTOS':True,

    #ADICIONAIS
    'SITE_DOMAIN':'https://lista.mercadolivre.com.br',
    'CSV_HEADER':'categoria; nome; preco cheio; vendidos; url',
    'PAR_FIND_NUMBER_EXP':'[-+]?[,]?[\d]+(?:,\d\d\d)*[\,]?\d*(?:[eE][-+]?\d+)?',
    'USER_AGENT':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36',
    'GERAR_EXCEL_POR_CATEGORIA':True
}

configPaths = {
    'CFG_NOME_PLANILHA':'mercadolivre_items',
    'CFG_INPUT_FOLDER':'./data/input/',
    'CFG_CSV_FOLDER':'./data/output/',
    'CFG_LOG_FOLDER':'./log/',
    'CFG_IMAGE_FOLDER':'./data/output/imagens/'
}

productXPaths = {
    'STR_NOME':'//div[contains(@class,"title-container")]//h1',
    'NR_TOTAL_VENDAS':'//div[@class="ui-pdp-header"]//span[@class="ui-pdp-subtitle"]',
    'NR_PRECO_CHEIO':'(//div[contains(@class,"row--price")]//span[@class="price-tag-fraction"])[1]',
    'HTM_CARACTERISTICAS':'//div[contains(@class,"specs")]//ul//li',   
    'HTM_DESCRICAO':'//div[@class="ui-pdp-description"]', 
    'URL_FOTOS':'//figure[@class="ui-pdp-gallery__figure"]//img', 
    'LST_CATEG_BAR':'//ul[@class="andes-breadcrumb"]//li/a'
} 

altProductXPaths = { 
}

queryXPath = {
    'PAGE_PROD_LIST':'//ol[contains(@class,"search-layout")]//li//a[@class="ui-search-link"]',    
    'RESULT_COUNT':'//span[contains(@class,"quantity-results")]',
    'LNK_NEXT_PAGE':'//link[@rel="canonical"]'
}

