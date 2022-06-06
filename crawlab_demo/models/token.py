from typing import List

from crawlab_demo.models.spider import Spider


class Token(dict):
    @property
    def name(self) -> str:
        return self.get('name')
