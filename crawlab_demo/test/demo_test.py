import os
import unittest
from typing import List, Dict

from crawlab.actions.login import login
from crawlab.client import http_get

from crawlab_demo.demo import Demo


class DemoTestCase(unittest.TestCase):
    demo = Demo()

    def setUp(self) -> None:
        api_address = os.environ.get('CRAWLAB_API_ADDRESS') or 'http://localhost:8080/api'
        login(api_address=api_address, username='admin', password='admin')
        self.demo.cleanup_all()

    def tearDown(self) -> None:
        self.demo.cleanup_all()

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
            for s in p.spiders:
                spider_remote = spiders_dict.get(s.name)
                assert spider_remote is not None
                assert spider_remote.get('name') == s.name
                assert spider_remote.get('description') == s.description

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

    def test_import_schedules(self):
        self.demo.import_spiders()
        self.demo.import_schedules()
        res = http_get('/spiders', {'all': True})
        data: List[Dict] = res.json().get('data')
        spiders_dict = {s.get('name'): s for s in data}
        res = http_get('/schedules', {'all': True})
        data: List[Dict] = res.json().get('data')
        schedules_dict = {sch.get('name'): sch for sch in data}
        for p in self.demo.projects:
            for s in p.spiders:
                if s.schedules is None:
                    continue
                for sch in s.schedules:
                    schedule_remote = schedules_dict.get(sch.name)
                    assert schedule_remote is not None
                    assert schedule_remote.get('name') == sch.name
                    assert schedule_remote.get('description') == sch.description
                    assert schedule_remote.get('cron') == sch.cron
                    assert schedule_remote.get('enabled') == sch.enabled
                    spider_remote = spiders_dict.get(s.name)
                    assert spider_remote is not None
                    assert spider_remote.get('_id') == spider_remote.get('_id')

    def test_import_users(self):
        self.demo.import_users()
        res = http_get('/users', {'all': True})
        data: List[Dict] = res.json().get('data')
        assert len(data) > 0
        usernames = list(map(lambda x: x.username, self.demo.users))
        for u in data:
            if u.get('username') == 'admin':
                continue
            assert u.get('username') in usernames

    def test_import_tokens(self):
        self.demo.import_tokens()
        res = http_get('/tokens', {'all': True})
        data: List[Dict] = res.json().get('data')
        assert len(data) > 0
        names = list(map(lambda x: x.name, self.demo.tokens))
        for tk in data:
            assert tk.get('name') in names


if __name__ == '__main__':
    unittest.main()
