# -*- coding: utf-8 -*-
__author__ = 'Bohdan Mushkevych'

import unittest
from datetime import datetime

from odm import document, fields


class ADocument(document.BaseDocument):
    alpha = fields.IntegerField(null=False)
    beta = fields.StringField(null=False)
    gama = fields.DecimalField(null=False)
    delta = fields.DateTimeField(null=False)
    epsilon = fields.BooleanField(null=False)
    zeta = fields.ObjectIdField(null=False)


class TestDocument(unittest.TestCase):
    def test_plural_key_fields(self):
        class Example(ADocument):
            @classmethod
            def key_fields(cls):
                return Example.alpha.name, Example.beta.name, Example.gama.name

        model = Example()
        model.alpha = 45
        model.beta = 'string'
        model.gama = 987654321
        model.other = 'something else'

        self.assertSequenceEqual(model.key, [45, 'string', 987654321])
        self.assertSequenceEqual(model.key_fields(), ['alpha', 'beta', 'gama'])
        self.assertSequenceEqual(Example.key_fields(), ['alpha', 'beta', 'gama'])

        model.key = [99, 'carabra', 12345]

        self.assertSequenceEqual(model.key, [99, 'carabra', 12345])
        self.assertSequenceEqual(model.key_fields(), ['alpha', 'beta', 'gama'])

        self.assertEqual(model.alpha, 99)
        self.assertEqual(model.beta, 'carabra')
        self.assertEqual(model.gama, 12345)
        self.assertEqual(model.other, 'something else')

    def test_int_key_fields(self):
        class Example(ADocument):
            @classmethod
            def key_fields(cls):
                return Example.alpha.name

        model = Example()

        model.alpha = 45
        self.assertEqual(model.key, 45)
        self.assertEqual(model.key_fields(), 'alpha')
        self.assertEqual(Example.key_fields(), 'alpha')

        model.key = 12345
        self.assertEqual(model.key, 12345)
        self.assertEqual(model.key_fields(), 'alpha')
        self.assertEqual(model.alpha, 12345)

    def test_str_key_fields(self):
        class Example(ADocument):
            @classmethod
            def key_fields(cls):
                return Example.beta.name

        model = Example()

        model.beta = 'string'
        self.assertEqual(model.key, 'string')
        self.assertEqual(model.key_fields(), 'beta')
        self.assertEqual(Example.key_fields(), 'beta')

        model.key = 'new value'
        self.assertEqual(model.key, 'new value')
        self.assertEqual(model.key_fields(), 'beta')
        self.assertEqual(model.beta, 'new value')

    def test_decimal_key_fields(self):
        class Example(ADocument):
            @classmethod
            def key_fields(cls):
                return Example.gama.name

        model = Example()

        model.gama = 987654321.123456789
        self.assertEqual(model.key, 987654321.12)
        self.assertEqual(model.key_fields(), 'gama')
        self.assertEqual(Example.key_fields(), 'gama')

        model.key = 1234567890.0123456789
        self.assertEqual(model.key, 1234567890.01)
        self.assertEqual(model.key_fields(), 'gama')
        self.assertEqual(model.gama, 1234567890.01)

    def test_dt_key_fields(self):
        class Example(ADocument):
            @classmethod
            def key_fields(cls):
                return Example.delta.name

        model = Example()

        model.delta = '2020-01-01 23:59:59'
        self.assertEqual(model.key, datetime(2020, 1, 1, 23, 59, 59))
        self.assertEqual(model.key_fields(), 'delta')
        self.assertEqual(Example.key_fields(), 'delta')

        model.key = '2222-10-10 23:59:59'
        self.assertEqual(model.key, datetime(2222, 10, 10, 23, 59, 59))
        self.assertEqual(model.key_fields(), 'delta')
        self.assertEqual(model.delta, datetime(2222, 10, 10, 23, 59, 59))

    def test_bool_key_fields(self):
        class Example(ADocument):
            @classmethod
            def key_fields(cls):
                return Example.epsilon.name

        model = Example()

        model.epsilon = False
        self.assertEqual(model.key, False)
        self.assertEqual(model.key_fields(), 'epsilon')
        self.assertEqual(Example.key_fields(), 'epsilon')

        model.key = True
        self.assertEqual(model.key, True)
        self.assertEqual(model.key_fields(), 'epsilon')
        self.assertEqual(model.epsilon, True)

    def test_objid_key_fields(self):
        class Example(ADocument):
            @classmethod
            def key_fields(cls):
                return Example.zeta.name

        model = Example()

        model.zeta = '9db7dabd-1519-40c8-90fb-fea0c7a93ffe'
        self.assertEqual(model.key, '9db7dabd-1519-40c8-90fb-fea0c7a93ffe')
        self.assertEqual(model.key_fields(), 'zeta')
        self.assertEqual(Example.key_fields(), 'zeta')

        model.key = '6889eda6-656e-4c42-b789-34c788a414b4'
        self.assertEqual(model.key, '6889eda6-656e-4c42-b789-34c788a414b4')
        self.assertEqual(model.key_fields(), 'zeta')
        self.assertEqual(model.zeta, '6889eda6-656e-4c42-b789-34c788a414b4')


if __name__ == '__main__':
    unittest.main()
