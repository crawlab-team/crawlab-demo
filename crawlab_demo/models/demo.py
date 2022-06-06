from typing import List

from crawlab_demo.models.project import Project


class DemoModel(dict):
    @property
    def projects(self) -> List[Project]:
        return self.get('projects')
