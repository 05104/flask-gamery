class Game:
    def __init__(self, name, category, console, id=None, created_at=None):
        self.id = id
        self.name = name
        self.category = category
        self.console = console
        self.created_at = created_at
