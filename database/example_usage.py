"""
Example usage of the centralized database connection module.
This demonstrates how to use the database connection from any part of the application.
"""
import pandas as pd
from sqlalchemy import text
from database import get_engine, get_connection, update_config


def example_query_with_engine():
    """Example using the engine directly."""
    engine = get_engine()
    
    with engine.begin() as conn:
        result = conn.execute(text("SELECT COUNT(*) as total FROM map"))
        count = result.fetchone()
        print(f"Total records in map table: {count[0]}")


def example_query_with_connection():
    """Example using a direct connection."""
    with get_connection() as conn:
        df = pd.read_sql("SELECT * FROM map LIMIT 5", conn)
        print("First 5 records from map table:")
        print(df)


def example_update_config():
    """Example of updating database configuration at runtime."""
    # Update configuration if needed
    update_config(
        host='localhost',
        database='stakes',
        username='root',
        password='root'
    )
    
    # Now get engine with new configuration
    engine = get_engine()
    print(f"Engine created with updated configuration")


if __name__ == "__main__":
    example_query_with_engine()
    example_query_with_connection()
    example_update_config()
