import os
from peewee import Model, CharField, DateTimeField, SqliteDatabase
from typing import Optional


base_dir = os.path.dirname(__file__)
db_path  = os.path.join(base_dir, 'databases', 'news', 'news_en.db')
db = SqliteDatabase(db_path)

class NewsDB(Model):
    """
        Model for storages news notes.

        Attributes:
            url (str): Uniq news URL .
            title (str): Title of news.
            description (str): Description  news.
            thumbnail (Optional[str]): Picture from the news page.
            createdat (datetime): Date and time when the news was created.
    """
    url = CharField(unique=True)
    title = CharField()
    description = CharField()
    thumbnail = CharField(null=True)
    createdat = DateTimeField()

    class Meta:
        database = db

def initialize_NewsDB( ) -> None:
    """
        Connects to the database News_DB and creates table, if it doesn't exist.
    """
    db.connect()
    db.create_tables([NewsDB], safe=True)
    db.close()

if __name__ == "__main__":
    initialize_NewsDB()
