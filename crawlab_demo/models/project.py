from typing import List


class Project(dict):
    @property
    def name(self) -> str:
        return self.get('name')

    @property
    def description(self) -> str:
        return self.get('description')

    @property
    def spiders(self) -> List[str]:
        return self.get('spiders')
