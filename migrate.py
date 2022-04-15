import psycopg2

print('connecting...')
conn = psycopg2.connect(
        host="localhost",
        database="gamery",
        user='postgres',
        password='123456')

cur = conn.cursor()

cur.execute('CREATE TABLE games (id serial PRIMARY KEY,'
                                 'name varchar (50) NOT NULL,'
                                 'category varchar (40) NOT NULL,'
                                 'console varchar (20) NOT NULL,'
                                 'created_at date DEFAULT CURRENT_TIMESTAMP);'
            'CREATE TABLE users (id serial PRIMARY KEY,'
                                 'username varchar (20) NOT NULL,'
                                 'name varchar (50) NOT NULL,'
                                 'password varchar (20) NOT NULL,'
                                 'created_at date DEFAULT CURRENT_TIMESTAMP);'
                                 )

cur.execute('INSERT INTO users (username, name, password)'
            'VALUES (%s, %s, %s)',
            ('richard',
             'Richard Dickens',
             '12345678')
            )

cur.executemany(
      'INSERT INTO games (name, category, console) VALUES (%s, %s, %s)',
      [
            ('God of War 4', 'Ação', 'PS4'),
            ('NBA 2k18', 'Esporte', 'Xbox One'),
            ('Rayman Legends', 'Indie', 'PS4'),
            ('Super Mario RPG', 'RPG', 'SNES'),
            ('Super Mario Kart', 'Corrida', 'SNES'),
            ('Fire Emblem Echoes', 'Estratégia', '3DS'),
      ])


conn.commit()
cur.close()
conn.close()