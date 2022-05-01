import config as cfg
import pytest
from business import util
from business.crawler import Crawler

crawler = Crawler()

@pytest.fixture
def load_lista_departamentos():
    return crawler.ListaTodosDepartamentos()

@pytest.fixture
def load_departamento_unico(load_lista_departamentos):
    lista_departamentos = load_lista_departamentos        
    return crawler.GetRequestString(lista_departamentos[0].href)

def test_load_lista_departamentos(load_lista_departamentos):
    lista_departamentos = load_lista_departamentos
    assert lista_departamentos is not None
    assert len(lista_departamentos) > 0
    assert len(lista_departamentos[0].nome) > 0
    assert 'https://' in lista_departamentos[0].href

def test_load_departamentos_count_nav(load_departamento_unico):
    browser = load_departamento_unico
    objRes = browser.xpath(cfg.queryXPath['RESULT_COUNT'])
    countItens = int(util.ExtractNumber(objRes[0].text_content().strip().replace('.', '')))
    assert len(objRes) > 0
    assert countItens > 0

