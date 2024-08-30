import psycopg2


class PostgreSql_monitor:
    def __init__(self):
        self.connect = psycopg2.connect(
            host="localhost",
            user="postgres",
            database="online_store",
            password="123456"
        )
        self.cursor = self.connect.cursor()
    def create_table(self):
        self.cursor.execute(f"""
            CREATE TABLE IF NOT EXISTS monitors(
                id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
                brand_name VARCHAR(255),
                product_url TEXT,
                product_image VARCHAR(255),
                product_price VARCHAR(40),
                configurations TEXT UNIQUE
            )""")
        self.connect.commit()
    def insert_data(self, *args):
        self.create_table()
        self.cursor.execute(f"""INSERT INTO monitors (brand_name, product_url, product_image, product_price, configurations)
            VALUES (%s, %s, %s, %s, %s)
            ON CONFLICT(configurations) DO NOTHING""", args)
        self.connect.commit()
    def select_data(self):
        self.cursor.execute(f"""
            SELECT brand_name, product_url, product_image, product_price, configurations
            FROM monitors
        """)
        return self.cursor.fetchall()