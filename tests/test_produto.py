import pytest
from business import util
from business.crawler import Crawler

crawler = Crawler()

@pytest.fixture
def load_lista_departamentos():
    return crawler.ListaTodosDepartamentos()

@pytest.fixture
def load_lista_products(load_lista_departamentos):
    return crawler.ReturnProducts(load_lista_departamentos[0].href)

@pytest.fixture
def load_produto_unico(load_lista_products):
    return crawler.GetRequestStringEncoded(load_lista_products[0].url, 'UTF-8', False)

def test_load_lista_produtos(load_lista_products):
    valideProductList = load_lista_products
    assert valideProductList is not None
    assert len(valideProductList) > 0

def test_load_produto_nome(load_produto_unico):
    browser = load_produto_unico
    objNome = crawler.GetElementObject(browser, 'STR_NOME')
    nome = objNome[0].text_content().strip()
    
    assert objNome is not None and len(objNome) > 0
    assert type(nome) is str

def test_load_produto_total_vendas(load_produto_unico):
    browser = load_produto_unico
    objVendas = crawler.GetElementObject(browser, 'NR_TOTAL_VENDAS')
    totalVendas = int(util.ExtractNumber(objVendas[0].text_content().strip()))

    assert objVendas is not None and len(objVendas) > 0
    assert totalVendas >= 0

def test_load_produto_total_preco(load_produto_unico):
    browser = load_produto_unico
    objPreco = crawler.GetElementObject(browser, 'NR_PRECO_BASE')
    precoProduto = int(util.ExtractNumber(objPreco[0].text_content().strip()))

    assert objPreco is not None and len(objPreco) > 0
    assert precoProduto > 0
