class UserModel():
    def __init__(self, user_id, user_login, user_email):
        self.id = user_id
        self.login = user_login
        self.email = user_email
    
    def toString(self):
        return f"user id: {self.id}, user login: {self.login}, user email: {self.login}"