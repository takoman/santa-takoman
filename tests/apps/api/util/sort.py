"""
    tests.api.util.sort
    ~~~~~~~~~~~~~~~~~~~~~~~~~~
    api util sorting helper
"""
import unittest, os, santa
from mongoengine import *
from datetime import datetime
from santa import create_app
from santa.apps.api.util.sort import sort

class Post(Document):
    title      = StringField(required=True)
    category   = StringField()
    created_at = DateTimeField(default=datetime.now)

class PaginateTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        current_dir = os.path.dirname(os.path.realpath(santa.__file__))
        os.environ['SANTA_SETTINGS'] = current_dir + '/config/settings_test.py'

    def setUp(self):
        self.app = create_app()
        self.test_client = self.app.test_client()
        Post(title='post 1', category='Sports', created_at=datetime(2014, 11, 29, 8, 30, 20, 000000)).save()
        Post(title='post 2', category='Art', created_at=datetime(2014, 11, 28, 8, 30, 20, 000000)).save()
        Post(title='post 3', category='Science', created_at=datetime(2014, 11, 27, 8, 30, 20, 000000)).save()

    def tearDown(self):
        # Drop database
        for doc in [Post]:
            doc.drop_collection()
        self.app.db.drop_database(self.app.config['MONGO_DBNAME'])
        self.app.db.close()
        del self.app

    def test_without_sort_param(self):
        sorted = sort(Post.objects)
        self.assertIsInstance(sorted, QuerySet)
        self.assertEqual(len(Post.objects), len(sorted))
        for u, s in zip(Post.objects, sorted):
            self.assertEqual(u.title, s.title)
            self.assertEqual(u.category, s.category)
            self.assertEqual(u.created_at, s.created_at)

    def test_with_invalid_sort_param(self):
        sorted = sort(Post.objects, { 'sort': 'random' })
        self.assertIsInstance(sorted, QuerySet)
        self.assertEqual(len(Post.objects), len(sorted))
        for u, s in zip(Post.objects, sorted):
            self.assertEqual(u.title, s.title)
            self.assertEqual(u.category, s.category)
            self.assertEqual(u.created_at, s.created_at)

    def test_ascending_sort(self):
        sorted = sort(Post.objects, { 'sort': 'created_at' })
        self.assertIsInstance(sorted, QuerySet)
        self.assertEqual(len(Post.objects), len(sorted))
        self.assertEqual(sorted[0].title, 'post 3')
        self.assertEqual(sorted[1].title, 'post 2')
        self.assertEqual(sorted[2].title, 'post 1')

    def test_decending_sort(self):
        sorted = sort(Post.objects, { 'sort': '-category' })
        self.assertIsInstance(sorted, QuerySet)
        self.assertEqual(len(Post.objects), len(sorted))
        self.assertEqual(sorted[0].title, 'post 1')
        self.assertEqual(sorted[1].title, 'post 3')
        self.assertEqual(sorted[2].title, 'post 2')

    @unittest.skip('don\'t know how to do this... :(')
    def test_case_insensitive_sort(self):
        pass

    def test_multiple_sort_fields(self):
        Post(title='post 4', category='Business', created_at=datetime(2014, 11, 26, 8, 30, 20, 000000)).save()
        Post(title='post 4', category='Business', created_at=datetime(2014, 11, 25, 8, 30, 20, 000000)).save()
        Post(title='post 4', category='Cup cake', created_at=datetime(2014, 11, 24, 8, 30, 20, 000000)).save()
        sorted = sort(Post.objects, { 'sort': '-title,category,-created_at' })
        self.assertIsInstance(sorted, QuerySet)
        self.assertEqual(len(Post.objects), len(sorted))
        self.assertEqual(sorted[0].title, 'post 4')
        self.assertEqual(sorted[0].category, 'Business')
        self.assertEqual(sorted[0].created_at, datetime(2014, 11, 26, 8, 30, 20, 000000))
        self.assertEqual(sorted[1].title, 'post 4')
        self.assertEqual(sorted[1].category, 'Business')
        self.assertEqual(sorted[1].created_at, datetime(2014, 11, 25, 8, 30, 20, 000000))
        self.assertEqual(sorted[2].title, 'post 4')
        self.assertEqual(sorted[2].category, 'Cup cake')
        self.assertEqual(sorted[3].title, 'post 3')
        self.assertEqual(sorted[4].title, 'post 2')
        self.assertEqual(sorted[5].title, 'post 1')

if __name__ == '__main__':
    unittest.main()
