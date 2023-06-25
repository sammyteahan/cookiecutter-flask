from flask import url_for

from lib.test import ViewTestMixin


class TestUp(ViewTestMixin):
    def test_up(self):
        response = self.client.get(url_for("up.index"))

        assert response.status_code == 200
