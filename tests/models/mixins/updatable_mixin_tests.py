# -*- coding: utf-8 -*-

import unittest, json
from tests import AppTestCase
from mongoengine import *
from mongoengine import ValidationError, NotUniqueError
from santa.models.mixins.updatable_mixin import UpdatableMixin
from santa.lib.api_errors import ApiException
from santa.lib.common import me_to_json

class Image(EmbeddedDocument):
    original    = URLField()
    small       = URLField()
    large       = URLField()

class Author(Document):
    name        = StringField(required=True)

class Post(UpdatableMixin, Document):
    title       = StringField(required=True, max_length=20, unique=True)
    images      = ListField(EmbeddedDocumentField(Image, default=Image))
    urls        = ListField(URLField())
    author      = ReferenceField(Author)
    # comments    = ListField(ReferenceField(Comment))

class UpdatableMixinTests(AppTestCase):
    """Test cases for the updatable mixin."""

    def setUp(self):
        super(UpdatableMixinTests, self).setUp()
        author = Author(name="Clare Tai").save()
        image1 = Image(original="http://takoman.co/image1/original.jpg")
        image2 = Image(original="http://takoman.co/image2/original.jpg",
                       small="http://takoman.co/image2/small.jpg")

        self.post = Post(title="Unchained Melody",
                         images=[image1, image2],
                         urls=["http://takoman.co/post1", "http://takoman.co/post1-1"],
                         author=author).save()

    def test_update_regular_fields(self):
        data = {
            "title": "Endless Love",
            "urls": ["http://takoman.co/new-post1", "http://takoman.co/new-post1-1"]
        }
        self.post.update_with_validation(data)
        self.post.reload()
        self.assertEqual(self.post.title, data["title"])
        self.assertEqual(self.post.urls, data["urls"])

    def test_update_embedded_fields(self):
        data = {
            "title": "Endless Love",
            "urls": ["http://takoman.co/new-post1", "http://takoman.co/new-post1-1"],
            "images": [
                {
                    "original": "http://takoman.co/image1/new-original.jpg",
                    "large": "http://takoman.co/image1/new-large.jpg"
                },
                {
                    "small": "http://takoman.co/image2/new-small.jpg",
                    "original": "http://takoman.co/image2/new-original.jpg"
                }
            ]
        }
        self.post.update_with_validation(data)
        self.post.reload()
        self.assertEqual(self.post.title, data["title"])
        self.assertEqual(self.post.urls, data["urls"])
        self.assertEqual(self.post.images, map(lambda x: Image(**x), data["images"]))

    def test_update_reference_fields_with_string_object_id(self):
        new_author = Author(name="starsirius").save()
        data = {
            "title": "Endless Love",
            "urls": ["http://takoman.co/new-post1", "http://takoman.co/new-post1-1"],
            "images": [
                {
                    "original": "http://takoman.co/image1/new-original.jpg",
                    "large": "http://takoman.co/image1/new-large.jpg"
                },
                {
                    "small": "http://takoman.co/image2/new-small.jpg",
                    "original": "http://takoman.co/image2/new-original.jpg"
                }
            ],
            "author": str(new_author.id)
        }
        self.post.update_with_validation(data)
        self.post.reload()
        self.assertEqual(self.post.title, data["title"])
        self.assertEqual(self.post.urls, data["urls"])
        self.assertEqual(self.post.images, map(lambda x: Image(**x), data["images"]))
        self.assertEqual(self.post.author, new_author)

    def test_update_reference_fields_with_dict(self):
        new_author = Author(name="starsirius").save()
        data = {
            "title": "Endless Love",
            "urls": ["http://takoman.co/new-post1", "http://takoman.co/new-post1-1"],
            "images": [
                {
                    "original": "http://takoman.co/image1/new-original.jpg",
                    "large": "http://takoman.co/image1/new-large.jpg"
                },
                {
                    "small": "http://takoman.co/image2/new-small.jpg",
                    "original": "http://takoman.co/image2/new-original.jpg"
                }
            ],
            "author": json.loads(me_to_json(new_author))
        }
        self.post.update_with_validation(data)
        self.post.reload()
        self.assertEqual(self.post.title, data["title"])
        self.assertEqual(self.post.urls, data["urls"])
        self.assertEqual(self.post.images, map(lambda x: Image(**x), data["images"]))
        self.assertEqual(self.post.author, new_author)

    def test_ignore_id_in_data_if_identical_to_self(self):
        data = {
            "id": str(self.post.id),
            "title": "Random Title"
        }
        self.post.update_with_validation(data)
        self.post.reload()
        self.assertEqual(str(self.post.id), data["id"])
        self.assertEqual(self.post.title, data["title"])

    def test_different_id_in_data_than_self(self):
        new_post = Post(title="Random Post").save()
        with self.assertRaisesRegexp(ApiException, "unable to update Post with data with a different id"):
            self.post.update_with_validation({ "id": str(new_post.id) })

    def test_updating_with_other_validations(self):
        Post(title="Do Not Repeat").save()
        with self.assertRaisesRegexp(NotUniqueError, ".*duplicate key error.*"):
            self.post.update_with_validation({ "title": "Do Not Repeat" })

        with self.assertRaisesRegexp(ValidationError, ".*String value is too long.*"):
            self.post.update_with_validation({ "title": "12345678901234567890extra" })

        with self.assertRaisesRegexp(ValidationError, ".*not valid url.*"):
            self.post.update_with_validation({ "urls": ["not valid url", "random string"] })

    @unittest.skip("UpdatableMixin should support update by passing a list of dicts of reference fields")
    def test_update_list_of_reference_fields(self):
        pass

if __name__ == '__main__':
    unittest.main()
