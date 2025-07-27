"""
Excel file loader service.
Handles reading and loading Excel files from the share directory.
"""

import os
import pandas as pd
from typing import Dict


class ExcelLoaderService:
    """Service for loading Excel files into pandas DataFrames."""
    
    def __init__(self, share_dir: str):
        self.share_dir = share_dir
    
    def load_all_files(self) -> Dict[str, pd.DataFrame]:
        """Load all required Excel files."""
        files_config = {
            'map': 'map.xlsx',
            'centerpos2x': 'centerpos2x.xlsx',
            'bamboopattern': 'bamboopattern.xlsx',
            'largescreenpixelpos': 'largescreenpixelpos.xlsx'
        }
        
        dataframes = {}
        
        for table_name, filename in files_config.items():
            file_path = os.path.join(self.share_dir, filename)
            print(f"Loading {filename}...")
            dataframes[table_name] = pd.read_excel(file_path)
        
        print("All Excel files loaded successfully")
        return dataframes
