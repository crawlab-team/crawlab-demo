import os
import unittest
from typing import List, Dict

from crawlab.client import http_get, http_delete
from crawlab.config import get_spider_config

from crawlab_demo.demo import Demo


class DemoTestCase(unittest.TestCase):
    demo = Demo()

    def test_import_projects(self):
        self.demo.import_projects()
        res = http_get('/projects', {'all': True})
        data: List[Dict] = res.json().get('data')
        assert len(data) > 0
        names = list(map(lambda x: x.name, self.demo.projects))
        descriptions = list(map(lambda x: x.description, self.demo.projects))
        for p in data:
            assert p.get('name') in names
            assert p.get('description') in descriptions

    def test_import_spiders(self):
        self.demo.import_spiders()
        res = http_get('/spiders', {'all': True})
        data: List[Dict] = res.json().get('data')
        assert len(data) > 0
        spiders_dict = {s.get('name'): s for s in data}
        for p in self.demo.projects:
            for s_path in p.spiders:
                spider_path = os.path.join(os.path.dirname(__file__), f'../../crawlab_demo/data/spiders/{s_path}')
                spider_path = os.path.abspath(spider_path)
                spider_config = get_spider_config(spider_path)
                spider_remote = spiders_dict.get(spider_config.name)
                assert spider_remote is not None
                assert spider_remote.get('name') == spider_config.name
                assert spider_remote.get('description') == spider_config.description

    def test_link_projects_spiders(self):
        self.demo.import_projects()
        self.demo.import_spiders()
        self.demo.link_projects_spiders()
        res = http_get('/projects', {'page': 1, 'size': 1000})
        data = res.json().get('data')
        projects_dict = {p.get('name'): p for p in data}
        for p in self.demo.projects:
            project_spiders = projects_dict.get(p.name).get('spiders')
            assert len(p.spiders) == project_spiders

    @staticmethod
    def _delete_all():
        # delete projects
        res = http_get('/projects', {'all': True})
        data: List[Dict] = res.json().get('data')
        for p in data:
            _id = p.get('_id')
            http_delete(f'/projects/{_id}')

        # delete spiders
        res = http_get('/spiders', {'all': True})
        data: List[Dict] = res.json().get('data')
        for s in data:
            _id = s.get('_id')
            http_delete(f'/spiders/{_id}')

    def tearDown(self) -> None:
        self._delete_all()


if __name__ == '__main__':
    unittest.main()
