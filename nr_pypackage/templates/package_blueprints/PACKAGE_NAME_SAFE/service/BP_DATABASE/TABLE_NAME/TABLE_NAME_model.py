"""{{ current_table_name_lower }} database model."""
from sqlalchemy.dialects.postgresql.json import JSON as Postgres_JSON
from sqlalchemy.dialects.postgresql.json import JSONB as Postgres_JSONB
from sqlalchemy import Text as StringText
from sqlalchemy import (Column, String, Unicode, Integer, ForeignKey,
                        UnicodeText, UniqueConstraint, Boolean, Float, LargeBinary,
                        DateTime, TIMESTAMP)

from sqlalchemy.orm import relationship

from .. import Base


class {{ blueprints['database']['current_table'].table_name }}(Base):
    __tablename__ = '{{ current_table_name_lower }}'

    # Columns
    {% for column_statement in blueprints['database']['current_table'].column_statements %}
    {{ column_statement }}
    {% endfor %}

    # Foreign keys.
    {% for foreign_statement in blueprints['database']['current_table'].foreign_statements %}
    {{ foreign_statement }}
    {% endfor %}

    # Foreign relationships.
    {% for foreign_relationship in blueprints['database']['current_table'].foreign_relationships %}
    {{ foreign_relationship }}
    {% endfor %}

    # Unique contraints.
    __table_args__ = (
        {% for unique_constraint in blueprints['database']['current_table'].unique_constraints %}
        UniqueConstraint({{ unique_constraint }}),
        {% endfor %}
    )

    def to_dict(self):
        """Represent table row as dict."""
        row_dict = self.__dict__
        row_dict.pop('_sa_instance_state')
        {% for foreign_table in blueprints['database']['current_table'].foreign_parents %}
        row_dict.pop('{{ foreign_table.lower() }}')
        {% endfor %}
        {% for foreign_table in blueprints['database']['current_table'].foreign_children %}
        row_dict.pop('{{ foreign_table.lower() }}s', None)
        {% endfor %}
        return row_dict
