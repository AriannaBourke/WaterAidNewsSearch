from werkzeug.security import generate_password_hash

# Login adapted from https://github.com/CoreyMSchafer/code_snippets/tree/master/Python/Flask_Blog
# Login adapted from https://github.com/boh717/FlaskLogin-and-pymongo/tree/master/app


class User():
    """ User class for login authentication """

    def __init__(self, email):
        self.email = email

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.email

    def set_password(self, password):
        self.password = generate_password_hash(password)
