import os
from peewee import SqliteDatabase

def init_database(db_name: str) -> SqliteDatabase:
    """
    Initializes and returns an SQLite database object.

    Args:
        db_name (str): The name of the database file (for example, 'news.db').

    Returns:
        SQLiteDatabase: The database object associated with the specified file.
    """
    base_dir = os.path.dirname(__file__)
    db_path  = os.path.join(base_dir, db_name)
    return SqliteDatabase(db_path)