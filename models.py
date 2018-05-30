import sqlalchemy as sa
import aiopg.sa
import datetime

metadata = sa.MetaData()

users = sa.Table('users',metadata,
                 sa.Column('id',       sa.Integer, primary_key = True),
                 sa.Column('nickname', sa.VARCHAR(100)),
                 sa.Column('email',    sa.VARCHAR(100)),
                 sa.Column('password', sa.VARCHAR(100)))

messages = sa.Table('messages', metadata,
                sa.Column('id',         sa.Integer, primary_key = True),
                sa.Column('date',       sa.VARCHAR(100)),
                sa.Column('author_id',  sa.Integer),
                sa.Column('receiver_id',sa.Integer),
                sa.Column('text',       sa.VARCHAR(100)))

class User():
    def __init__(self,app,id="",nickname="",email="",password=""):
        self.id = id
        self.app = app
        self.nickname = nickname
        self.email = email
        self.password = password

    async def create_user(self):
        user = await self.check_user()
        if not user:
            async with self.app.db.acquire() as conn:
                result = await conn.execute(users.insert().values(nickname = self.nickname,
                                                                  email = self.email,
                                                                  password = self.password))
        else:
            result = "User exist"
        return result
            

    async def check_user(self):
        async with self.app.db.acquire() as conn:
            async for row in conn.execute(users.select().where(users.c.nickname == self.nickname)):
                return row.id

    async def get_login(self):
        async with self.app.db.acquire() as conn:
            async for row in conn.execute(users.select().where(users.c.id == self.id)):
                return row.nickname

class Message():
    def __init__(self,app,text,author_id,receiver_id=None):
        self.app = app
        self.date = str(datetime.datetime.now())
        self.text = text
        self.author_id = author_id
        self.receiver_id = receiver_id

    async def save_message(self):
        async with self.app.db.acquire() as conn:
            result = await conn.execute(messages.insert().values(date=self.date,
                                                                 author_id = self.author_id,
                                                                 receiver_id = self.receiver_id,
                                                                 text = self.text))