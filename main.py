#!/usr/bin/env python3


'''
Vulnerable FastAPI (vFastAPI)

Please issue a GET request to "/docs" in order to obtain infromation regarding endpoints within this API.
'''


from typing import Optional, Any

from faker import Faker
from hashlib import md5
from montydb import set_storage, MontyClient
from fastapi import FastAPI, Request, Body, HTTPException, Header, Depends
from pydantic import BaseModel
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.openapi.utils import get_openapi
from fastapi.openapi.docs import get_swagger_ui_oauth2_redirect_html
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from jose import jwt
from time import time
from os import path, remove
from shutil import rmtree
import asyncio, aiosqlite, random


class User(BaseModel):
    name: str
    username: str
    address: str
    email: str
    password: str
    tel: str

class Credentials(BaseModel):
    username: str
    password: str

author_info = {
    'name': 'Captain Nick Lucifer*',
    'url': 'https://git.io/vulnfapi',
    'email': 'naryal2580@gmail.com'
        }
__license__ = {
        'name': 'MIT',
        'url': 'https://github.com/naryal2580/vfapi/blob/main/LICENSE'
        }
DB_FILENAME = 'vfapi'; JWT_SECRET = "penpineappleapplepen"
app = FastAPI(
        title="vFastAPI",
        version="0.01a",
        description=__doc__,
        contact=author_info,
        license_info=__license__,
        redoc_url=False,
        docs_url=False
        )
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
app.mount("/static", StaticFiles(directory="static"), name="static")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="vFastAPI",
        version="0.01a",
        description=__doc__,
        contact=author_info,
        license_info=__license__,
        routes=app.routes
    )
    openapi_schema["info"]["x-logo"] = {
        "url": "static/img/logo.png"
    }
    # print(openapi_schema)
    app.openapi_schema = openapi_schema
    return app.openapi_schema


async def get_sql_db():
    db = await aiosqlite.connect(database=f'{DB_FILENAME}.sql.db')
    return db


async def init_sql_db():
    if path.isfile(f'{DB_FILENAME}.sql.db'):
        remove(f'{DB_FILENAME}.sql.db')
    db = await get_sql_db()
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
    for _ in range(random.randint(7, 84)):
        query = f'''
INSERT INTO users ( name,
                    username,
                    password,
                    address,
                    email,
                    tel
                    )
       VALUES (
                "{fake.name()}",
                "{fake.user_name()}",
                "{md5(fake.password().encode()).hexdigest()}",
                "{fake.address()}",
                "{fake.email()}",
                "{fake.phone_number()}"
            ) ;
'''[1:-1]
        await db.execute(query)
        await db.commit()
    await db.close()
    return True


