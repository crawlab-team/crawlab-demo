from typing import List

from crawlab_demo.models.spider import Spider


class Project(dict):
    @property
    def name(self) -> str:
        return self.get('name')

    @property
    def description(self) -> str:
        return self.get('description')

    @property
    def spiders(self) -> List[Spider]:
        return list(map(lambda s: Spider(s), self.get('spiders')))
