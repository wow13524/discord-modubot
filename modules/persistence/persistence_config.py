from modubot import PropertyDict

class PersistenceConfig(PropertyDict):
    db_name: str = "data.db"
    write_ahead_logging: bool = True