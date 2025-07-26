"""
Quick test to verify that the database import works from the dataLoader directory.
This mimics the exact context of loader.py
"""

try:
    print("🧪 Testing database import from dataLoader context...")
    
    # This is the exact import used in loader.py
    from ..database import get_engine
    
    print("✅ Import successful: 'from ..database import get_engine'")
    
    # This is the exact line from loader.py
    engine = get_engine()
    
    print("✅ Engine creation successful: 'engine = get_engine()'")
    
    # Test the connection
    from sqlalchemy import text
    with engine.connect() as conn:
        result = conn.execute(text("SELECT 1"))
        test_value = result.fetchone()[0]
        assert test_value == 1
    
    print("✅ Database connection successful")
    print("\n🎉 SUCCESS! Your loader.py 'engine = get_engine()' line will work perfectly!")
    
except Exception as e:
    print(f"❌ Error: {e}")
    print("\n💡 This means there might be an issue with the import or database connection.")
