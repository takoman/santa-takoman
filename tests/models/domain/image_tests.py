# -*- coding: utf-8 -*-

import unittest, json
from mongoengine import *
from santa.models.domain import *
from santa.lib.common import me_to_json
from tests import AppTestCase

class Gallery(Document):
    images = ListField(EmbeddedDocumentField(Image))

class ImageTests(AppTestCase):
    def setUp(self):
        super(ImageTests, self).setUp()
        self.gallery = Gallery(
            images=[
                Image(original='http://takoman.co/image1/original.jpg',
                      small='http://takoman.co/image1/small.jpg',
                      square='http://takoman.co/image1/square.jpg'),
                Image(original='http://takoman.co/image2/original.jpg',
                      medium='http://takoman.co/image2/medium.jpg',
                      large='http://takoman.co/image2/large.jpg'),
            ]
        ).save()

    def test_image_only_contains_defined_versions(self):
        expected = [
            {
                'original': 'http://takoman.co/image1/original.jpg',
                'small': 'http://takoman.co/image1/small.jpg',
                'square': 'http://takoman.co/image1/square.jpg'
            },
            {
                'original': 'http://takoman.co/image2/original.jpg',
                'medium': 'http://takoman.co/image2/medium.jpg',
                'large': 'http://takoman.co/image2/large.jpg'
            }
        ]
        self.assertListEqual(json.loads(me_to_json(self.gallery.images)), expected)

if __name__ == '__main__':
    unittest.main()
