class Spider(dict):
    @property
    def name(self) -> str:
        return self.get('name')
