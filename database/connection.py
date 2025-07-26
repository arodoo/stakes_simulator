"""
Database connection configuration module.
Single source of truth for database connections across the application.
"""
import os
from sqlalchemy import create_engine
from typing import Optional


class DatabaseConfig:
    """Database configuration class to manage connection parameters."""
    
    def __init__(self):
        # Default configuration - can be overridden by environment variables
        self.host = os.getenv('DB_HOST', 'localhost')
        self.port = os.getenv('DB_PORT', '3306')
        self.username = os.getenv('DB_USERNAME', 'root')
        self.password = os.getenv('DB_PASSWORD', 'root')
        self.database = os.getenv('DB_DATABASE', 'stakes')
        self.charset = os.getenv('DB_CHARSET', 'utf8mb4')
        
    def get_connection_string(self) -> str:
        """Generate the database connection string."""
        return (f"mysql+mysqlconnector://{self.username}:{self.password}"
                f"@{self.host}:{self.port}/{self.database}?charset={self.charset}")


# Global configuration instance
_config = DatabaseConfig()
_engine: Optional[object] = None


def get_engine(pool_pre_ping: bool = True, **kwargs):
    """
    Get the SQLAlchemy engine instance.
    
    Args:
        pool_pre_ping (bool): Enable connection health checks
        **kwargs: Additional engine parameters
    
    Returns:
        SQLAlchemy engine instance
    """
    global _engine
    
    if _engine is None:
        connection_string = _config.get_connection_string()
        _engine = create_engine(
            connection_string,
            pool_pre_ping=pool_pre_ping,
            **kwargs
        )
    
    return _engine


def get_connection():
    """
    Get a database connection from the engine.
    
    Returns:
        Database connection object
    """
    engine = get_engine()
    return engine.connect()


def update_config(host: str = None, port: str = None, username: str = None, 
                 password: str = None, database: str = None, charset: str = None):
    """
    Update database configuration parameters.
    
    Args:
        host: Database host
        port: Database port
        username: Database username
        password: Database password
        database: Database name
        charset: Database charset
    """
    global _engine, _config
    
    # Reset engine to force recreation with new config
    _engine = None
    
    if host is not None:
        _config.host = host
    if port is not None:
        _config.port = port
    if username is not None:
        _config.username = username
    if password is not None:
        _config.password = password
    if database is not None:
        _config.database = database
    if charset is not None:
        _config.charset = charset
