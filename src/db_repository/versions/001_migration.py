from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
user = Table('user', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('loginname', VARCHAR(length=64)),
    Column('loginpwd', VARCHAR(length=64)),
    Column('nickname', VARCHAR(length=64)),
    Column('email', VARCHAR(length=120)),
    Column('phone', VARCHAR(length=20)),
    Column('createdbydate', VARCHAR(length=20)),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['user'].columns['createdbydate'].drop()
    pre_meta.tables['user'].columns['email'].drop()
    pre_meta.tables['user'].columns['loginpwd'].drop()
    pre_meta.tables['user'].columns['nickname'].drop()
    pre_meta.tables['user'].columns['phone'].drop()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['user'].columns['createdbydate'].create()
    pre_meta.tables['user'].columns['email'].create()
    pre_meta.tables['user'].columns['loginpwd'].create()
    pre_meta.tables['user'].columns['nickname'].create()
    pre_meta.tables['user'].columns['phone'].create()
