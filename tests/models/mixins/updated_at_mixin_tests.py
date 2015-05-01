"""
    tests.models.mixins.updated_at_mixin
    ~~~~~~~~~~~~~~~~~~~~~~~~~~
    mixin to update the updated_at timestamp before save
"""
import unittest, datetime
from tests import AppTestCase
from mongoengine import *
from freezegun import freeze_time
from santa.models.mixins.updated_at_mixin import UpdatedAtMixin

class Post(Document):
    title      = StringField(required=True, max_length=200)
    updated_at = DateTimeField(default=datetime.datetime.utcnow)

class UpdatablePost(UpdatedAtMixin, Document):
    title      = StringField(required=True, max_length=200)
    updated_at = DateTimeField(default=datetime.datetime.utcnow)

class UpdatedAtMixinTests(AppTestCase):
    """Test cases for the updated_at mixin."""

    def test_regular_document_not_update_updated_at(self):
        # TODO: Ideally, we should be able to freeze time and create a post,
        # and the default updated_at should use the frozen time.
        post = Post(title='Old Post Title',
                    updated_at=datetime.datetime(2009, 8, 15, 12, 0, 1)).save()
        with freeze_time('2010-02-02 12:00:01'):
            post.title = 'New Post Title'
            post.save()

        post = Post.objects(title='New Post Title').first()
        self.assertEqual(post.updated_at, datetime.datetime(2009, 8, 15, 12, 0, 1))

    def test_mixed_in_document_update_updated_at_automatically(self):
        post = UpdatablePost(title='Old Post Title').save()
        with freeze_time('2010-02-02 12:00:01'):
            post.title = 'New Post Title'
            post.save()

        post = UpdatablePost.objects(title='New Post Title').first()
        self.assertEqual(post.updated_at, datetime.datetime(2010, 2, 2, 12, 0, 1))

if __name__ == '__main__':
    unittest.main()
