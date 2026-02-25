import sqlite3

class Database:
    def __init__(self, db_name):

        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()

    async def get_products_by_category(self, category):
        self.cursor.execute(
            "SELECT name, price, image_path FROM products WHERE category = ?",
            (category,)
        )
        return self.cursor.fetchall()

    def close(self):
        self.conn.close()