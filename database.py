from connection import Connect

class Database:
    def __init__(self):
        self.connection = Connect.get_instance().get_connection()
        self.cursor = self.connection.cursor()

class User(Database):
    CREATE = """
        INSERT INTO user
        (username, user_key, user_format_short, user_expiration,
        user_avatar_url, user_private, user_website, user_email, user_location,
        user_account_type)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
    """
    READ = """
        SELECT * FROM user
        WHERE (username = ?);
    """
    ALL = """
        SELECT * FROM user;
    """

    def __init__(self):
        super().__init__()

    def create(self, username, user_key, user_format_short,
               user_expiration, user_avatar_url, user_private,
               user_website, user_email, user_location,
               user_account_type):
        self.cursor.execute(self.CREATE, (username, user_key,
            user_format_short, user_expiration, user_avatar_url,
            user_private, user_website, user_email, user_location,
            user_account_type))            

    def read(self, username):
        result = self.cursor.execute(self.READ, (username,)).fetchone()

        return {
                'username': result['username'],
                'user_key': result['user_key'],
                'user_format_short': result['user_format_short'],
                'user_expiration': result['user_expiration'],
                'user_avatar_url': result['user_avatar_url'],
                'user_private': result['user_private'],
                'user_website': result['user_website'],
                'user_email': result['user_email'],
                'user_location': result['user_location'],
                'user_account_type': result['user_account_type']
        }

    def all(self):
        result = self.cursor.execute(self.ALL).fetchall()
        res_list = []

        for entry in result:
            res_list.append({
                'username': entry['username'],
                'user_key': entry['user_key'],
                'user_format_short': entry['user_format_short'],
                'user_expiration': entry['user_expiration'],
                'user_avatar_url': entry['user_avatar_url'],
                'user_private': entry['user_private'],
                'user_website': entry['user_website'],
                'user_email': entry['user_email'],
                'user_location': entry['user_location'],
                'user_account_type': entry['user_account_type']
            })

        return res_list


class PasteInfo(Database):
    CREATE = """
        INSERT INTO paste_info
        (paste_key, owner, paste_date, paste_size, paste_expire_date,
        paste_private, paste_format_long, paste_format_short, paste_url,
        paste_hits)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
    """
    READ = """
        SELECT * FROM paste_info
        WHERE (paste_key = ?);
    """
    ALL = """
        SELECT * FROM paste_info;
    """

    def __init__(self):
        super().__init__()

    def create(self, paste_key, owner, paste_date, paste_size,
               paste_expire_date, paste_private, paste_format_long,
               paste_format_short, paste_url, paste_hits):
        self.cursor.execute(self.CREATE, (paste_key, owner,
            paste_date, paste_size, paste_expire_date, paste_private,
            paste_format_long, paste_format_short, paste_url, paste_hits))

    def read(self, paste_key):
        result = self.cursor.execute(self.READ, (paste_key,)).fetchone()

        return {
                'paste_key': result['paste_key'],
                'owner': result['owner'],
                'paste_date': result['paste_date'],
                'paste_size': result['paste_size'],
                'paste_expire_date': result['paste_expire_date'],
                'paste_private': result['paste_private'],
                'paste_format_long': result['paste_format_long'],
                'paste_format_short': result['paste_format_short'],
                'paste_url': result['paste_url'],
                'paste_hits': result['paste_hits']
        }

    def all(self):
        result = self.cursor.execute(self.ALL).fetchall()
        res_list = []

        for entry in result:
            res_list.append({
                'paste_key': entry['paste_key'],
                'owner': entry['owner'],
                'paste_date': entry['paste_date'],
                'paste_size': entry['paste_size'],
                'paste_expire_date': entry['paste_expire_date'],
                'paste_private': entry['paste_private'],
                'paste_format_long': entry['paste_format_long'],
                'paste_format_short': entry['paste_format_short'],
                'paste_url': entry['paste_url'],
                'paste_hits': entry['paste_hits']
            })

        return res_list

class PasteText(Database):
    CREATE = """
        INSERT INTO paste_text (paste_key, paste)
        VALUES (?, ?);
    """
    READ = """
        SELECT * FROM paste_text
        WHERE (paste_key = ?);
    """
    ALL = """
        SELECT * FROM paste_text;
    """

    def __init__(self):
        super().__init__()

    def create(self, paste_key, paste):
        self.cursor.execute(self.CREATE, (paste_key, paste))

    def read(self, paste_key):
        result = self.cursor.execute(self.READ, (paste_key,)).fetchone()

        return {
                'paste_key': result['paste_key'],
                'paste': result['paste']
        }

    def all(self):
        result = self.cursor.execute(self.ALL).fetchall()
        res_list = []

        for entry in result:
            res_list.append({
                'paste_key': entry['paste_key'],
                'paste': entry['paste']
            })

        return res_list
