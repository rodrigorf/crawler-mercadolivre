import config as cfg
from business.crawler import Crawler

crawler = Crawler()

def test_statuscode_200_main_url():
    url_request = crawler.GetRequest(cfg.configParams['SITE_DOMAIN'])
    assert url_request is not None
    assert url_request.status_code == 200
