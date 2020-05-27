import sys

import pastemngr
import pastemngr.db.connection as con

class DatabaseError(Exception):
    """An ambiguous database error occurred."""

    def __init__(self, msg, orig_exception):
        super().__init__(f'{msg}: {orig_exception}')
        self.orig_exception = orig_exception

class CreationError(DatabaseError):
    """An error occurred during table creation"""

class ReadError(DatabaseError):
    """An error occurred during table read"""

class UpdateError(DatabaseError):
    """An error occurred during table update"""

class DeleteError(DatabaseError):
    """An error occurred during table delete"""

class Database:
    def __init__(self):
        try:
            self.connection = con.Connect.get_connection()
            self.cursor = self.connection.cursor()
        except con.ConnectionError as e:
            raise DatabaseError('Unable to connect', e)

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
        SET user_format_short = ?, user_expiration = ?, user_avatar_url = ?,
        user_private = ?, user_website = ?, user_email = ?, user_location = ?,
        user_account_type = ?
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
    LIST_USER_PASTES= """
        SELECT *
        FROM paste_info
        WHERE owner = ?
        ORDER BY paste_date ASC;
    """

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
            self.connection.rollback()

            raise CreateError('An error occurred during user creation', e)
        finally:
            return self.cursor.rowcount

    def read(self, user_name):
        try:
            result = self.cursor.execute(self.READ, (user_name,)).fetchone()

            return dict(result) if result is not None else None
        except Exception as e:
            raise ReadError('An error occurred during user read', e)

    def update(self, user_name, user_format_short, user_expiration,
               user_avatar_url, user_private, user_website, user_email,
               user_location, user_account_type):
        try:
            self.cursor.execute(self.UPDATE, (user_format_short,
                    user_expiration, user_avatar_url, user_private,
                    user_website, user_email, user_location, user_account_type,
                    user_name))

            self.connection.commit()
        except Exception as e:
            self.connection.rollback()

            raise UpdateError('An error occurred during user update', e)
        finally:
            return self.cursor.rowcount

    def delete(self, user_name):
        try:
            self.cursor.execute(self.DELETE, (user_name,))
            
            self.connection.commit()
        except Exception as e:
            self.connection.rollback()

            raise DeleteException('An error occurred during user deletion', e)
        finally:
            return self.cursor.rowcount

    def update_key(self, user_name, user_key):
        try:
            self.cursor.execute(self.UPDATE_KEY, (user_key, user_name))

            self.connection.commit()
        except Exception as e:
            self.connection.rollback()

            raise UpdateError('An error occurred while updating user key', e)
        finally:
            return self.cursor.rowcount

    def list_user_pastes(self, user_name):
        try:
            result = self.cursor.execute(self.LIST_USER_PASTES, (user_name,))

            return [dict(e) for e in result] if result is not None else None
        except Exception as e:
            raise ReadError('An error occurred while reading user pastes', e)

    def all(self):
        try:
            result = self.cursor.execute(self.ALL).fetchall()

            return [dict(e) for e in result] if result is not None else None
        except Exception as e:
            raise ReadError('An error occurred while retrieving all users', e)



class PasteInfo(Database):
    # Default operations
    CREATE = """
        INSERT INTO paste_info
        (paste_key, owner, paste_date, paste_title, paste_size, paste_expire_date,
        paste_private, paste_format_long, paste_format_short, paste_url,
        paste_hits)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
    """
    READ = """
        SELECT * FROM paste_info
        WHERE (paste_key = ?);
    """
    UPDATE = """
        UPDATE paste_info
        SET paste_date = ?, paste_title = ?, paste_size = ?,
        paste_expire_date = ?, paste_private = ?, paste_format_long = ?,
        paste_format_short = ?, paste_url = ?, paste_hits = ?
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

    def create(self, paste_key, owner, paste_date, paste_title, paste_size,
               paste_expire_date, paste_private, paste_format_long,
               paste_format_short, paste_url, paste_hits):
        try:
            self.cursor.execute(self.CREATE, (paste_key, owner,
                paste_date, paste_title, paste_size, paste_expire_date,
                paste_private, paste_format_long, paste_format_short,
                paste_url, paste_hits))

            self.connection.commit()
        except Exception as e:
            self.connection.rollback()

            raise CreateError('An error occurred during paste info creation', e)
        finally:
            return self.cursor.rowcount

    def read(self, paste_key):
        try:
            result = self.cursor.execute(self.READ, (paste_key,)).fetchone()
            
            return dict(result) if result is not None else None
        except Exception as e:
            raise ReadError('An error occurred during paste info read', e)

    def update(self, paste_key, paste_date, paste_title, paste_size,
               paste_expire_date, paste_private, paste_format_long,
               paste_format_short, paste_url, paste_hits):
        try:
            self.cursor.execute(self.UPDATE, (paste_date, paste_title,
                paste_size, paste_expire_date, paste_private,
                paste_format_long, paste_format_short, paste_url, paste_hits,
                paste_key))

            self.connection.commit()
        except Exception as e:
            self.connection.rollback()

            raise UpdateError('An error occurred during paste info update', e)
        finally:
            return self.cursor.rowcount

    def delete(self, paste_key):
        try:
            self.cursor.execute(self.DELETE, (paste_key,))

            self.connection.commit()
        except Exception as e:
            self.connection.rollback()

            raise DeleteError('An error occurred during paste info deletion', e)
        finally:
            return self.cursor.rowcount

    def all(self):
        try:
            result = self.cursor.execute(self.ALL).fetchall()

            return [dict(e) for e in result] if result is not None else None
        except Exception as e:
            raise ReadError('An error occurred while reading all pastes info', e)

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

    def create(self, paste_key, paste):
        try:
            self.cursor.execute(self.CREATE, (paste_key, paste))

            self.connection.commit()
        except Exception as e:
            self.connection.rollback()

            raise CreateError('An error occurred during paste text creation', e)
        finally:
            return self.cursor.rowcount

    def read(self, paste_key):
        try:
            result = self.cursor.execute(self.READ, (paste_key,)).fetchone()

            return dict(result) if result is not None else None
        except Exception as e:
            raise ReadError('An error occurred while reading paste text', e)

    def update(self, paste_key, paste):
        try:
            self.cursor.execute(self.UPDATE, (paste, paste_key))

            self.connection.commit()
        except Exception as e:
            self.connection.rollback()

            raise UpdateError('An error occurred during paste text update', e)
        finally:
            return self.cursor.rowcount

    def delete(self, paste_key):
        try:
            self.cursor.execute(self.DELETE, (paste_key,))

            self.connection.commit()
        except Exception as e:
            self.connection.rollback()

            raise DeleteError('An error occurred during paste text deletion', e)
        finally:
            return self.cursor.rowcount

    def all(self):
        try:
            result = self.cursor.execute(self.ALL).fetchall()

            return [dict(e) for e in result] if result is not None else None
        except Exception as e:
            raise ReadError('An error occurred while reading all paste texts', e)
