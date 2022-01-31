#!/usr/bin/env python3


from faker import Faker
from hashlib import md5
from montydb import set_storage, MontyClient
from os import path, remove
from shutil import rmtree
import aiosqlite, random
from csv import DictReader
from datetime import datetime


DB_FILENAME = 'vfapi'; JWT_SECRET = "penpineappleapplepen"
fake = Faker()
set_storage(
        repository=f'{DB_FILENAME}.nosql.db',
        storage='sqlite',
        use_bson=False
        )
db_client = MontyClient(
        f"{DB_FILENAME}.nosql.db",
        synchronous=1,
        automatic_index=False,
        busy_timeout=5000
        )


def read_csv(filename, delimiter=';'):
    contents = []
    if path.isfile(filename):
        file = open(filename)
        reader = DictReader(file, delimiter=delimiter)
        # columns = reader.fieldnames
        for rows in reader:
            contents.append(rows)
        return tuple(contents)
    else:
        raise FileNotFoundError(f'{filename} doesn\'t exist.')


async def get_sql_db():
    db = await aiosqlite.connect(database=f'{DB_FILENAME}.sql.db')
    return db


def generate_data(max_entries=84):
    users, posts = [], []
    for _ in range(random.randint(7, max_entries)):
        users.append({
            'name': fake.name(),
            'username': fake.user_name(),
            'password': md5(fake.password().encode()).hexdigest(),
            'address': fake.address(),
            'email': fake.email(),
            'tel': fake.phone_number()
            })
    quotes = read_csv('./core/quotes.csv')
    for _ in range(random.randint(7, max_entries)):
        post = random.choice(quotes)
        posts.append({
            'content': f"{post['quote']}  ({post['author']})"
            })
    return (users, posts)


async def populate_sql(db, max_entries=84):
    users, posts = generate_data(max_entries)
    users.append({
        'name': "Captain Nick Lucifer",
        'username': 'nick',
        'password': md5(b'passw0rd').hexdigest(),
        'address': 'Nepal',
        'email': 'naryal2580@gmail.com',
        'tel': '098765456789'
    })
    for user in users:
        query = f'''
INSERT INTO users ( name,
                    username,
                    password,
                    address,
                    email,
                    tel
                    )
        VALUES (
                "{user['name']}",
                "{user['username']}",
                "{user['password']}",
                "{user['address']}",
                "{user['email']}",
                "{user['tel']}"
            ) ;
'''[1:-1]
        await db.execute(query)
        await db.commit()
    for post in posts:
        user = random.choice(users)
        author = await run_sql_query('SELECT id FROM users WHERE username="'+ user['username'] +'"')
        query = f'''
INSERT INTO posts ( content,
                    author,
                    author_id,
                    likes,
                    at
                    )
        VALUES (
                "{post['content']}",
                "{user['name']}",
                "{author['id']}",
                0,
                "{datetime.now()}"
            ) ;
'''[1:-1]
        await db.execute(query)
        await db.commit()


async def init_sql_db_users(db):
    await db.execute('''
CREATE TABLE users ( id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    username TEXT NOT NULL,
                    password TEXT NOT NULL,
                    address TEXT NOT NULL,
                    email TEXT NOT NULL,
                    tel TEXT NOT NULL
                    );'''[1:])
    await db.commit()


async def init_sql_db_posts(db):
    await db.execute('''
CREATE TABLE posts ( id INTEGER PRIMARY KEY AUTOINCREMENT,
                    content TEXT NOT NULL,
                    author TEXT NOT NULL,
                    author_id INTEGER FOREIGNKEY,
                    likes INTEGER NOT NULL,
                    at TEXT NOT NULL
                    );'''[1:])
    await db.commit()


async def init_sql_db():
    if path.isfile(f'{DB_FILENAME}.sql.db'):
        remove(f'{DB_FILENAME}.sql.db')
    db = await get_sql_db()
    await init_sql_db_users(db)
    await init_sql_db_posts(db)
    await populate_sql(db)
    await db.close()
    return True


async def init_nosql_db():
    if path.isdir(f'{DB_FILENAME}.nosql.db'):
        rmtree(f'{DB_FILENAME}.nosql.db')
    users = db_client.vfapi.users
    users_data = await run_sql_query('SELECT * FROM USERS;')
    for user in users_data:
        users.insert_one({
            'id': user['id'],
            'name': user['name'],
            'username': user['username'],
            'address': user['address'],
            'email': user['email'],
            'tel': user['tel']
            })
    posts = db_client.vfapi.posts
    posts_data = await run_sql_query('SELECT * FROM POSTS;')
    for post in posts_data:
        posts.insert_one({
            'id': post['id'],
            'content': post['content'],
            'author': post['author'],
            'author_id': post['author_id']
            })


async def init_db():
    await init_sql_db()
    await init_nosql_db()


async def run_sql_query(query, commit=False):
    try:
        db = await get_sql_db()
        cursor = await db.execute(query)
        _data, keys, data = await cursor.fetchall(), [], {}
        if commit: await db.commit()
        await cursor.close()
        await db.close()
        if commit: return _data
        for k in cursor.description:
            keys.append(k[0])
        if len(_data) == 1:
            if len(_data[0]) == 1:
                return {keys[0]: _data[0][0]}
            _data = _data[0]
            for i in range(len(keys)):
                data[keys[i]] = _data[i]
        else:
            data = []
            for d in _data:
                _d = {}
                for i in range(len(keys)):
                    _d[keys[i]] = d[i]
                data.append(_d)
        return data
    except KeyboardInterrupt as e:
    # except Exception as e:
        print(e)
        await init_db()
        return await run_sql_query(query)


def get_nosql_users(query):
    users = db_client.vfapi.users
    user_data = tuple(users.find(query))
    for data in user_data: data.pop('_id'); # data.pop('password')
    if len(user_data) == 1: return user_data[0]
    return tuple(user_data)
