import sqlite3


class DataBase:
    def __init__(self):
        self.conn = sqlite3.connect("books.db")
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS books (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT,
                author TEXT,
                year INTEGER
            )
            """
        )
        self.conn.commit()

    def add_book(self, title, author, year):
        self.cursor.execute(
            """
            INSERT INTO books (title, author, year)
            VALUES (?, ?, ?)
            """,
            (title, author, year),
        )
        self.conn.commit()

    def get_books(self):
        self.cursor.execute("SELECT * FROM books")
        return self.cursor.fetchall()

    def search_books(self, title):
        self.cursor.execute(
            """
            SELECT * FROM books WHERE title LIKE ?
            """,
            ("%" + title + "%",),
        )
        return self.cursor.fetchall()

    def update_book(self, book_id, title, author, year):
        self.cursor.execute(
            """
            UPDATE books SET title = ?, author = ?, year = ?
            WHERE id = ?
            """,
            (title, author, year, book_id),
        )
        self.conn.commit()

    def delete_book(self, book_id):
        self.cursor.execute(
            """
            DELETE FROM books WHERE id = ?
            """,
            (book_id,),
        )
        self.conn.commit()
