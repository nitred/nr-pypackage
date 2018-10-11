"""Create flask-login's objects."""
from flask_login import LoginManager

auth_manager = LoginManager()
auth_manager.session_protection = "strong"
auth_manager.login_view = "auth.login"
