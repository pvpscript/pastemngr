import sys

from connection import Connect

class Database:
    def __init__(self):
        self.connection = Connect.get_instance().get_connection()
        self.cursor = self.connection.cursor()

class User(Database):
    # Default operations
    CREATE = """
        INSERT INTO user
        (user_name, user_key, user_format_short, user_expiration,
        user_avatar_url, user_private, user_website, user_email, user_location,
        user_account_type)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
    """
    READ = """
        SELECT * FROM user
        WHERE (user_name = ?);
    """
    UPDATE = """
        UPDATE user
        SET user_key = ?, user_format_short = ?, user_expiration = ?,
        user_avatar_url = ?, user_private = ?, user_website = ?,
        user_email = ?, user_location = ?, user_account_type = ?
        WHERE user_name = ?;
    """
    DELETE = """
        DELETE FROM user
        WHERE user_name = ?;
    """

    # Extra operations
    UPDATE_KEY = """
        UPDATE user
        SET user_key = ?
        WHERE user_name = ?;
    """
    ALL = """
        SELECT * FROM user;
    """

    def __init__(self):
        super().__init__()

    def create(self, user_name, user_key, user_format_short,
               user_expiration, user_avatar_url, user_private,
               user_website, user_email, user_location,
               user_account_type):
        try:
            self.cursor.execute(self.CREATE, (user_name, user_key,
                user_format_short, user_expiration, user_avatar_url,
                user_private, user_website, user_email, user_location,
                user_account_type))

            self.connection.commit()
        except Exception as e:
            print(f'An error occurred: {e}', file=sys.stderr)

            self.connection.rollback()



    def read(self, user_name):
        result = self.cursor.execute(self.READ, (user_name,)).fetchone()

        return dict(result) if result is not None else None

    def all(self):
        result = self.cursor.execute(self.ALL).fetchall()

        return [dict(e) for e in result] if result is not None else None


class PasteInfo(Database):
    # Default operations
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
    UPDATE = """
        UPDATE paste_info
        SET owner = ?, paste_date = ?, paste_size = ?, paste_expire_date = ?,
        paste_private = ?, paste_format_long = ?, paste_format_short = ?,
        paste_url = ?, paste_hits = ?
        WHERE paste_key = ?;
    """
    DELETE = """
        DELETE FROM paste_info
        WHERE paste_key = ?;
    """

    # Extra operations
    ALL = """
        SELECT * FROM paste_info;
    """

    def __init__(self):
        super().__init__()

    def create(self, paste_key, owner, paste_date, paste_size,
               paste_expire_date, paste_private, paste_format_long,
               paste_format_short, paste_url, paste_hits):
        try:
            self.cursor.execute(self.CREATE, (paste_key, owner,
                paste_date, paste_size, paste_expire_date, paste_private,
                paste_format_long, paste_format_short, paste_url, paste_hits))

            self.connection.commit()
        except Exception as e:
            print(f'An error occurred: {e}', file=sys.stderr)

            self.connection.rollback()


    def read(self, paste_key):
        result = self.cursor.execute(self.READ, (paste_key,)).fetchone()
        
        return dict(result) if result is not None else None

    def all(self):
        result = self.cursor.execute(self.ALL).fetchall()

        return [dict(e) for e in result] if result is not None else None

class PasteText(Database):
    # Default operations
    CREATE = """
        INSERT INTO paste_text (paste_key, paste)
        VALUES (?, ?);
    """
    READ = """
        SELECT * FROM paste_text
        WHERE (paste_key = ?);
    """
    UPDATE = """
        UPDATE paste_text
        SET paste = ?
        WHERE paste_key = ?;
    """
    DELETE = """
        DELETE FROM paste_text
        WHERE paste_key = ?;
    """

    # Extra operations
    ALL = """
        SELECT * FROM paste_text;
    """

    def __init__(self):
        super().__init__()

    def create(self, paste_key, paste):
        try:
            self.cursor.execute(self.CREATE, (paste_key, paste))

            self.connection.commit()
        except Exception as e:
            print(f'An error occurred: {e}', file=sys.stderr)

            self.connection.rollback()

    def read(self, paste_key):
        result = self.cursor.execute(self.READ, (paste_key,)).fetchone()

        return dict(result) if result is not None else None

    def all(self):
        result = self.cursor.execute(self.ALL).fetchall()

        return [dict(e) for e in result] if result is not None else None
