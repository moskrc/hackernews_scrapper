import unittest
import requests_mock
import datetime

from app import create_app, db
from app.utils import hn_scrapper


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
    def test_is_list(self, m):
        m.get('https://news.ycombinator.com/', text=self.fixture_html)
        res = hn_scrapper.get_news_list()

        self.assertTrue(type(res) == list)

    @requests_mock.Mocker()
    def test_columns(self, m):
        m.get('https://news.ycombinator.com/', text=self.fixture_html)
        res = hn_scrapper.get_news_list()
        assert res[0].keys() >= {'id', 'title',
                                 'approx_created_at', 'url', 'post_age'}

    @requests_mock.Mocker()
    def test_first_row(self, m):
        m.get('https://news.ycombinator.com/', text=self.fixture_html)
        res = hn_scrapper.get_news_list()

        self.assertEqual(res[0]['id'], '23962961')
        self.assertEqual(
            res[0]['title'], 'Amazon gets priority while mail gets delayed, say US letter carriers')
        self.assertEqual(
            res[0]['url'], 'https://www.pressherald.com/2020/07/21/first-class-and-priority-mail-delayed-in-favor-of-amazon-parcels-according-to-portland-letter-carriers/')
        self.assertEqual(res[0]['post_age'],
                         datetime.timedelta(0, 10800))

    @requests_mock.Mocker()
    def test_length(self, m):
        m.get('https://news.ycombinator.com/', text=self.fixture_html)
        res = hn_scrapper.get_news_list()

        self.assertEqual(len(res), 30)
