import os
import sys

# Add parent directory to Python path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from database.connection import get_engine
    from services import (
        DatabaseSchemaService, 
        DataCleaningService,
        DataInsertionService,
        ExcelLoaderService,
        SqlExportService
    )
    print("All modules imported successfully")
except ImportError as e:
    print(f"Import error: {e}")
    sys.exit(1)

# Configuration
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
SHARE_DIR = os.path.join(BASE_DIR, 'share')
SQL_DIR = os.path.join(SHARE_DIR, 'SQL')
TABLE_NAMES = ['map', 'centerpos2x', 'bamboopattern', 'largescreenpixelpos']

try:
    # Initialize services
    engine = get_engine()
    schema_service = DatabaseSchemaService(engine)
    cleaning_service = DataCleaningService()
    insertion_service = DataInsertionService(engine)
    excel_service = ExcelLoaderService(SHARE_DIR)
    sql_export_service = SqlExportService(SQL_DIR)
    
    print("Starting data loading process...")
    
    # Step 1: Drop existing tables
    print("Dropping existing tables...")
    schema_service.drop_tables_if_exist(TABLE_NAMES)
    
    # Step 2: Create fresh tables
    print("Creating tables...")
    schema_service.create_tables()
    
    # Step 3: Load Excel data
    dataframes = excel_service.load_all_files()
    
    # Step 4: Clean data
    print("Cleaning data...")
    dataframes['map'] = cleaning_service.clean_map_data(dataframes['map'])
    dataframes['centerpos2x'] = cleaning_service.clean_centerpos2x_data(dataframes['centerpos2x'])
    dataframes['bamboopattern'] = cleaning_service.clean_bamboopattern_data(dataframes['bamboopattern'])
    dataframes['largescreenpixelpos'] = cleaning_service.clean_largescreenpixelpos_data(dataframes['largescreenpixelpos'])
    
    # Step 5: Insert data
    print("Inserting data...")
    insertion_service.insert_all_data(dataframes)
    
    # Step 6: Export SQL files with versioning
    print("Generating SQL export files...")
    version_dir = sql_export_service.export_all_data_as_sql(dataframes)
    
    print("Carga completada sin pérdidas.")
    print(f"Archivos SQL exportados en: {version_dir}")
    
except Exception as e:
    print(f"Error during execution: {e}")
    import traceback
    traceback.print_exc()
