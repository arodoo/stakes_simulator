"""
Data insertion service.
Handles database insertion operations with proper transaction management.
"""

from sqlalchemy import text
import pandas as pd
from typing import Dict


class DataInsertionService:
    """Service for inserting cleaned data into database tables."""
    
    def __init__(self, engine):
        self.engine = engine
    
    def insert_all_data(self, dataframes: Dict[str, pd.DataFrame]) -> None:
        """Insert all dataframes into their respective tables."""
        table_order = ['map', 'centerpos2x', 'bamboopattern', 'largescreenpixelpos']
        
        with self.engine.begin() as conn:
            conn.execute(text("SET foreign_key_checks = 0;"))
            
            for table_name in table_order:
                if table_name in dataframes:
                    self._insert_data(conn, table_name, dataframes[table_name])
            
            conn.execute(text("SET foreign_key_checks = 1;"))
    
    def _insert_data(self, conn, table_name: str, df: pd.DataFrame) -> None:
        """Insert data into a specific table."""
        print(f"Inserting {len(df)} rows into {table_name}...")
        df.to_sql(
            table_name, 
            conn, 
            if_exists="append", 
            index=False, 
            chunksize=1000
        )
