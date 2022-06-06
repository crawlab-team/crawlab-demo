import json
from typing import List, Dict

from pkg_resources import resource_stream

from crawlab.client import http_put, http_get, http_post, http_delete
from crawlab.actions.upload import upload_dir

from crawlab_demo.models.demo import DemoModel
from crawlab_demo.models.project import Project
from crawlab_demo.models.schedule import Schedule


class Demo(object):
    _demo: DemoModel = None

    def __init__(self):
        self._demo = DemoModel(json.load(resource_stream(__name__, 'data/demo.json')))

    @property
    def projects(self) -> List[Project]:
        return list(map(lambda p: Project(p), self._demo.projects))

    @property
    def schedules(self) -> List[Schedule]:
        _schedules = []
        for p in self.projects:
            for s in p.spiders:
                if s.schedules is None:
                    continue
                for sch in s.schedules:
                    _schedules.append(sch)
        return _schedules

    def import_projects(self):
        for p in self.projects:
            http_put('/projects', {
                'name': p.name,
                'description': p.description,
            })

    def import_spiders(self):
        for p in self.projects:
            for s in p.spiders:
                upload_dir(s.dir_path)

    def import_schedules(self):
        # spiders dict
        res = http_get(f'/spiders', {'all': True})
        data = res.json().get('data')
        spiders_dict = {s.get('name'): s for s in data}

        # iterate projects
        for p in self.projects:
            # iterate spiders
            for s in p.spiders:
                # skip no-schedule spiders
                if s.schedules is None:
                    continue
                # spider id
                sid = spiders_dict.get(s.name).get('_id')

                # iterate schedules
                for sch in s.schedules:
                    http_put(f'/schedules', {
                        'name': sch.name,
                        'description': sch.description,
                        'cron': sch.cron,
                        'enabled': sch.enabled,
                        'spider_id': sid,
                        'mode': sch.mode,
                    })

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
            for s in p.spiders:
                # spider id
                sid = spiders_dict.get(s.name).get('_id')

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
        self.import_schedules()

    @staticmethod
    def cleanup_all():
        # delete projects
        res = http_get('/projects', {'all': True})
        data: List[Dict] = res.json().get('data')
        for d in data:
            _id = d.get('_id')
            http_delete(f'/projects/{_id}')

        # delete spiders
        res = http_get('/spiders', {'all': True})
        data: List[Dict] = res.json().get('data')
        for d in data:
            _id = d.get('_id')
            http_delete(f'/spiders/{_id}')

        # delete schedules
        res = http_get('/schedules', {'all': True})
        data: List[Dict] = res.json().get('data')
        for d in data:
            _id = d.get('_id')
            http_delete(f'/schedules/{_id}')


if __name__ == '__main__':
    Demo().import_all()
