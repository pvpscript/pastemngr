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

        return dict(result) if result is not None else None

    def all(self):
        result = self.cursor.execute(self.ALL).fetchall()

        return [dict(e) for e in result] if result is not None else None


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
        
        return dict(result) if result is not None else None

    def all(self):
        result = self.cursor.execute(self.ALL).fetchall()

        return [dict(e) for e in result] if result is not None else None

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

        return dict(result) if result is not None else None

    def all(self):
        result = self.cursor.execute(self.ALL).fetchall()

        return [dict(e) for e in result] if result is not None else None
