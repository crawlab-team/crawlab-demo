import json
import os.path
import random
import tempfile
from typing import List, Dict

import pkg_resources
from crawlab.client import http_put, http_get, http_post, http_delete
from crawlab.actions.upload import upload_dir

from crawlab_demo.models.demo import DemoModel
from crawlab_demo.models.project import Project
from crawlab_demo.models.schedule import Schedule
from crawlab_demo.models.token import Token
from crawlab_demo.models.user import User

DATA_PATH = os.path.join(os.path.dirname(__file__), 'data')


class Demo(object):
    _demo: DemoModel = None
    _spiders_dir: str = tempfile.mkdtemp()
    _pkg_name = 'crawlab_demo'
    _pkg_spiders_path = 'data/spiders'

    def __init__(self):
        # read demo.json
        with pkg_resources.resource_stream(self._pkg_name, 'data/demo.json') as f:
            data = json.load(f)
            self._demo = DemoModel(data)

        # copy spiders
        self._copy_dir()

        # set spiders directory path
        for i, p in enumerate(self.projects):
            for j, s in enumerate(p.spiders):
                spider_dir_path = os.path.join(self._spiders_dir, f'data/spiders/{s.path}')
                self._demo['projects'][i]['spiders'][j]['_dir_path'] = spider_dir_path

    def _copy_dir(self, dir_path: str = None):
        if dir_path is None:
            dir_path = self._pkg_spiders_path
        for filename in pkg_resources.resource_listdir(self._pkg_name, dir_path):
            file_path = os.path.join(dir_path, filename)
            if pkg_resources.resource_isdir(self._pkg_name, file_path):
                self._copy_dir(file_path)
            else:
                self._copy_file(file_path)

    def _copy_file(self, file_path: str):
        target_file_path = os.path.join(self._spiders_dir, file_path)
        target_dir_path = os.path.dirname(target_file_path)
        if not os.path.exists(target_dir_path):
            os.makedirs(target_dir_path)
        with pkg_resources.resource_stream(self._pkg_name, file_path) as f_in:
            with open(target_file_path, 'wb') as f_out:
                f_out.write(f_in.read())

    @property
    def projects(self) -> List[Project]:
        return self._demo.projects

    @property
    def users(self) -> List[User]:
        return self._demo.users

    @property
    def tokens(self) -> List[Token]:
        return self._demo.tokens

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
            http_post('/projects', {
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
                    http_post(f'/schedules', {
                        'name': sch.name,
                        'description': sch.description,
                        'cron': sch.cron,
                        'enabled': sch.enabled,
                        'spider_id': sid,
                        'mode': sch.mode,
                    })

    def import_users(self):
        for u in self.users:
            http_post('/users', {
                'username': u.username,
                'password': u.password,
                'role': u.role,
                'email': u.email,
            })

    def import_tokens(self):
        for tk in self.tokens:
            http_post('/tokens', {
                'name': tk.name,
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
                http_put(f'/spiders/{sid}', spider)

    @staticmethod
    def run_spiders():
        res = http_get('/spiders', {'all': True})
        data = res.json().get('data')
        for s in data:
            sid = s.get('_id')
            http_post(f'/spiders/{sid}/run', {
                'priority': random.randint(1, 10),
                'mode': s.get('mode'),
            })

    def import_all(self):
        # import
        self.import_projects()
        self.import_spiders()
        self.import_schedules()
        self.import_users()
        self.import_tokens()

        # link
        self.link_projects_spiders()

        # action
        self.run_spiders()

    def reimport_all(self):
        self.cleanup_all()
        self.import_all()

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

        # delete tasks
        res = http_get('/tasks', {'all': True})
        data: List[Dict] = res.json().get('data')
        for d in data:
            _id = d.get('_id')
            http_delete(f'/tasks/{_id}')

        # delete users
        res = http_get('/users', {'all': True})
        data: List[Dict] = res.json().get('data')
        for d in data:
            if d.get('username') == 'admin':
                continue
            _id = d.get('_id')
            http_delete(f'/users/{_id}')

        # delete tokens
        res = http_get('/tokens', {'all': True})
        data: List[Dict] = res.json().get('data')
        for d in data:
            _id = d.get('_id')
            http_delete(f'/tokens/{_id}')


if __name__ == '__main__':
    Demo().import_all()
