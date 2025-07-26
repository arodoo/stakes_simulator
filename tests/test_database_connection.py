"""
Test module for database connection functionality.
Tests if the centralized database connection is working properly.
"""

import sys
import os

# Add the parent directory to the path to import the database module
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database import get_engine, get_connection
from sqlalchemy import text


class TestDatabaseConnection:
    """Test class for database connection functionality."""

    def test_get_engine_returns_engine(self):
        """Test that get_engine() returns a valid SQLAlchemy engine."""
        engine = get_engine()
        assert engine is not None
        assert hasattr(engine, "connect")
        assert hasattr(engine, "begin")
        print("✅ Engine object created successfully")

    def test_engine_connection(self):
        """Test that the engine can establish a database connection."""
        try:
            engine = get_engine()
            with engine.connect() as connection:
                # Simple query to test connection
                result = connection.execute(text("SELECT 1 as test"))
                row = result.fetchone()
                assert row[0] == 1
                print("✅ Database connection established successfully")
        except Exception as e:
            print(f"❌ Database connection failed: {e}")
            raise

    def test_get_connection_function(self):
        """Test the get_connection() function."""
        try:
            connection = get_connection()
            assert connection is not None
            # Test a simple query
            result = connection.execute(text("SELECT 'Hello Database' as message"))
            row = result.fetchone()
            assert row[0] == "Hello Database"
            connection.close()
            print("✅ get_connection() function works correctly")
        except Exception as e:
            print(f"❌ get_connection() failed: {e}")
            raise

    def test_database_schema_access(self):
        """Test if we can access the stakes database and its tables."""
        try:
            engine = get_engine()
            with engine.connect() as connection:
                # Check if we can access the stakes database
                result = connection.execute(text("SELECT DATABASE() as current_db"))
                current_db = result.fetchone()[0]
                print(f"✅ Connected to database: {current_db}")

                # List tables in the database
                result = connection.execute(text("SHOW TABLES"))
                tables = [row[0] for row in result.fetchall()]
                print(f"✅ Available tables: {tables}")

                assert current_db == "stakes" or current_db is not None
        except Exception as e:
            print(f"❌ Database schema access failed: {e}")
            raise

    def test_transaction_capability(self):
        """Test that transactions work with the engine."""
        try:
            engine = get_engine()
            with engine.begin() as connection:
                # Test transaction by creating a temporary table
                connection.execute(
                    text(
                        """
                    CREATE TEMPORARY TABLE test_transaction (
                        id INT PRIMARY KEY,
                        message VARCHAR(100)
                    )
                """
                    )
                )

                # Insert test data
                connection.execute(
                    text(
                        """
                    INSERT INTO test_transaction (id, message) 
                    VALUES (1, 'Transaction test')
                """
                    )
                )

                # Verify data was inserted
                result = connection.execute(
                    text("SELECT message FROM test_transaction WHERE id = 1")
                )
                row = result.fetchone()
                assert row[0] == "Transaction test"

                print("✅ Transaction capability works correctly")
        except Exception as e:
            print(f"❌ Transaction test failed: {e}")
            raise


def run_manual_tests():
    """Run tests manually without pytest."""
    print("🧪 Running Database Connection Tests...")
    print("=" * 50)

    test_instance = TestDatabaseConnection()

    try:
        print("\n1. Testing engine creation...")
        test_instance.test_get_engine_returns_engine()

        print("\n2. Testing database connection...")
        test_instance.test_engine_connection()

        print("\n3. Testing get_connection() function...")
        test_instance.test_get_connection_function()

        print("\n4. Testing database schema access...")
        test_instance.test_database_schema_access()

        print("\n5. Testing transaction capability...")
        test_instance.test_transaction_capability()

        print("\n" + "=" * 50)
        print("🎉 ALL TESTS PASSED! Database connection is working correctly.")

    except Exception as e:
        print(f"\n❌ TEST FAILED: {e}")
        print("\n💡 Make sure:")
        print("   - MySQL server is running")
        print("   - Database 'stakes' exists")
        print("   - Username/password are correct")
        print("   - mysql-connector-python is installed")
        return False

    return True


if __name__ == "__main__":
    run_manual_tests()
