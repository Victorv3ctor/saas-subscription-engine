from database.transaction import transaction

from domains.user import User

from services.security import security_hash_pwd

from exceptions.user import UserNotFound

from repository.repository import(
    save_user, get_user_by_id, get_user_by_username
)

def new_user(data_username, data_password, data_email):
    with transaction() as conn:
        hashed_pwd = security_hash_pwd(data_password)
        user = User.create(data_username, hashed_pwd, data_email)
        save_user(conn, user)
        return user

def user_query_by_id(user_id):
    with transaction() as conn:
        user = get_user_by_id(conn, user_id)
        if not user:
            raise UserNotFound()
        return user

def user_query_by_username(data_username):
    with transaction() as conn:
        user = get_user_by_username(conn, data_username)
        if not user:
            raise UserNotFound()
        return user