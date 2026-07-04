class User:
    def __init__(
            self, username, pwd,  email, user_id: int | None = None
    ):
        self.username = username
        self.pwd = pwd
        self.email = email
        self.user_id = user_id

    @classmethod
    def create(cls, username, pwd, email):
        return cls(username, pwd, email)

    def __str__(self):
        return str({self.user_id, self.username, self.pwd, self.email})





