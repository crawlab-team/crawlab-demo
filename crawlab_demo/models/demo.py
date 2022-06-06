from typing import List

from crawlab_demo.models.project import Project
from crawlab_demo.models.user import User


class DemoModel(dict):
    @property
    def projects(self) -> List[Project]:
        return list(map(lambda x: Project(x), self.get('projects')))

    @property
    def users(self):
        return list(map(lambda x: User(x), self.get('users')))
