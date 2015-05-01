# -*- coding: utf-8 -*-

import unittest, datetime
from nose2.tools import such
from santa.models.domain.product import Product
from santa.models.domain.image import Image
from tests import AppLifeCycle
from mongoengine import ValidationError

with such.A('Product model') as it:
    it.uses(AppLifeCycle)

    with it.having('fields'):
        @it.should('require title')
        def test_require_title(case):
            product = Product()
            case.assertRaisesRegexp(ValidationError, "Field is required: \['title'\]", product.save)

        @it.should('have optional attributes')
        def test_have_optional_attributes(case):
            description = u"""想要營造具有獨特風味的生活環境嗎？那一定少不了它囉～
                              這款【綠野仙蹤抱枕45x45cm 放輕鬆】時尚風格，運用仿麻材質布套，
                              搭配鮮艷卡通圖案，可當靠枕、墊枕、抱枕等使用，可擺放於客廳、臥房等；
                              此外，抱枕除實用功能外，更能大大提升室內空間的層次美感，
                              還再羨慕別人的家嗎？趕快帶它回家吧，您也可以輕鬆擁有設計感的小窩喔！"""
            product = Product(title=u'綠野仙蹤抱枕45x45cm 放輕鬆',
                              seller_product_id='014089478',
                              brand='HOLA',
                              size=u'長16 寬45 高45 (cm)',
                              urls=['http://www.hola.com.tw/product/detail/id/479883'],
                              description=description,
                              notes=u'只剩 3 件').save()
            case.assertEqual(product.title, u'綠野仙蹤抱枕45x45cm 放輕鬆')
            case.assertEqual(product.seller_product_id, '014089478')
            case.assertEqual(product.brand, 'HOLA')
            case.assertEqual(product.size, u'長16 寬45 高45 (cm)')
            case.assertEqual(product.urls, ['http://www.hola.com.tw/product/detail/id/479883'])
            case.assertEqual(product.description, description)
            case.assertEqual(product.notes, u'只剩 3 件')
            # Attributes without values
            for attr in ['color', 'images', 'updated_at', 'created_at']:
                case.assertTrue(hasattr(product, attr))
            case.assertIsNone(product.color)
            case.assertEqual(product.images, [])

        @it.should('have images attribute with embedded images')
        def test_have_images_attributes_with_embedded_images(case):
            images = [
                Image(small='https://takoman.co/path/to/image1/small.jpg',
                      original='https://takoman.co/path/to/image1/original.jpg'),
                Image(large='https://takoman.co/path/to/image2/large.jpg',
                      original='https://takoman.co/path/to/image2/original.jpg')
            ]
            Product(title='御茶園極上紅茶', images=images).save()
            product_images = Product.objects(title='御茶園極上紅茶').first().images
            case.assertEqual(len(product_images), 2)
            case.assertEqual(product_images[0].small,
                             'https://takoman.co/path/to/image1/small.jpg')
            case.assertEqual(product_images[0].original,
                             'https://takoman.co/path/to/image1/original.jpg')
            case.assertEqual(product_images[1].large,
                             'https://takoman.co/path/to/image2/large.jpg')
            case.assertEqual(product_images[1].original,
                             'https://takoman.co/path/to/image2/original.jpg')

        with it.having('created_at and updated_at'):
            @it.should('have default created_at and updated_at timestamps')
            def test_have_default_created_at_and_updated_at(case):
                Product(title='iPhone 99s').save()
                now = datetime.datetime.utcnow()
                created_at = Product.objects(title='iPhone 99s').first().created_at
                updated_at = Product.objects(title='iPhone 99s').first().updated_at
                # TODO: We should freeze time with something like freezegun.
                case.assertLess((now - created_at).seconds, 5)
                case.assertLess((now - updated_at).seconds, 5)

            @it.should('have correct created_at and updated_at after update')
            @unittest.skip('Wait until we can freeze the time in MongoEngine')
            def test_have_correct_created_at_and_updated_at_after_update(case):
                pass

it.createTests(globals())
