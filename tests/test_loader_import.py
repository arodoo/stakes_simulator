"""
Simple test to verify that 'engine = get_engine()' works from the loader module.
This test mimics exactly what happens in the loader.py file.
"""

import sys
import os

# Add the parent directory to the path to import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def test_loader_import():
    """Test the exact import pattern used in loader.py"""
    print("🧪 Testing loader.py import pattern...")
    print("=" * 40)

    try:
        # Test the exact import from loader.py
        print("1. Testing import: 'from database import get_engine'")
        from database import get_engine

        print("   ✅ Import successful")

        print("2. Testing: 'engine = get_engine()'")
        engine = get_engine()
        print("   ✅ Engine creation successful")

        print("3. Testing engine properties...")
        assert engine is not None
        assert hasattr(engine, "connect")
        assert hasattr(engine, "begin")
        print("   ✅ Engine has required methods")

        print("4. Testing actual database connection...")
        with engine.connect() as conn:
            from sqlalchemy import text

            result = conn.execute(text("SELECT 1"))
            test_value = result.fetchone()[0]
            assert test_value == 1
        print("   ✅ Database connection successful")

        print("\n" + "=" * 40)
        print("🎉 SUCCESS! The loader.py import pattern works correctly!")
        print("   'engine = get_engine()' is functioning properly.")

        return True

    except ImportError as e:
        print(f"   ❌ Import Error: {e}")
        print("\n💡 Possible solutions:")
        print("   - Check if database module files exist")
        print("   - Verify __init__.py files are present")
        return False

    except Exception as e:
        print(f"   ❌ Connection Error: {e}")
        print("\n💡 Possible solutions:")
        print("   - Check if MySQL server is running")
        print("   - Verify database credentials")
        print("   - Ensure 'stakes' database exists")
        return False


if __name__ == "__main__":
    success = test_loader_import()
    if success:
        print("\n✨ Your loader.py should work without issues!")
    else:
        print("\n🔧 Please fix the issues above before running loader.py")
