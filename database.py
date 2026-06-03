
# MOCK DATABASES
users_db = []          # Stores: id, username, hashed_password
transactions_db = []   # Stores: id, amount, category, type, description, user_id

# A simple class to simulate auto-incrementing Primary Keys in a database
class DBIDGenerator:
    def __init__(self):
        self.user_id = 1
        self.transaction_id = 1

    def get_new_user_id(self):
        id = self.user_id
        self.user_id += 1
        return id

    def get_new_transaction_id(self):
        id = self.transaction_id
        self.transaction_id += 1
        return id

db_ids = DBIDGenerator()