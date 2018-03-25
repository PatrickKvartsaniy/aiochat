import sqlalchemy as sa
import aiopg.sa

metadata = sa.MetaData()

async def init_pg(app):
    conf = app['config']['postgres']
    engine = await aiopg.sa.create_engine(
        database=conf['database'],
        user=conf['user'],
        password=conf['password'],
        host=conf['host'],
        port=conf['port'],
        minsize=conf['minsize'],
        maxsize=conf['maxsize'],
        loop=app.loop)
    return engine


users = sa.Table('users',metadata,
                 sa.Column('id',sa.Integer, primary_key = True),
                 sa.Column('nickname', sa.VARCHAR(100)),
                 sa.Column('email',    sa.VARCHAR(100)),
                 sa.Column('password', sa.VARCHAR(100)))

async def close_pg(app):
    app['db'].close()
    await app['db'].wait_closed()

class User():
    def __init__(self,app,nickname,email="",password=""):
        self.app      = app
        self.nickname = nickname
        self.email    = email
        self.password = password

    async def create_user(self):
        async with self.app.db.acquire() as conn:
            return await conn.execute(users.insert().values(nickname = self.nickname,
                                                            email    = self.email,
                                                            password = self.password))

    async def check_user(self):
        async with self.app.db.acquire() as conn:
            async for row in conn.execute(users.select().where(users.c.nickname == self.nickname)):
                return row.id