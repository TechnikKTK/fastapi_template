from sqlalchemy import Engine
from sqlalchemy.orm import sessionmaker

from app.utils.patterns.singleton import SingletonMeta


class SyncPgEngine(metaclass=SingletonMeta):

    def __init__(self, engine: Engine):
        self.engine = engine
        self.session_class = sessionmaker(self.engine)
