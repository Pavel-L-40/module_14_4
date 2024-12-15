import sqlite3


def initiate_db():
    connection = sqlite3.connect('db_crud.db')
    cursor = connection.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Products(
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT,
    price INT NOT NULL,
    photo TEXT
    );
    ''')
    connection.commit()
    connection.close()

dict_product = {1: ['izotonic', 'про изотоники', 1000, 'files/izotonic.jpg'], 2: ['vitamin', 'про витамины', 750, 'files/vitamin.jpg'],
                3: ['protein', 'про протеин', 500, 'files/protein.jpg'], 4: ['hormon', 'про гормон', 6400, 'files/hormone.jpeg']}

def add_dict_product():
    connection = sqlite3.connect('db_crud.db')
    cursor = connection.cursor()
    for i in range(1,1+len(dict_product)):
        connection.execute('INSERT INTO Products(title, description, price, photo) VALUES (?,?,?,?)',
                       (dict_product[i][0], dict_product[i][1], dict_product[i][2], dict_product[i][3]))
    connection.commit()
    connection.close()

def get_all_products():
    connection = sqlite3.connect('db_crud.db')
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM Products')
    all_products = cursor.fetchall()
    connection.close()
    return all_products

# initiate_db()
# add_dict_product()

