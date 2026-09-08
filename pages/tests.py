import pytest
from django.test import Client


class TestPagesViews:
    def test_home_page(self):
        client = Client()
        response = client.get('/')
        assert response.status_code == 200

    def test_about_page(self):
        client = Client()
        response = client.get('/about/')
        assert response.status_code == 200
