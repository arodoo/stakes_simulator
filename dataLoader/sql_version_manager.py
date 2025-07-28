"""
SQL Version Manager
Utility script to manage and apply SQL versions from the version history.
"""

import os
import sys

# Add parent directory to Python path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from database.connection import get_engine
    from services.sql_export_service import SqlExportService
    from sqlalchemy import text
except ImportError as e:
    print(f"Import error: {e}")
    sys.exit(1)


class SqlVersionManager:
    """Manager for applying SQL versions to the database."""
    
    def __init__(self):
        self.base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        self.sql_dir = os.path.join(self.base_dir, 'share', 'SQL')
        self.engine = get_engine()
        self.export_service = SqlExportService(self.sql_dir)
    
    def list_versions(self):
        """List all available versions."""
        versions = self.export_service.list_all_versions()
        if not versions:
            print("No versions found.")
            return
        
        print("Available versions:")
        for version in versions:
            version_path = os.path.join(self.sql_dir, version)            # Try to read metadata
            metadata_file = os.path.join(version_path, "version_info.sql")
            if os.path.exists(metadata_file):
                with open(metadata_file, 'r', encoding='utf-8') as f:
                    lines = f.readlines()[:4]  # Read first 4 lines
                    for line in lines:
                        if line.startswith('--'):
                            print(f"  {version}: {line.strip()[2:].strip()}")
                            break
            else:
                print(f"  {version}")
    
    def apply_version(self, version_name: str, confirm: bool = False):
        """Apply a specific version to the database."""
        version_path = os.path.join(self.sql_dir, version_name)
        
        if not os.path.exists(version_path):
            print(f"Version {version_name} not found.")
            return False
        
        # List SQL files in the version
        sql_files = [f for f in os.listdir(version_path) if f.endswith('.sql') and f != 'version_info.sql']
        
        if not sql_files:
            print(f"No SQL files found in version {version_name}")
            return False
        
        print(f"Version {version_name} contains the following SQL files:")
        for sql_file in sql_files:
            print(f"  - {sql_file}")
        
        if not confirm:
            response = input("Do you want to apply this version? (y/N): ")
            if response.lower() != 'y':
                print("Operation cancelled.")
                return False
        
        # Apply each SQL file
        try:
            with self.engine.begin() as conn:
                conn.execute(text("SET foreign_key_checks = 0;"))
                
                # First, clear existing data from all tables
                table_names = [sql_file.replace('.sql', '') for sql_file in sql_files]
                print("Clearing existing data from tables...")
                for table_name in table_names:
                    conn.execute(text(f"DELETE FROM {table_name}"))
                    print(f"  - Cleared table: {table_name}")
                
                # Then apply the SQL files
                for sql_file in sorted(sql_files):
                    sql_file_path = os.path.join(version_path, sql_file)
                    table_name = sql_file.replace('.sql', '')
                    
                    print(f"Applying {sql_file}...")
                    
                    # Read and execute SQL file
                    with open(sql_file_path, 'r', encoding='utf-8') as f:
                        sql_content = f.read()
                    
                    # Split by statements and execute each one
                    statements = [stmt.strip() for stmt in sql_content.split(';') if stmt.strip() and not stmt.strip().startswith('--')]
                    
                    for statement in statements:
                        if statement:
                            conn.execute(text(statement))
                
                conn.execute(text("SET foreign_key_checks = 1;"))
            
            print(f"Version {version_name} applied successfully!")
            return True
            
        except Exception as e:
            print(f"Error applying version {version_name}: {e}")
            return False
    
    def show_version_details(self, version_name: str):
        """Show detailed information about a version."""
        version_path = os.path.join(self.sql_dir, version_name)
        
        if not os.path.exists(version_path):
            print(f"Version {version_name} not found.")
            return
        
        # Show metadata
        metadata_file = os.path.join(version_path, "version_info.sql")
        if os.path.exists(metadata_file):
            print(f"=== Version {version_name} Details ===")
            with open(metadata_file, 'r', encoding='utf-8') as f:
                print(f.read())
        
        # List SQL files and their record counts
        sql_files = [f for f in os.listdir(version_path) if f.endswith('.sql') and f != 'version_info.sql']
        
        if sql_files:
            print("SQL Files:")
            for sql_file in sorted(sql_files):
                sql_file_path = os.path.join(version_path, sql_file)
                # Count INSERT statements as rough estimate of records
                with open(sql_file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    insert_count = content.count('INSERT INTO')
                    print(f"  - {sql_file} ({insert_count} INSERT statement{'s' if insert_count != 1 else ''})")


def main():
    """Main function for command line usage."""
    manager = SqlVersionManager()
    
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python sql_version_manager.py list                    - List all versions")
        print("  python sql_version_manager.py show <version>          - Show version details")
        print("  python sql_version_manager.py apply <version>         - Apply a version")
        print("  python sql_version_manager.py apply <version> --yes   - Apply without confirmation")
        return
    
    command = sys.argv[1]
    
    if command == "list":
        manager.list_versions()
    
    elif command == "show" and len(sys.argv) >= 3:
        version_name = sys.argv[2]
        manager.show_version_details(version_name)
    
    elif command == "apply" and len(sys.argv) >= 3:
        version_name = sys.argv[2]
        confirm = len(sys.argv) > 3 and sys.argv[3] == "--yes"
        manager.apply_version(version_name, confirm)
    
    else:
        print("Invalid command or missing arguments.")


if __name__ == "__main__":
    main()
