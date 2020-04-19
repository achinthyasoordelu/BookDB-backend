from sqlalchemy import Table, Column, Integer, String, MetaData

meta = MetaData()

quotesTable = Table(
    'quotes', meta,
    Column('QuoteID', Integer, primary_key=True),
    Column('Title', String),
    Column('Author', String),
    Column('Quote', String)
)

quotesTagsTable = Table(
    'quotetags', meta,
    Column('QuoteID', Integer, primary_key=True),
    Column('Tag', String, primary_key=True),
)

tagsTable = Table(
    'tags', meta,
    Column('Tag', String, primary_key=True),
)