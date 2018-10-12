"""Module dedicated to high level database api for the table which takes care of session management."""
from . import {{ current_table_name_lower }}_ops
from .. import ManagedSession


def get_{{ current_table_name_lower }}s(**kwargs):
    """Get multiple {{ current_table_name_lower }}s."""
    with ManagedSession() as session:
        {{ current_table_name_lower }}s = {{ current_table_name_lower }}_ops.select_all(session=session, **kwargs)
        return {{ current_table_name_lower }}s


def get_{{ current_table_name_lower }}(**kwargs):
    """Get a single object."""
    with ManagedSession() as session:
        {{ current_table_name_lower }} = {{ current_table_name_lower }}_ops.select_one(session=session, **kwargs)
        return {{ current_table_name_lower }}


def register_{{ current_table_name_lower }}({{ blueprints['database']['current_table'].column_names_as_args }}):
    """Register object."""
    with ManagedSession() as session:
        {{ current_table_name_lower }} = {{ current_table_name_lower }}_ops.insert(
            session=session,
            {% for column_name in blueprints['database']['current_table'].column_names %}
            {{ column_name }}={{ column_name }},
            {% endfor %}
        )
        return {{ current_table_name_lower }}


def update_{{ current_table_name_lower }}({{ blueprints['database']['current_table'].column_names_as_args }}):
    with ManagedSession() as session:
        {{ current_table_name_lower }} = {{ current_table_name_lower }}_ops.update(
            session=session,
            {% for column_name in blueprints['database']['current_table'].column_names %}
            {{ column_name }}={{ column_name }},
            {% endfor %}
        )
        return {{ current_table_name_lower }}


def deregister_{{ current_table_name_lower }}({{ blueprints['database']['current_table'].column_names_as_args }}):
    with ManagedSession() as session:
        {{ current_table_name_lower }} = {{ current_table_name_lower }}_ops.delete(
            session=session,
            {% for column_name in blueprints['database']['current_table'].column_names %}
            {{ column_name }}={{ column_name }},
            {% endfor %}
        )
        return {{ current_table_name_lower }}
