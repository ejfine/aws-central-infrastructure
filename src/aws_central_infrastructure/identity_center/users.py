"""Only use this if you do not have an external Identity Provider (e.g. Okta, Microsoft)."""

from .lib import User


def create_users():
    _ = User(first_name="eli", last_name="fine", email="ejfine@gmail.com")
