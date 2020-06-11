# -*- coding: utf-8 -*-
__author__ = 'Bohdan Mushkevych'

import unittest

from odm import document, fields


class TestDocument(unittest.TestCase):
    def test_plural_key_fields(self):
        class Example(document.BaseDocument):
            alpha = fields.IntegerField(null=False)
            beta = fields.StringField(null=False)
            gama = fields.IntegerField(null=False)
            other = fields.StringField(null=False)

            @classmethod
            def key_fields(cls):
                return Example.alpha.name, Example.beta.name, Example.gama.name

        model = Example()
        model.alpha = 45
        model.beta = 'string'
        model.gama = 987654321
        model.other = 'something else'

        self.assertListEqual(model.key, [45, 'string', 987654321])
        self.assertSequenceEqual(model.key_fields(), ['alpha', 'beta', 'gama'])
        self.assertSequenceEqual(Example.key_fields(), ['alpha', 'beta', 'gama'])

        model.key = [99, 'carabra', 12345]

        self.assertListEqual(model.key, [99, 'carabra', 12345])
        self.assertSequenceEqual(model.key_fields(), ['alpha', 'beta', 'gama'])

        self.assertEqual(model.alpha, 99)
        self.assertEqual(model.beta, 'carabra')
        self.assertEqual(model.gama, 12345)
        self.assertEqual(model.other, 'something else')

    def test_singular_key_fields(self):
        class Example(document.BaseDocument):
            alpha = fields.IntegerField(null=False)
            beta = fields.StringField(null=False)
            gama = fields.IntegerField(null=False)
            other = fields.StringField(null=False)

            @classmethod
            def key_fields(self):
                return Example.alpha.name

        model = Example()
        model.alpha = 45
        model.beta = 'string'
        model.gama = 987654321
        model.other = 'something else'

        self.assertEqual(model.key, 45)
        self.assertEqual(model.key_fields(), 'alpha')
        self.assertEqual(Example.key_fields(), 'alpha')

        model.key = 12345

        self.assertEqual(model.key, 12345)
        self.assertEqual(model.key_fields(), 'alpha')

        self.assertEqual(model.alpha, 12345)
        self.assertEqual(model.beta, 'string')
        self.assertEqual(model.gama, 987654321)
        self.assertEqual(model.other, 'something else')


if __name__ == '__main__':
    unittest.main()
