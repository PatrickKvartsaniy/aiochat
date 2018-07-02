import datetime

import sqlalchemy as sa
import aiopg.sa

from sqlalchemy.sql import and_, or_

from auth.models import users 

metadata = sa.MetaData()

messages = sa.Table('messages', metadata,
                sa.Column('id',         sa.Integer, primary_key = True),
                sa.Column('date',       sa.VARCHAR(100)),
                sa.Column('author_id',  sa.Integer),
                sa.Column('receiver_id',sa.Integer),
                sa.Column('text',       sa.VARCHAR(100)))

friends = sa.Table('friends', metadata,
                sa.Column('user_id',   sa.Integer),
                sa.Column('friend_id', sa.Integer))

class Message():
    def __init__(self,app,text,author_id,receiver_id=None):
        self.app = app
        self.date = str(datetime.datetime.now())
        self.text = text
        self.author_id = author_id
        self.receiver_id = receiver_id

    async def save_message(self):
        async with self.app.db.acquire() as conn:
            await conn.execute(messages.insert().values(date=self.date,
                                                        author_id = self.author_id,
                                                        receiver_id = self.receiver_id,
                                                        text = self.text))

class Friends():
    def __init__(self,app,user_id, friend_id=None):
        self.app = app
        self.user_id = user_id
        self.friend_id = friend_id

    async def check_friendship(self):
        print(self.user_id, self.friend_id)
        async with self.app.db.acquire() as conn:
            async for row in conn.execute(friends.select().where(and_(
                or_(friends.c.user_id == self.user_id,   friends.c.friend_id == self.user_id),
                or_(friends.c.user_id == self.friend_id, friends.c.friend_id == self.friend_id)))):
                return row
    async def add_friends(self):
        if await self.check_friendship():
            print("You are already friends:)")
        else:
            async with self.app.db.acquire() as conn:
                await conn.execute(friends.insert().values(user_id=self.user_id,
                                                           friend_id = self.friend_id))
                print(f"{user_id} and {friend_id} are friends now!")

    async def find_friends(self):
        friends_id = set()
        async with self.app.db.acquire() as conn:
            async for row in conn.execute(friends.select().where(or_(friends.c.user_id == self.user_id,
                                          friends.c.friend_id == self.user_id))):
                if row.user_id != self.user_id:
                    friends_id.add(row.user_id)
                elif row.friend_id != self.user_id:
                    friends_id.add(row.friend_id)
            return friends_id