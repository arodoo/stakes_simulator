# Database Module

This module provides a centralized database connection configuration for the vehicle emulator application.

## Features

- Single source of truth for database connections
- Environment variable support for configuration
- Singleton pattern for efficient connection reuse
- Easy configuration updates at runtime
- Support for connection pooling and health checks

## Usage

### Basic Usage

```python
from database import get_engine, get_connection

# Get engine instance
engine = get_engine()

# Use with pandas
import pandas as pd
df = pd.read_sql("SELECT * FROM map", engine)

# Use with SQLAlchemy transactions
from sqlalchemy import text
with engine.begin() as conn:
    result = conn.execute(text("SELECT COUNT(*) FROM map"))
    count = result.fetchone()[0]
```

### Direct Connection

```python
from database import get_connection

with get_connection() as conn:
    # Use connection directly
    df = pd.read_sql("SELECT * FROM map LIMIT 10", conn)
```

### Configuration

#### Environment Variables

Create a `.env` file in your project root:

```env
DB_HOST=localhost
DB_PORT=3306
DB_USERNAME=your_username
DB_PASSWORD=your_password
DB_DATABASE=your_database
DB_CHARSET=utf8mb4
```

#### Runtime Configuration

```python
from database import update_config, get_engine

# Update configuration
update_config(
    host='localhost',
    database='stakes',
    username='root',
    password='root'
)

# Get engine with new configuration
engine = get_engine()
```

## Configuration Parameters

- `DB_HOST`: Database host (default: localhost)
- `DB_PORT`: Database port (default: 3306)
- `DB_USERNAME`: Database username (default: root)
- `DB_PASSWORD`: Database password (default: root)
- `DB_DATABASE`: Database name (default: stakes)
- `DB_CHARSET`: Database charset (default: utf8mb4)

## Files

- `connection.py`: Main database connection module
- `__init__.py`: Module initialization and exports
- `example_usage.py`: Usage examples
- `.env.example`: Example environment configuration file

## Migration from Direct Connections

If you have existing code using direct SQLAlchemy connections:

**Before:**
```python
from sqlalchemy import create_engine
engine = create_engine("mysql+mysqlconnector://root:root@localhost/stakes")
```

**After:**
```python
from database import get_engine
engine = get_engine()
```

This ensures all parts of your application use the same connection configuration and can be updated centrally.
