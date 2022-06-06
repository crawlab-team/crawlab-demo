import os
from typing import List, Optional

from crawlab.config import get_spider_config, SpiderConfig

from crawlab_demo.models.schedule import Schedule


class Spider(dict):
    @property
    def path(self) -> str:
        return self.get('path')

    @property
    def dir_path(self) -> str:
        return os.path.join(os.path.dirname(__file__), f'../data/spiders/{self.path}')

    @property
    def schedules(self) -> Optional[List[Schedule]]:
        if not self.get('schedules'):
            return
        return list(map(lambda sch: Schedule(sch), self.get('schedules')))

    @property
    def config(self) -> SpiderConfig:
        return get_spider_config(self.dir_path)

    @property
    def name(self) -> str:
        return self.config.name

    @property
    def description(self) -> str:
        return self.config.description
