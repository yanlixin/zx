from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
School = Table('School', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('schoolname', String(length=120)),
    Column('schooldesc', String(length=1024)),
    Column('addr', String(length=126)),
    Column('tuition', String(length=64)),
    Column('features', String(length=1024)),
    Column('phone', String(length=32)),
    Column('intro', String(length=1024)),
    Column('team', String(length=1024)),
    Column('founded', String(length=16)),
    Column('city', String(length=64)),
    Column('age', String(length=64)),
    Column('size', String(length=64)),
    Column('population', String(length=32)),
    Column('duration', String(length=32)),
    Column('foreignduration', String(length=1024)),
    Column('schoolbus', String(length=16)),
    Column('cramclass', String(length=16)),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['School'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['School'].drop()
