"""Simple database ops."""
import logging
from .{{ current_table_name_lower }}_model import {{ current_table_name }}


logger = logging.getLogger(__name__)


def select_all(session, **kwargs):
    if kwargs:
        return (session.query({{ current_table_name }})
                .filter_by(**kwargs)
                .all())
    else:
        return (session.query({{ current_table_name }})
                .all())


def select_one(session, **kwargs):
    if kwargs:
        return (session.query({{ current_table_name }})
                .filter_by(**kwargs)
                .one())
    else:
        return (session.query({{ current_table_name }})
                .one())


def insert(session, **kwargs):
    """Insert {{ current_table_name_lower }}."""
    kwargs['id'] = None
    {{ current_table_name_lower }} = {{ current_table_name }}(**kwargs)
    session.add({{ current_table_name_lower }})
    return {{ current_table_name_lower }}


def update(session, id, **kwargs):
    """Update {{ current_table_name_lower }}."""
    {{ current_table_name_lower }} = select_one(session, id=id)
    for k, v in kwargs.items():
        setattr({{ current_table_name_lower }}, k, v)
    session.add({{ current_table_name_lower }})
    return {{ current_table_name_lower }}


def delete(session, id, **kwargs):
    """Delete {{ current_table_name_lower }}."""
    {{ current_table_name_lower }} = select_one(session, id=id)
    session.delete({{ current_table_name_lower }})
    return {{ current_table_name_lower }}
