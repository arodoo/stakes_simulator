"""
SQL Export Service.
Handles generation of SQL files from dataframes with versioning support.
"""

import os
import pandas as pd
from datetime import datetime
from typing import Dict
import re


class SqlExportService:
    """Service for exporting dataframes as SQL INSERT statements with versioning."""
    
    def __init__(self, base_sql_dir: str):
        self.base_sql_dir = base_sql_dir
    
    def export_all_data_as_sql(self, dataframes: Dict[str, pd.DataFrame]) -> str:
        """
        Export all dataframes as SQL files with versioning.
        Returns the version directory path.
        """
        # Create version directory
        version_dir = self._create_version_directory()
        
        # Export each table as SQL
        for table_name, df in dataframes.items():
            self._export_table_as_sql(df, table_name, version_dir)
        
        print(f"SQL files exported to: {version_dir}")
        return version_dir
    
    def _create_version_directory(self) -> str:
        """Create a new version directory based on timestamp."""
        # Get current timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Find existing version directories
        existing_versions = []
        if os.path.exists(self.base_sql_dir):
            for item in os.listdir(self.base_sql_dir):
                if os.path.isdir(os.path.join(self.base_sql_dir, item)):
                    # Extract version number if it follows V{number} pattern
                    match = re.match(r'V(\d+)', item)
                    if match:
                        existing_versions.append(int(match.group(1)))
        
        # Determine next version number
        next_version = max(existing_versions, default=0) + 1
        
        # Create version directory
        version_dir = os.path.join(self.base_sql_dir, f"V{next_version}_{timestamp}")
        os.makedirs(version_dir, exist_ok=True)
        
        # Create metadata file
        self._create_metadata_file(version_dir, next_version, timestamp)
        
        return version_dir
    
    def _create_metadata_file(self, version_dir: str, version: int, timestamp: str) -> None:
        """Create a metadata file with version information."""
        metadata_content = f"""-- Version: V{version}
-- Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
-- Timestamp: {timestamp}
-- Description: Automated SQL export from Excel data loading process
"""
        metadata_path = os.path.join(version_dir, "version_info.sql")
        with open(metadata_path, 'w', encoding='utf-8') as f:
            f.write(metadata_content)
    
    def _export_table_as_sql(self, df: pd.DataFrame, table_name: str, version_dir: str) -> None:
        """Export a single dataframe as SQL INSERT statements."""
        sql_file_path = os.path.join(version_dir, f"{table_name}.sql")
        
        with open(sql_file_path, 'w', encoding='utf-8') as f:
            # Write header
            f.write(f"-- SQL INSERT statements for table: {table_name}\n")
            f.write(f"-- Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"-- Records: {len(df)}\n\n")
            
            # Write table cleanup (optional, commented out since tables are immutable)
            f.write(f"-- DELETE FROM {table_name}; -- Uncomment if you want to clear existing data\n\n")
            
            if len(df) > 0:
                # Generate INSERT statements
                columns = list(df.columns)
                columns_str = ', '.join([f"`{col}`" for col in columns])
                
                # Process data in chunks for better performance
                chunk_size = 100
                for i in range(0, len(df), chunk_size):
                    chunk = df.iloc[i:i+chunk_size]
                    
                    f.write(f"INSERT INTO `{table_name}` ({columns_str}) VALUES\n")
                    
                    values_list = []
                    for _, row in chunk.iterrows():
                        value_parts = []
                        for col in columns:
                            value = row[col]
                            if pd.isna(value):
                                value_parts.append("NULL")
                            elif isinstance(value, str):
                                # Escape single quotes and wrap in quotes
                                escaped_value = value.replace("'", "''")
                                value_parts.append(f"'{escaped_value}'")
                            elif isinstance(value, (int, float)):
                                value_parts.append(str(value))
                            else:
                                # Convert to string and escape
                                escaped_value = str(value).replace("'", "''")
                                value_parts.append(f"'{escaped_value}'")
                        
                        values_list.append(f"({', '.join(value_parts)})")
                    
                    f.write(',\n'.join(values_list))
                    f.write(';\n\n')
            else:
                f.write(f"-- No data to insert for table {table_name}\n\n")
        
        print(f"Generated SQL file: {sql_file_path} ({len(df)} records)")
    
    def get_latest_version_dir(self) -> str:
        """Get the path to the latest version directory."""
        if not os.path.exists(self.base_sql_dir):
            return None
            
        version_dirs = []
        for item in os.listdir(self.base_sql_dir):
            if os.path.isdir(os.path.join(self.base_sql_dir, item)):
                match = re.match(r'V(\d+)', item)
                if match:
                    version_dirs.append((int(match.group(1)), item))
        
        if version_dirs:
            version_dirs.sort(key=lambda x: x[0], reverse=True)
            latest_dir = version_dirs[0][1]
            return os.path.join(self.base_sql_dir, latest_dir)
        
        return None
    
    def list_all_versions(self) -> list:
        """List all existing version directories."""
        if not os.path.exists(self.base_sql_dir):
            return []
            
        versions = []
        for item in os.listdir(self.base_sql_dir):
            if os.path.isdir(os.path.join(self.base_sql_dir, item)):
                match = re.match(r'V(\d+)', item)
                if match:
                    versions.append(item)
        
        versions.sort()
        return versions
