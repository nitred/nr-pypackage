import click


auth_instructions_doc = """--------------------------------------------------------------------------------
        SPECIAL INSTRUCTIONS FOR BLUEPRINT: "auth"
--------------------------------------------------------------------------------
1. Edit the docker/docker-compose.yml to have a custom network subnet.
2. Edit blueprints.auth.models to include an `is_ldap_authenticated_user` function.
"""


def handle_auth(include, **kwargs):
    """Main CLI entrypoint for Python Package option."""
    return {'include': include, 'instructions': auth_instructions_doc}
