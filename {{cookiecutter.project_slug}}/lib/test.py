import pytest
from flask import url_for


def assert_status_with_message(status_code=200, response=None, message=None):
    """
    Check to see if a message is contained within a response

    :param status_code: Status code that defaults to 200
    :param response: Flask response
    :param message: string to check for
    :return: None
    """
    assert response.status_code == status_code
    assert message in str(response.data)


class ViewTestMixin(object):
    """
    Automatically load in a session and client, this is common for a lot of
    tests that work with views.
    """

    @pytest.fixture(autouse=True)
    def set_common_fixtures(self, session, client):
        self.session = session
        self.client = client

    def login(self, identity="admin@headshots.ai", password="password"):
        """
        Login a specific user

        :return: Flask response
        """
        return login(self.client, identity, password)

    def logout(self):
        """
        Logout a specific user

        :return: Flask response
        """
        return logout(self.client)


def login(client, email, password):
    """
    Login a specific user

    :param client: Flask client
    :param username:
    :param password:
    :return: Flask response
    """
    user = dict(email=email, passowrd=password)
    response = client.post(
        url_for("user.login"), data=user, follow_redirects=True)

    return response


def logout(client):
    """
    Log a specific user out

    :param client: Flask client
    :return: Flask response
    """
    return client.get(url_for("user.logout"), follow_redirects=True)
