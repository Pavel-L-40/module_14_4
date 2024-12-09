import sqlite3


connection = sqlite3.connect('Products.db') # <<< определяем файл с которым мы будем работать
cursor = connection.cursor()  # << Задаем курсор для работы с данными


# создаем таблицу и определяем ее столбцы >>>
def initiate_db():
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Products(
    id INTEGER PRIMARY KEY, 
    title TEXT NOT NULL,
    description TEXT,
    price INT NOT NULL,
    img TEXT
    );
    ''')

    cursor.execute('CREATE INDEX IF NOT EXISTS idx_title on Products (title, description)')


dict_product = {1: ['product first', 'about first', 100, 'jp1.jpg'], 2: ['product second', 'about second', 750, 'jp2.jpg'],
                3: ['product third', 'about th', 500, 'jp3.jpg'], 4: ['boyar', 'ot vsego', 64, 'jp4.jpg']}

def filling_table():
    initiate_db()
    for i in range(1, 5):
        cursor.execute('INSERT INTO Products (title, description, price, img) VALUES(?,?,?,?)',
                       (dict_product[i][0], dict_product[i][1], dict_product[i][2], dict_product[i][3]))
    connection.commit()
    connection.close()

def get_all_products():
    connection = sqlite3.connect('Products.db')
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM Products')
    products = cursor.fetchall()
    if products is not None:
        for product in products:
            print(product)
    connection.close()

# filling_table()  # <<<<< создание таблицы и добавление в таблицу товаров
get_all_products() # >> вывод в консоль значений таблицы





