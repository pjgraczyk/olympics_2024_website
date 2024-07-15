import pandas as pd
import sqlite3 as sq

class Database:
    def __init__(self):
        self.conn = sq.connect('database/olympics.db')
    
    def get_data(self, table_name: str) -> pd.DataFrame:
        return pd.read_sql(f"SELECT * FROM {table_name}", self.conn)

    def close(self):
        self.conn.close()