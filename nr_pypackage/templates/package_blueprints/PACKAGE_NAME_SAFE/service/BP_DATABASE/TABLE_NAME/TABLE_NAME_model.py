"""{{ current_table_name_lower }} database model."""
from sqlalchemy import Column, String, Integer, ForeignKey, UnicodeText, UniqueConstraint, Boolean, Float, LargeBinary
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
