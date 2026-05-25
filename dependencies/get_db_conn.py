from storage.database import Database

db = Database()

def get_db_conn():
    with db.transaction() as conn:
        yield conn