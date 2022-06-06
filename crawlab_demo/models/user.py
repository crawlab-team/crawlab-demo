import os
from typing import List, Optional

from crawlab.config import get_spider_config, SpiderConfig

from crawlab_demo.models.schedule import Schedule


class User(dict):
    @property
    def username(self) -> str:
        return self.get('username')

    @property
    def password(self) -> str:
        return self.get('password')

    @property
    def role(self) -> str:
        return self.get('role')

    @property
    def email(self) -> str:
        return self.get('email')
