import pandas as pd

USERS_FILE = 'data/login_data/users.csv'


class UsersClass:
    def __init__(self, users_file):
        self.users_file = users_file
        self.__fetch_users()

    def __fetch_users(self):
        parsed_users = pd.read_csv(self.users_file, dtype='string')
        self.users = {user['username']: user['password']
                      for index, user in parsed_users.iterrows()}

    def add_user(self, username, password):
        with open(self.users_file, "a+") as uf:
            uf.write("\n")
            uf.write(f"{username},{password}")
        self.__fetch_users()

    def get_users(self):
        return self.users


Users = UsersClass(USERS_FILE)
