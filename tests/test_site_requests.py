import os
import sys

import config as cfg
import pytest
from business import util
from business.crawler import Crawler

#sys.path.insert(0, os.getcwd()) 


browserSession = None
crawler = Crawler()

def test_statuscode_200_main_url():
    url_request = crawler.GetRequest(cfg.configParams['SITE_DOMAIN'])
    assert url_request is not None
    assert url_request.status_code == 200

@pytest.fixture
def load_lista_departamentos():
    return crawler.ListaTodosDepartamentos()

@pytest.fixture
def load_departamento_unico(load_lista_departamentos):
    lista_departamentos = load_lista_departamentos        
    return crawler.GetRequestString(lista_departamentos[0].href)

@pytest.fixture
def load_lista_products(load_lista_departamentos):
    return crawler.ReturnProducts(load_lista_departamentos[0].href)

@pytest.fixture
def load_produto_unico(load_lista_products):
    return crawler.GetRequestStringEncoded(load_lista_products[0].url, 'UTF-8', False)

def test_load_lista_departamentos(load_lista_departamentos):
    lista_departamentos = load_lista_departamentos
    assert lista_departamentos is not None
    assert len(lista_departamentos) > 0
    assert lista_departamentos[0].nome != ''
    assert 'https://' in lista_departamentos[0].href

def test_load_departamentos_count_nav(load_departamento_unico):
    browser = load_departamento_unico
    objRes = browser.xpath(cfg.queryXPath['RESULT_COUNT'])
    countItens = int(util.ExtractNumber(objRes[0].text_content().strip().replace('.', '')))

    assert len(objRes) > 0
    assert countItens > 0

def test_load_lista_produtos(load_lista_products):
    valideProductList = load_lista_products
    assert valideProductList is not None
    assert len(valideProductList) > 0

def test_load_produto_nome(load_produto_unico):
    browser = load_produto_unico
    objNome = crawler.GetElementObject(browser, 'STR_NOME')
    nome = objNome[0].text_content().strip()
    
    assert objNome is not None and len(objNome) > 0
    assert type(objValue) is str

def test_load_produto_total_vendas(load_produto_unico):
    browser = load_produto_unico
    objVendas = crawler.GetElementObject(browser, 'NR_TOTAL_VENDAS')
    totalVendas = int(util.ExtractNumber(objVendas[0].text_content().strip()))

    assert objVendas is not None and len(objVendas) > 0
    assert totalVendas >= 0

