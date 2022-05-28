"""
Setups configurations and fixture
neccessary for running the tests
"""


import pytest
from flask_jwt_extended import create_access_token

from project import create_app, db
from project.models import Template, User


@pytest.fixture(autouse=True)
def app():
    """
    Enables each test run within
    the application context
    """

    test_app = create_app("test")
    with test_app.app_context():
        yield test_app


@pytest.fixture()
def client(app):
    """
    Sets up an api client for the tests
    """

    with app.test_client() as client:
        yield client


@pytest.fixture(autouse=True)
def default_user():
    """
    Sets up a default user to be available
    in all the tests (autouse=True)
    """

    user1 = User(email="test1@test.com", first_name="test", last_name="test")
    user2 = User(email="test2@test.com", first_name="test", last_name="test")
    user1.password = User.hash_password("test1_123")
    user2.password = User.hash_password("test2_123")
    user1.save()
    user2.save()
    yield user1, user2
    User.drop_collection()
    # user1.delete()
    # user2.delete()


@pytest.fixture
def default_template(default_user):
    """
    Sets up a default template object
    """
    owner1, owner2 = default_user
    template1 = Template(
        template_name="test_temp",
        subject="template",
        body="Testing template",
        owner=owner1,
    )
    template2 = Template(
        template_name="test_temp",
        subject="template",
        body="Testing template",
        owner=owner2,
    )
    template1.save()
    template2.save()
    yield template1.id, template2.id
    Template.drop_collection()
    # template1.delete()
    # template2.delete()


@pytest.fixture
def token(client, default_user):
    """
    Generates access token for testing
    authenticated endpoints
    """
    user1, user2 = default_user
    return create_access_token(identity=user1), create_access_token(identity=user2)
