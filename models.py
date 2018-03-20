import sqlalchemy as sa
import aiopg.sa

meta = sa.MetaData()

question = sa.Table(
    'questions', meta,
    sa.Column('id', sa.Integer, nullable=False),
    sa.Column('question_text', sa.String(200), nullable=False),
    sa.Column('pub_date', sa.Date, nullable=False),

    #Indexes
    sa.PrimaryKeyConstraint('id', name='question_id_pkey')
)

choise = sa.Table(
    'choise', meta,
    sa.Column('id', sa.Integer, nullable=False),
    sa.Column('question_id', sa.Integer, nullable=False),
    sa.Column('choise_text', sa.String(200), nullable=False),
    sa.Column('votes', sa.Integer, server_default="0", nullable=False),
    
    #Indexes
    sa.PrimaryKeyConstraint('id',name='choise_id_pkey'),
    sa.ForeignKeyConstraint(['question_id'], [question.c.id],
                            name='choise_question_id_fkey',
                            ondelete='CASCADE')
)

async def init_pg(app):
    conf = app['config']['postgres']
    engine = await aiopg.sa.create_engine(
        database=conf['database'],
        user=conf['user'],
        password=cond['password'],
        host=conf['host'],
        port=conf['port'],
        minsize=conf['minsize'],
        maxsize=conf['maxsize'],
        loop=app.loop)
    app['db'] = engine

async def close_pg(app):
    app['db'].close()
    await app['db'].wait_closed()