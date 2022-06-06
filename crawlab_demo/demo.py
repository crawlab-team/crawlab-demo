import json
import os.path
from typing import List, Dict

from crawlab.config import get_spider_config
from pkg_resources import resource_stream

from crawlab.client import http_put, http_get, http_post
from crawlab.actions.upload import upload_dir

from crawlab_demo.models.project import Project


class Demo(object):
    _projects: List[Project] = None

    def __init__(self):
        self._projects = json.load(resource_stream(__name__, '../data/projects.json'))

    @property
    def projects(self):
        return list(map(lambda p: Project(p), self._projects))

    def import_projects(self):
        for p in self.projects:
            http_put('/projects', {
                'name': p.name,
                'description': p.description,
            })

    def import_spiders(self):
        for p in self.projects:
            for s in p.spiders:
                spider_path = os.path.join(os.path.dirname(__file__), f'../data/spiders/{s}')
                upload_dir(spider_path)

    def link_projects_spiders(self):
        # all projects dict
        res = http_get('/projects', {'all': True})
        data: List[Dict] = res.json().get('data')
        projects_dict = {p.get('name'): p for p in data}

        # all spiders dict
        res = http_get('/spiders', {'all': True})
        data: List[Dict] = res.json().get('data')
        spiders_dict = {s.get('name'): s for s in data}

        # iterate projects
        for p in self.projects:
            # project id
            pid = projects_dict.get(p.name).get('_id')

            # iterate spiders
            for s_path in p.spiders:
                spider_path = os.path.join(os.path.dirname(__file__), f'../../crawlab_demo/data/spiders/{s_path}')
                spider_path = os.path.abspath(spider_path)
                spider_config = get_spider_config(spider_path)

                # spider id
                sid = spiders_dict.get(spider_config.name).get('_id')

                # spider
                res = http_get(f'/spiders/{sid}')
                spider = res.json().get('data')

                # set project id
                spider['project_id'] = pid

                # update
                http_post(f'/spiders/{sid}', spider)

    def import_all(self):
        self.import_projects()
        self.import_spiders()
        self.link_projects_spiders()

    def run(self):
        pass
