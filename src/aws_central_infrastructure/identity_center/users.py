"""Only use this if you do not have an external Identity Provider (e.g. Okta, Microsoft)."""

from lab_auto_pulumi import User


def create_users():
    _ = User(first_name="eli", last_name="fine", email="ejfine@gmail.com", use_deprecated_username_format=True)
    _ = User(first_name="Ethan", last_name="Ryter", email="ethanryter3@gmail.com")
