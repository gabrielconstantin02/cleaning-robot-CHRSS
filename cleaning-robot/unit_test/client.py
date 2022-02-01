import pytest
from app import create_app

"""
Initialize the testing environment
Creates an app for testing that has the configuration flag ``TESTING`` set to
``True``.
"""

user_data = {
    'username': 'test_user',
    'password': 'test_pass'
}


@pytest.fixture
def client():
    """
    Configures the app for testing
    Sets app config variable ``TESTING`` to ``True``
    :return: App for testing
    """
    # app.config['TESTING'] = True
    local_app = create_app()
    with local_app.test_client() as client:
        with local_app.app_context():
            client.post("/auth/register", data=user_data, follow_redirects=True)
            client.post("/auth/login", data=user_data, follow_redirects=True)

            yield client


@pytest.fixture
def client_no_login():
    local_app = create_app()
    client = local_app.test_client()

    yield client