"""
Test runner for database connection tests.
Run this file to test if the database connection is working.
"""
import os
import sys

def main():
    """Main test runner function."""
    print("🚀 Vehicle Emulator Database Connection Test Suite")
    print("=" * 60)
    
    # Test 1: Simple loader import test
    print("\n📋 Test 1: Loader Import Pattern")
    print("-" * 30)
    
    try:
        from test_loader_import import test_loader_import
        success1 = test_loader_import()
    except Exception as e:
        print(f"❌ Failed to run loader import test: {e}")
        success1 = False
    
    # Test 2: Comprehensive database tests
    print("\n📋 Test 2: Comprehensive Database Tests")
    print("-" * 40)
    
    try:
        from test_database_connection import run_manual_tests
        success2 = run_manual_tests()
    except Exception as e:
        print(f"❌ Failed to run database tests: {e}")
        success2 = False
    
    # Final results
    print("\n" + "=" * 60)
    print("📊 TEST RESULTS SUMMARY")
    print("=" * 60)
    
    if success1 and success2:
        print("🎉 ALL TESTS PASSED!")
        print("✅ Your database connection setup is working correctly.")
        print("✅ loader.py should work without issues.")
    elif success1:
        print("⚠️  PARTIAL SUCCESS")
        print("✅ Loader import works")
        print("❌ Database connection has issues")
    elif success2:
        print("⚠️  PARTIAL SUCCESS") 
        print("❌ Loader import has issues")
        print("✅ Database connection works")
    else:
        print("❌ ALL TESTS FAILED")
        print("🔧 Please check your database configuration and setup.")
    
    print("\n💡 Next steps:")
    if success1 and success2:
        print("   - You can now run your loader.py safely")
        print("   - The centralized database connection is ready to use")
    else:
        print("   - Fix the database connection issues")
        print("   - Ensure MySQL server is running")
        print("   - Verify database credentials in database/connection.py")
        print("   - Check if 'stakes' database exists")


if __name__ == "__main__":
    main()
