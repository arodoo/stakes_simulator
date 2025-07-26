# Tests Directory

This directory contains tests to verify that the database connection and module imports are working correctly in the vehicle emulator project.

## 📁 Test Files

### `test_loader_import.py`
Tests the exact import pattern used in `loader.py` to ensure the centralized database connection is working properly.

## 🚀 How to Run Tests

### Option 1: Run from Tests Directory (Recommended)

1. **Open terminal/command prompt**
2. **Navigate to the tests directory:**
   ```bash
   cd e:\01Projects\01Python\vehicle_emulator\vehicle_emulator\tests
   ```
3. **Run the test:**
   ```bash
   python test_loader_import.py
   ```

### Option 2: Run from Project Root

1. **Open terminal/command prompt**
2. **Navigate to the project root:**
   ```bash
   cd e:\01Projects\01Python\vehicle_emulator\vehicle_emulator
   ```
3. **Run the test:**
   ```bash
   python tests/test_loader_import.py
   ```

### Option 3: Run from VS Code

1. **Open the test file** (`test_loader_import.py`) in VS Code
2. **Right-click in the editor** and select "Run Python File in Terminal"
3. **Or use Ctrl+F5** to run the file

## 📊 Understanding Test Results

### ✅ Success Output
When everything is working correctly, you'll see:
```
🧪 Testing loader.py import pattern...
========================================
1. Testing import: 'from database import get_engine'
   ✅ Import successful
2. Testing: 'engine = get_engine()'
   ✅ Engine creation successful
3. Testing engine properties...
   ✅ Engine has required methods
4. Testing actual database connection...
   ✅ Database connection successful

========================================
🎉 SUCCESS! The loader.py import pattern works correctly!
   'engine = get_engine()' is functioning properly.

✨ Your loader.py should work without issues!
```

### ❌ Failure Scenarios

#### Import Error
```
❌ Import Error: No module named 'database'

💡 Possible solutions:
   - Check if database module files exist
   - Verify __init__.py files are present
```

**Solution:** Make sure the `database/` folder exists with `__init__.py` and `connection.py` files.

#### Connection Error
```
❌ Connection Error: (2003, "Can't connect to MySQL server on 'localhost'")

💡 Possible solutions:
   - Check if MySQL server is running
   - Verify database credentials
   - Ensure 'stakes' database exists
```

**Solutions:**
1. **Start MySQL server** (if not running)
2. **Check credentials** in `database/connection.py`
3. **Create database** if it doesn't exist:
   ```sql
   CREATE DATABASE stakes;
   ```

## 🔧 What Each Test Validates

### 1. Import Test
- Verifies that `from database import get_engine` works
- Ensures the database module is properly structured
- Confirms Python can find and load the module

### 2. Engine Creation Test
- Tests that `engine = get_engine()` executes without errors
- Validates the SQLAlchemy engine is created properly
- Checks that database configuration is loaded correctly

### 3. Engine Properties Test
- Ensures the engine has required SQLAlchemy methods
- Validates that the engine object is properly formed
- Tests that `connect()` and `begin()` methods are available

### 4. Database Connection Test
- Performs an actual connection to the MySQL database
- Executes a simple SQL query (`SELECT 1`)
- Verifies end-to-end database connectivity

## 🛠️ Troubleshooting

### Common Issues and Solutions

1. **"No module named 'database'"**
   - Ensure you're running from the correct directory
   - Check that `database/__init__.py` exists
   - Verify the Python path is correct

2. **"Can't connect to MySQL server"**
   - Start your MySQL service
   - Check if MySQL is running on localhost:3306
   - Verify your MySQL credentials

3. **"Access denied for user 'root'"**
   - Check your MySQL username/password
   - Update credentials in `database/connection.py`
   - Or set environment variables

4. **"Unknown database 'stakes'"**
   - Create the database: `CREATE DATABASE stakes;`
   - Or update the database name in configuration

## 🔒 Environment Variables (Optional)

You can override default database settings using environment variables:

```bash
# Set environment variables (Windows)
set DB_HOST=localhost
set DB_USERNAME=your_user
set DB_PASSWORD=your_password
set DB_DATABASE=your_database

# Set environment variables (Linux/Mac)
export DB_HOST=localhost
export DB_USERNAME=your_user
export DB_PASSWORD=your_password
export DB_DATABASE=your_database
```

## 📝 Adding New Tests

To create additional tests:

1. **Create a new Python file** in this directory
2. **Follow the naming convention:** `test_*.py`
3. **Import required modules** at the top
4. **Add path configuration** if needed:
   ```python
   import sys
   import os
   sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
   ```
5. **Write test functions** with descriptive names
6. **Add proper error handling** and user-friendly messages

## 🎯 When to Run Tests

- **Before running loader.py** - to ensure database connection works
- **After modifying database configuration** - to verify changes work
- **When setting up a new environment** - to validate the setup
- **When troubleshooting connection issues** - to isolate problems
- **After database credential changes** - to confirm new settings

## 📞 Need Help?

If tests are failing and you can't resolve the issues:

1. **Check the error messages** - they usually indicate the problem
2. **Verify MySQL is running** - restart if necessary
3. **Check database credentials** - ensure they're correct
4. **Review the database module files** - ensure they exist and are properly formatted
5. **Try running from different directories** - path issues are common

Remember: These tests are designed to catch problems early before they affect your main application!
