import unittest
import requests_mock
import datetime
from flask import json
from app import create_app, db
from app.utils import hn_scrapper
from app.tasks import fetch_data


class PostModelTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        with open('tests/fixtures/hn.html', 'r') as f:
            self.fixture_html = f.read()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    @requests_mock.Mocker()
    def test_home(self, m):
        m.get('https://news.ycombinator.com/', text=self.fixture_html)

        fetch_data()

        with self.app.test_client() as c:
            response = c.get('/api/v1/')
            self.assertEqual(response.status_code, 200)
            "Hacker News Grabber API"
            data = response.get_data(as_text=True)
            self.assertIn('<title>Hacker News Grabber API</title>', data)


    @requests_mock.Mocker()
    def test_api(self, m):
        m.get('https://news.ycombinator.com/', text=self.fixture_html)

        fetch_data()

        with self.app.test_client() as c:
            response = c.get('/api/v1/posts/')
            self.assertEqual(response.status_code, 200)
            data = json.loads(response.get_data(as_text=True))
            self.assertEqual(len(data), 10)

    @requests_mock.Mocker()
    def test_api_limit(self, m):
        m.get('https://news.ycombinator.com/', text=self.fixture_html)

        fetch_data()

        with self.app.test_client() as c:
            response = c.get('/api/v1/posts/?limit=5')
            self.assertEqual(response.status_code, 200)
            data = json.loads(response.get_data(as_text=True))
            self.assertEqual(len(data), 5)

    @requests_mock.Mocker()
    def test_api_offset(self, m):
        m.get('https://news.ycombinator.com/', text=self.fixture_html)

        fetch_data()

        with self.app.test_client() as c:
            response = c.get('/api/v1/posts/?limit=5&offset=2')
            self.assertEqual(response.status_code, 200)
            data = json.loads(response.get_data(as_text=True))
            self.assertEqual(len(data), 5)
            self.assertEqual(data[0]['id'], '28')

    @requests_mock.Mocker()
    def test_api_order(self, m):
        m.get('https://news.ycombinator.com/', text=self.fixture_html)

        fetch_data()

        with self.app.test_client() as c:
            response = c.get('/api/v1/posts/?limit=5&offset=2&order=title')
            self.assertEqual(response.status_code, 200)
            data = json.loads(response.get_data(as_text=True))
            self.assertEqual(len(data), 5)
            self.assertEqual(data[0]['id'], '9')

    @requests_mock.Mocker()
    def test_api_order_asc(self, m):
        m.get('https://news.ycombinator.com/', text=self.fixture_html)

        fetch_data()

        with self.app.test_client() as c:
            response = c.get('/api/v1/posts/?limit=5&offset=2&order=id&dir=asc')
            self.assertEqual(response.status_code, 200)
            data = json.loads(response.get_data(as_text=True))
            self.assertEqual(len(data), 5)
            self.assertEqual(data[0]['id'], '3')