async def init_nosql_db():
    if path.isdir(f'{DB_FILENAME}.nosql.db'):
        rmtree(f'{DB_FILENAME}.nosql.db')
    users = db_client.vfapi.users
    data = await run_sql_query('SELECT * FROM USERS;')
    for user in data:
        users.insert_one({
            'id': user['id'],
            'name': user['name'],
            'username': user['username'],
            'address': user['address'],
            'email': user['email'],
            'tel': user['tel']
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


async def validation(token: Optional[str] = Header(None)):
    data = jwt.decode(token, JWT_SECRET, algorithms=['HS256'])
    if ( int(time()) - data['iat'] ) < 720:
        return data


@app.get('/', include_in_schema=False)
def root():
    return {'goto': '/docs'}


@app.get('/select')
async def sql_return_users_from_username(username: str, token: dict = Depends(validation)):
    resp = await run_sql_query(f'SELECT * FROM users WHERE username = "{username}";')
    return resp


@app.put('/user')
async def put_user(user: User):
    user.password = md5(user.password.encode()).hexdigest()
    query = f'''
INSERT INTO users (
                    name,
                    username,
                    password,
                    address,
                    email,
                    tel
                ) VALUES ( 
                            "{user.name}",
                            "{user.username}",
                            "{user.password}",
                            "{user.address}",
                            "{user.email}",
                            "{user.tel}"
                            );
'''[1:-1]
    await run_sql_query(query, commit=True)
    _id = await run_sql_query('SELECT id from users ORDER BY ROWID DESC limit 1;')
    db_client.vfapi.users.insert_one({
        'id': _id,
        'name': user.name,
        'username': user.username,
        'password': user.password,
        'address': user.address,
        'email': user.email,
        'tel': user.tel
        })
    return {'resp': 'done'}


@app.get('/find')
async def nosql_return_users_from_username(username: str, token: dict = Depends(validation)):
    return get_nosql_users({'username': username})


@app.post('/find')
async def nosql_return_users(query: dict = Body(...), token: dict = Depends(validation)):
    print(query)
    return get_nosql_users(query)


@app.post('/login')
async def authenticate(creds: Credentials):
    resp = await run_sql_query(f'SELECT username, password FROM users WHERE username = "{creds.username}";')
    if not resp:
        raise HTTPException(status_code=401, detail="Invalid credentials sent. Access Denied!")
    if type(resp) == list:
        resp = resp[0]
    if resp and md5(creds.password.encode()).hexdigest() == resp['password']:
        return {'token': jwt.encode({'username': creds.username, 'iat': int(time())}, JWT_SECRET, algorithm='HS256')}
    raise HTTPException(status_code=401, detail="Invalid credentials sent. Access Denied!")


@app.delete('/user')
async def delete_user(username: Optional[str] = '', user: Optional[User] = None, token: dict = Depends(validation)):
    if username:
        db_client.vfapi.users.delete_one({'username': username})
        await run_sql_query(f'DELETE FROM users WHERE username = "{username}";', commit=True)
        return {'resp': 'done'}
    elif user:
        db_client.vfapi.users.delete_one({'address': user.address})
        await run_sql_query(f'DELETE FROM users WHERE address = {user.address};', commit=True)
    return {'resp': '!done'}


@app.get('/reset', include_in_schema=False)
def reset_page():
    return {'resp': 'Please issue a POST request to the same endpoint in order to actually reset the database.'}


@app.post('/reset')
async def reset_database():
    remove(f'{DB_FILENAME}.sql.db')
    rmtree(f'{DB_FILENAME}.nosql.db')
    await init_db()
    return {'resp': 'done'}


@app.get('/favicon.ico', include_in_schema=False)
def return_favicon():
    return FileResponse('./static/img/favicon.ico')


@app.get('/robots.txt', include_in_schema=False)
def return_robots_txt():
    return FileResponse('./static/robots.txt')


@app.get('/.well-known/security.txt', include_in_schema=False)
def security_txt():
    return FileResponse('./static/security.txt')


@app.get('/docs', include_in_schema=False)
def return_docs():
    return HTMLResponse('<!DOCTYPE html><html><head><link type="text/css" rel="stylesheet" href="static/css/swagger-ui.css"><link rel="shortcut icon" href="static/img/favicon.png"><title>' + app.title + ' - Swagger UI</title></head><body><div id="vfastapi-ui"></div><script src="static/js/swagger-ui-bundle.js"></script><script>const ui = SwaggerUIBundle({ url: "/openapi.json", oauth2RedirectUrl: window.location.origin + "/docs/oauth2-redirect", dom_id: "#vfastapi-ui", presets: [ SwaggerUIBundle.presets.apis, SwaggerUIBundle.SwaggerUIStandalonePreset ], layout: "BaseLayout", deepLinking: true, showExtensions: true, showCommonExtensions: true });</script></body></html>', status_code=200)


@app.get('/redoc', include_in_schema=False)
def return_redoc():
    # TODO: Serve font locally.
    return HTMLResponse('<!DOCTYPE html><html><head><title>' + app.title + ' - ReDoc</title><meta charset="utf-8"/><meta name="viewport" content="width=device-width, initial-scale=1"><link href="https://fonts.googleapis.com/css?family=Montserrat:300,400,700|Roboto:300,400,700" rel="stylesheet"><link rel="shortcut icon" href="static/img/favicon.png"><link rel="stylesheet" href="static/css/redoc-ui.css" type="text/css"></head><body><redoc spec-url="/openapi.json"></redoc><script src="static/js/redoc.standalone.js"> </script></body></html>', status_code=200)


app.openapi = openapi


if __name__ == '__main__':
    # TODO: Custom port number.
    args = __import__('sys').argv
    if '--dev' in args:
        asyncio.run(init_db()); __import__('uvicorn').run('main:app', port=8888, reload=True)
    else:
        asyncio.run(init_db()); __import__('uvicorn').run('main:app', port=8888, reload=False)
