"""Unified creation of database and database session.

# NOTE: All models must be imported here so that they get created by the database.
# This is because, all models use the Base model as their base and in order for the
# db_create module to create a table for each model - all models must be available
# in the globals scope of their individual modules.
"""
from . import DeclarativeBase, init_engine, init_session_factory


def delete_db_if_not_exists(engine):
    DeclarativeBase.metadata.drop_all(bind=engine)


def delete_db_and_db_session_from_config_flask(app, config):
    db_uri = config['flask']['SQLALCHEMY_DATABASE_URI']
    engine = init_engine(uri=db_uri)
    app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # silence the deprecation warning

    delete_db_if_not_exists(engine)


def delete_db_and_db_session_from_config_offline(config):
    db_uri = config['flask']['SQLALCHEMY_DATABASE_URI']
    engine = init_engine(uri=db_uri)
    delete_db_if_not_exists(engine)
