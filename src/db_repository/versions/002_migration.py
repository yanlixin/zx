from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
user = Table('user', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('loginname', String(length=64)),
    Column('loginpwd', String(length=64)),
    Column('nickname', String(length=64)),
    Column('email', String(length=120)),
    Column('phone', String(length=20)),
    Column('createdbydate', String(length=20)),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['user'].columns['createdbydate'].create()
    post_meta.tables['user'].columns['email'].create()
    post_meta.tables['user'].columns['loginpwd'].create()
    post_meta.tables['user'].columns['nickname'].create()
    post_meta.tables['user'].columns['phone'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['user'].columns['createdbydate'].drop()
    post_meta.tables['user'].columns['email'].drop()
    post_meta.tables['user'].columns['loginpwd'].drop()
    post_meta.tables['user'].columns['nickname'].drop()
    post_meta.tables['user'].columns['phone'].drop()
