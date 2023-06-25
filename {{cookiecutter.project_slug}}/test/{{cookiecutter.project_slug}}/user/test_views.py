from flask import url_for

from lib.test import ViewTestMixin
from {{ cookiecutter.project_slug }}.blueprints.user.models import User


class TestLogin(ViewTestMixin):
    def test_login_page(self):
        """ Login page renders correctly """
        response = self.client.get(url_for("user.login"))
        assert response.status_code == 200

    def test_login(self):
        """ Login successfully """
        response = self.login()
        assert response.status_code == 200

    def test_login_fail(self, client, users):
        """ Login failure """
        response = client.post(url_for("user.login"), data={
            "email": "admin@{{ cookiecutter.project_slug }}.com",
            "password": "asdf"
        }, follow_redirects=True)

        assert response.status_code == 200
        assert "Email or password incorrect" in str(response.data)

    def test_login_update_activity(self, client, users):
        """ Ensure signing in updates log in activity """
        user = User.find_by_email("admin@{{ cookiecutter.project_slug }}.com")
        original_sign_in_count = user.sign_in_count

        response = client.post(url_for("user.login"), data={
            "email": "admin@{{ cookiecutter.project_slug }}.com",
            "password": "password"
        }, follow_redirects=True)

        assert response.status_code == 200
        assert (original_sign_in_count + 1) == user.sign_in_count
