import bcrypt

def security_hash_pwd(data_password):
    hashed = bcrypt.hashpw(data_password.encode('utf-8'), bcrypt.gensalt())
    return hashed.decode('utf-8')

def security_check_pwd(data_pwd, user_pwd):
    return bcrypt.checkpw(data_pwd.encode('utf-8'), user_pwd.encode('utf-8'))







