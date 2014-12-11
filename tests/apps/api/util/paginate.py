"""
    tests.api.util.paginate
    ~~~~~~~~~~~~~~~~~~~~~~~~~~
    api util pagination helper
"""
import unittest
from tests import AppTestCase
from mongoengine import *
from santa.apps.api.util.paginate import paginate
from santa.lib.api_errors import ApiException

class Post(Document):
    title = StringField(required=True, max_length=200)

class PaginateTests(AppTestCase):
    """Test cases for the paginate utility."""

    def setUp(self):
        super(PaginateTests, self).setUp()
        for i in range(42):  # 0, 1, ..., 40, 41
            Post(title="post: %s" % i).save()

    def test_without_page_and_size_params(self):
        paginated = paginate(Post.objects)
        self.assertIsInstance(paginated, list)
        self.assertEqual(len(paginated), 10)
        for i in range(10):
            self.assertEqual(paginated[i].title, "post: %s" % i)

    def test_with_page_without_size_param(self):
        for i in range(0, 40, 10):
            page = i / 10 + 1
            paginated = paginate(Post.objects, { 'page': page })
            self.assertIsInstance(paginated, list)
            self.assertEqual(len(paginated), 10)
            for j in range(10):
                self.assertEqual(paginated[j].title, "post: %s" % ((page - 1) * 10 + j))
        paginated = paginate(Post.objects, { 'page': 5 })
        self.assertIsInstance(paginated, list)
        self.assertEqual(len(paginated), 2)
        self.assertEqual(paginated[0].title, "post: %s" % 40)
        self.assertEqual(paginated[1].title, "post: %s" % 41)

    def test_with_size_without_page_param(self):
        paginated = paginate(Post.objects, { 'size': 40 })
        self.assertIsInstance(paginated, list)
        self.assertEqual(len(paginated), 40)
        for i in range(40):
            self.assertEqual(paginated[i].title, "post: %s" % i)

    def test_with_large_size_without_page_param(self):
        paginated = paginate(Post.objects, { 'size': 100 })
        self.assertIsInstance(paginated, list)
        self.assertEqual(len(paginated), 42)
        for i in range(42):
            self.assertEqual(paginated[i].title, "post: %s" % i)

    def test_with_page_and_size_params(self):
        size = 19
        for i in range(0, 38, size):
            page = i / size + 1
            paginated = paginate(Post.objects, { 'page': page, 'size': size })
            self.assertIsInstance(paginated, list)
            self.assertEqual(len(paginated), size)
            for j in range(size):
                self.assertEqual(paginated[j].title, "post: %s" % ((page - 1) * size + j))
        paginated = paginate(Post.objects, { 'page': 3, 'size': size })
        self.assertIsInstance(paginated, list)
        self.assertEqual(len(paginated), 4)
        for i in range(4):
            self.assertEqual(paginated[i].title, "post: %s" % (38 + i))

    def test_with_string_page_and_size_params(self):
        paginated = paginate(Post.objects, { 'page': '2', 'size': '5' })
        self.assertIsInstance(paginated, list)
        self.assertEqual(len(paginated), 5)
        for i in range(5):
            self.assertEqual(paginated[i].title, "post: %s" % (5 + i))

    def test_no_results(self):
        paginated = paginate(Post.objects, { 'page': 0 })
        self.assertEqual(paginated, [])
        paginated = paginate(Post.objects, { 'page': -1 })
        self.assertEqual(paginated, [])
        paginated = paginate(Post.objects, { 'page': 6 })
        self.assertEqual(paginated, [])
        paginated = paginate(Post.objects, { 'page': 6, 'size': 10 })
        self.assertEqual(paginated, [])

    def test_with_invalid_params(self):
        with self.assertRaisesRegexp(ApiException, 'size param exceeds maximum 100'):
            paginate(Post.objects, { 'size': 101 })
        with self.assertRaisesRegexp(ValueError, "invalid literal for int\(\) with base 10:.*"):
            paginate(Post.objects, { 'page': '1.5' })

if __name__ == '__main__':
    unittest.main()
