from fastapi import Depends
from repository.repository import Repository
from dependencies.get_db_conn import get_db_conn

def get_repo(conn=Depends(get_db_conn)):
    return Repository(conn)