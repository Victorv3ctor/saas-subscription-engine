from fastapi import Depends
from dependencies.get_repo import get_repo
from service.service import Service

def get_service(repo=Depends(get_repo)):
    return Service(repo)