from src.common.database import Database
from src.common.utils1 import Utils

Database.initialize()
Database.insert('date',{"date":Utils.current_time()})