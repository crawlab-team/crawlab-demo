class Schedule(dict):
    @property
    def name(self) -> str:
        return self.get('name')

    @property
    def description(self) -> str:
        return self.get('description')

    @property
    def cron(self) -> str:
        return self.get('cron')

    @property
    def enabled(self) -> bool:
        return self.get('enabled')

    @property
    def mode(self) -> str:
        return self.get('mode')
