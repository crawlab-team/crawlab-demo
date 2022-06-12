import time
from typing import List, Dict

from crawlab.client import http_get

from crawlab_demo import Demo


def _validate():
    demo = Demo()
    spider_names_demo = []
    for p in demo.projects:
        for s in p.spiders:
            spider_names_demo.append(s.get('name'))

    res = http_get('/spiders', {'all': True})
    data: List[Dict] = res.json().get('data')
    spiders_dict = {s.get('_id'): s for s in data}

    res = http_get('/tasks', {'all': True})
    data: List[Dict] = res.json().get('data')
    for t in data:
        spider_id = t.get('spider_id')
        spider = spiders_dict.get(spider_id)
        assert spider is not None
        spider_name = spider.get('name')
        assert spider_name in spider_names_demo
        assert t.get('status') == 'finished'


def validate():
    timeout = 60
    i = 0
    while i < timeout:
        try:
            _validate()
            break
        except Exception as ex:
            pass
        time.sleep(1)
        i += 1
    if i == timeout:
        assert f'timeout {timeout} seconds reached'
