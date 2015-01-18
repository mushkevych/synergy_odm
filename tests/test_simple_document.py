__author__ = 'Bohdan Mushkevych'

import unittest
from datetime import datetime

from odm import document, fields


class SimpleContainer(document.BaseDocument):
    field_string = fields.StringField('s')
    field_integer = fields.IntegerField('i')
    field_boolean = fields.BooleanField('b')
    field_datetime = fields.DateTimeField('dt')
    field_decimal = fields.DecimalField('d')


class TestDocument(unittest.TestCase):
    def setUp(self):
        self.model = SimpleContainer()

    def tearDown(self):
        del self.model

    def test_getter_setter(self):
        now = datetime.now()

        self.model.field_boolean = True
        self.model.field_string = 'a short string description'
        self.model.field_datetime = now
        self.model.field_decimal = 123.123
        self.model.field_integer = 123

        self.assertTrue(self.model.field_boolean)
        self.assertEqual(self.model.field_datetime, now)
        self.assertEqual(self.model.field_decimal, 123.123)
        self.assertEqual(self.model.field_integer, 123)
        self.assertEqual(self.model.field_string, 'a short string description')

    def test_jsonification(self):
        now = datetime.now()

        self.model.field_boolean = True
        self.model.field_string = 'a short string description'
        self.model.field_datetime = now
        self.model.field_decimal = 123.123
        self.model.field_integer = 123

        json_data = self.model.to_json()
        self.assertIsInstance(json_data, dict)
        m2 = SimpleContainer.from_json(json_data)

        self.assertEqual(self.model.field_boolean, m2.field_boolean)
        self.assertEqual(self.model.field_datetime, m2.field_datetime)
        self.assertEqual(self.model.field_decimal, m2.field_decimal)
        self.assertEqual(self.model.field_integer, m2.field_integer)
        self.assertEqual(self.model.field_string, m2.field_string)

        self.model.field_integer = 999
        self.assertNotEqual(self.model.field_integer, m2.field_integer)

    def test_isolation(self):
        self.model2 = SimpleContainer()
        self.model.field_decimal = 123.123
        self.model2.field_decimal = 678.987

        self.assertEqual(self.model.field_decimal, 123.123)
        self.assertEqual(self.model2.field_decimal, 678.987)

    def test_dict_getter_setter(self):
        now = datetime.now()

        self.model['b'] = True
        self.model['s'] = 'a short string description'
        self.model['dt'] = now
        self.model['d'] = 123.123
        self.model['i'] = 123

        self.assertTrue(self.model.field_boolean)
        self.assertEqual(self.model.field_datetime, now)
        self.assertEqual(self.model.field_decimal, 123.123)
        self.assertEqual(self.model.field_integer, 123)
        self.assertEqual(self.model.field_string, 'a short string description')

    def test_contains(self):
        now = datetime.now()

        self.model['b'] = True
        self.model['s'] = 'a short string description'
        self.model['dt'] = now
        self.model['d'] = 123.123
        self.model['i'] = 123

        self.assertTrue('b' in self.model)
        self.assertTrue('s' in self.model)
        self.assertTrue('dt' in self.model)
        self.assertTrue('d' in self.model)
        self.assertTrue('i' in self.model)

        self.assertFalse('field_boolean' in self.model)
        self.assertFalse('field_string' in self.model)
        self.assertFalse('field_datetime' in self.model)
        self.assertFalse('field_decimal' in self.model)
        self.assertFalse('field_integer' in self.model)


if __name__ == '__main__':
    unittest.main()
