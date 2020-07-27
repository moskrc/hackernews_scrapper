import unittest

from app import create_app, db
from app.database.models import Post


class PostModelTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_title_setter(self):
        p = Post(title='news')
        self.assertTrue(p.id is None)
        self.assertTrue(p.title == 'news')
