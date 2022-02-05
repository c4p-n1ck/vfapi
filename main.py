#!/usr/bin/env python3


'''
Vulnerable FastAPI (vFastAPI)

Please issue a GET request to "/docs" in order to obtain information regarding endpoints within this API.
'''


from typing import Optional, Any

from fastapi import (
    FastAPI,
    Body,
    HTTPException,
    Header,
    Depends
); from core import (
    db_client,
    get_sql_db,
    init_db,
    run_sql_query,
    get_nosql_users,
    rmtree,
    remove,
    md5,
    jwt,
    time,
    CORSMiddleware,
    StaticFiles,
    get_openapi,
    BaseModel,
    FileResponse,
    RedirectResponse,
    HTMLResponse,
    JWT_SECRET,
    DB_FILENAME,
    datetime
); import asyncio


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

class Post(BaseModel):
    content: str

author_info = {
    'name': 'Captain Nick Lucifer*',
    'url': 'https://git.io/vulnfapi',
    'email': 'naryal2580@gmail.com'
        }
__license__ = {
        'name': 'MIT',
        'url': 'https://github.com/naryal2580/vfapi/blob/main/LICENSE'
        }
app = FastAPI(
        title="vFastAPI",
        version="0.01a",
        description=__doc__,
        contact=author_info,
        license_info=__license__,
        redoc_url=False,
        docs_url=False
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


async def validation(token: Optional[str] = Header(None)):
    data = jwt.decode(token, JWT_SECRET, algorithms=['HS256'])
    if ( int(time()) - data['iat'] ) < 720 and data:
        return data
    raise HTTPException(status_code=401, detail="idk some auth err.")


@app.get('/', include_in_schema=False)
def root():
    return RedirectResponse('/docs')


@app.get('/select')
async def sql_return_users_from_username(username: str, token: dict = Depends(validation)):
    """# Select\n
            Selects and returns users using a SQL query.\n
            _Parameters_: \n
                - username: str\n
                - token: jwt
    """
    resp = await run_sql_query(f'SELECT * FROM users WHERE username = "{username}";')
    return resp


@app.put('/post')
async def add_post(post: Post, token: dict = Depends(validation)):
    """# Add Post\n
        Adds post content to the API database.\n
        _Parameters_: \n
            - Post (content): str\n
            - token: jwt
    """
    username = token['username']
    author = await run_sql_query(f'SELECT * FROM users WHERE username="{username}"')
    query = f'''
INSERT INTO posts ( content,
                    author,
                    author_id,
                    likes,
                    at
                    )
        VALUES (
                "{post.content}",
                "{author['name']}",
                "{author['id']}",
                0,
                "{datetime.now()}"
            ) ;
'''[1:-1]
    await run_sql_query(query, commit=True)
    return {'resp': 'done'}


@app.get('/posts')
async def get_posts(token: dict = Depends(validation)):
    """# Get Posts\n
        Gets posts off the API.\n
        _Parameters_: \n
            - token: jwt
    """
    posts = await run_sql_query('SELECT * FROM posts;')
    return {'posts': posts}


@app.put('/user')
async def add_user(user: User):
    """# Add User\n
        Adds a user to the API database.\n
        _Parameters_: \n
            - user (
                name: str,
                username: str,
                address: str,
                email: str,
                password: str,
                tel: str
            )
    """
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
    """# Find\n
        Finds user via username on the API using NoSql.\n
        _Parameters_: \n
            - username: str\n
            - token: jwt
    """
    return get_nosql_users({'username': username})


@app.post('/find')
async def nosql_return_users(query: dict = Body(...), token: dict = Depends(validation)):
    """# Return Users\n
        Returns user(s) via a JSON query on the API using NoSql!\n
        _Parameters_: \n
            - query: json\n
            - token: jwt
    """
    return get_nosql_users(query)


@app.post('/login')
async def authenticate(creds: Credentials):
    """# Login\n
        Returns a token after authenticating a user via their credentials.\n
        _Parameters_: \n
            - Credentials\n
                - username: str\n
                - password: str
    """
    resp = await run_sql_query(f'SELECT username, password FROM users WHERE username = "{creds.username}";')
    if not resp:
        raise HTTPException(status_code=401, detail="Invalid credentials sent. Access Denied!")
    if type(resp) == list:
        resp = resp[0]
    if resp and md5(creds.password.encode()).hexdigest() == resp['password']:
        return {'token': jwt.encode({'username': creds.username, 'iat': int(time())}, JWT_SECRET, algorithm='HS256')}
    raise HTTPException(status_code=401, detail="Invalid credentials sent. Access Denied!")


@app.delete('/user')
async def remove_user(username: Optional[str] = '', user: Optional[User] = None, token: dict = Depends(validation)):
    """# Remove User\n
        Remove a user from the API database based on either username, **OR** user object.\n
        _Parameters_: \n
            + username: str\n
            + user (\n
                name: str,\n
                username: str,\n
                address: str,\n
                email: str,\n
                password: str,\n
                tel: str\n
            )\n
            - token: jwt
    """
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
async def return_favicon():
    return FileResponse('./static/img/favicon.ico')


@app.get('/robots.txt', include_in_schema=False)
async def return_robots_txt():
    return FileResponse('./static/robots.txt')


@app.get('/.well-known/security.txt', include_in_schema=False)
async def security_txt():
    return FileResponse('./static/security.txt')


@app.get('/docs', include_in_schema=False)
async def return_docs():
    return HTMLResponse('<!DOCTYPE html><html><head><link type="text/css" rel="stylesheet" href="static/css/swagger-ui.css"><link rel="shortcut icon" href="static/img/favicon.png"><title>' + app.title + ' - Swagger UI</title></head><body><div id="vfastapi-ui"></div><script src="static/js/swagger-ui-bundle.js"></script><script>const ui = SwaggerUIBundle({ url: "/openapi.json", oauth2RedirectUrl: window.location.origin + "/docs/oauth2-redirect", dom_id: "#vfastapi-ui", presets: [ SwaggerUIBundle.presets.apis, SwaggerUIBundle.SwaggerUIStandalonePreset ], layout: "BaseLayout", deepLinking: true, showExtensions: true, showCommonExtensions: true });</script></body></html>', status_code=200)


@app.get('/redoc', include_in_schema=False)
async def return_redoc():
    return HTMLResponse('<!DOCTYPE html><html><head><title>' + app.title + ' - ReDoc</title><meta charset="utf-8"/><meta name="viewport" content="width=device-width, initial-scale=1"><link href="static/css/Montserrat.css" rel="stylesheet"><link rel="shortcut icon" href="static/img/favicon.png"><link rel="stylesheet" href="static/css/redoc-ui.css" type="text/css"></head><body><redoc spec-url="/openapi.json"></redoc><script src="static/js/redoc.standalone.js"> </script></body></html>', status_code=200)


app.openapi = openapi


if __name__ == '__main__':
    args, port = __import__('sys').argv, 8888
    for arg in args:
        try:
            if int(arg) > 1024 and int(arg) < 65535:
                port = int(arg)
                print(f'[info] Using {port} as port number.')
        except: pass
    if '--dev' in args:
        asyncio.run(init_db()); __import__('uvicorn').run('main:app', port=port, reload=True)
    else:
        asyncio.run(init_db()); __import__('uvicorn').run('main:app', port=port, reload=False)
