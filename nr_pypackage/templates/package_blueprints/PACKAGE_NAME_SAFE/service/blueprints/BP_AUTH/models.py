"""Create a USER object or model. Also decorate a user_loader function."""
raise NotImplementedError("""Function called `is_ldap_authenticated_user` has not been implemented.

Please import or create a function called `is_ldap_authenticated_user` that accepts `username` and `password`
as arguments and verifies them against an LDAPServer and returns a bool indicating if the user is authenticated.
""")

from .manager import auth_manager


class LDAPUser(object):
    """The LDAPUser is a class for creating a User object for the sake of Flask-Login.

    This class assumes there is an LDAPServer against which the username and password can be verfied. Once the username
    and password are verified, then password is thrown away. The username is also used as the unique ID to refer to the
    User. Flask-Login will create unique session IDs based on the LDAP ID (i.e. LDAP username). No other details of the
    user are required.

    How to use?
    First use the LDAPUser.authenticate_and_init() classmethod to first authenticate the username and password against
    the LDAP server and then create the LDAPUser object. Once the authentication is done within this classmethod an
    object of LDAPUser is created with ONLY the username as the attribute and the password and other details are thrown
    away.
    """

    def __init__(self, username):
        """Create an instance of LDAPUser only with the username, provided the user has been authenticated beforehand.

        Args:
            username (str): Username of the user which is also used as the Unique ID of the user.
        """
        self.username = username

    @classmethod
    def authenticate_and_init(cls, username, password):
        """Return an instance of LDAPUser after authentication success else return None.

        Args:
            username (str): Username of the user which is also used as the Unique ID of the user.
            password (str): Password of the user which is used to verify against ldap and thrown away.

        Returns:
            LDAPUser or None: Returns LDAPUser object if authentication is successful else None.
        """
        if is_ldap_authenticated_user(username, password) is True:
            return cls(username=username)
        else:
            return None

    def is_authenticated(self):
        """Same as UserMixin. Return True."""
        return True

    def is_active(self):
        """Same as UserMixin. Return True."""
        return True

    def is_anonymous(self):
        """Same as UserMixin. Return False"""
        return False

    def get_id(self):
        """NOT the same as UserMixin. We assume that LDAP username is as good as ID."""
        return str(self.username)


@auth_manager.user_loader
def load_ldap_user(id):
    """Return the LDAPUser for the string ID which is actually the username."""
    print("load_user: {}".format(id))
    return LDAPUser(username=id)
