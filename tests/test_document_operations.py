__author__ = 'Bohdan Mushkevych'

import unittest
from datetime import datetime, timedelta

from odm import document, fields


class SimpleContainer(document.BaseDocument):
    field_string = fields.StringField()
    field_integer = fields.IntegerField()
    field_boolean = fields.BooleanField()
    field_datetime = fields.DateTimeField()
    field_decimal = fields.DecimalField(precision=3)


class TestDocument(unittest.TestCase):
    def setUp(self):
        self.model = SimpleContainer()

    def tearDown(self):
        del self.model

    def test_init(self):
        now = datetime.now()

        self.model = SimpleContainer(field_boolean=True,
                                     field_string='a short string description',
                                     field_datetime=now,
                                     field_decimal=123.123,
                                     field_integer=123)

        self.assertTrue(self.model.field_boolean)
        self.assertEqual(self.model.field_datetime, now)
        self.assertEqual(self.model.field_decimal, 123.123)
        self.assertEqual(self.model.field_integer, 123)
        self.assertEqual(self.model.field_string, 'a short string description')

    def test_init_dict(self):
        now = datetime.now()

        self.model = SimpleContainer(field_boolean=True,
                                     field_string='a short string description',
                                     field_datetime=now,
                                     field_decimal=123.123,
                                     field_integer=123)

        self.assertTrue(self.model.field_boolean)
        self.assertEqual(self.model.field_datetime, now)
        self.assertEqual(self.model.field_decimal, 123.123)
        self.assertEqual(self.model.field_integer, 123)
        self.assertEqual(self.model.field_string, 'a short string description')

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
        self.assertTrue(self.model.field_datetime - m2.field_datetime < timedelta(seconds=1))
        self.assertAlmostEqual(self.model.field_decimal, float(m2.field_decimal), delta=0.01)
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

        self.model['field_boolean'] = True
        self.model['field_string'] = 'a short string description'
        self.model['field_datetime'] = now
        self.model['field_decimal'] = 123.123
        self.model['field_integer'] = 123

        self.assertTrue(self.model.field_boolean)
        self.assertEqual(self.model.field_datetime, now)
        self.assertEqual(self.model.field_decimal, 123.123)
        self.assertEqual(self.model.field_integer, 123)
        self.assertEqual(self.model.field_string, 'a short string description')

    def test_contains(self):
        now = datetime.now()

        self.assertNotIn('field_boolean', self.model)
        self.assertNotIn('field_string', self.model)
        self.assertNotIn('field_datetime', self.model)
        self.assertNotIn('field_decimal', self.model)
        self.assertNotIn('field_integer', self.model)

        self.model['field_boolean'] = True
        self.model['field_string'] = 'a short string description'
        self.model['field_datetime'] = now
        self.model['field_decimal'] = 123.123
        self.model['field_integer'] = 123

        self.assertIn('field_boolean', self.model)
        self.assertIn('field_string', self.model)
        self.assertIn('field_datetime', self.model)
        self.assertIn('field_decimal', self.model)
        self.assertIn('field_integer', self.model)

    def test_delete_dict_style(self):
        now = datetime.now()

        self.model['field_boolean'] = True
        self.model['field_string'] = 'a short string description'
        self.model['field_datetime'] = now
        self.model['field_decimal'] = 123.123
        self.model['field_integer'] = 123

        self.assertIn('field_boolean', self.model)
        self.assertIn('field_string', self.model)
        self.assertIn('field_datetime', self.model)
        self.assertIn('field_decimal', self.model)
        self.assertIn('field_integer', self.model)

        del self.model['field_integer']
        del self.model['field_boolean']
        del self.model['field_string']
        del self.model['field_datetime']
        del self.model['field_decimal']

        self.assertNotIn('field_boolean', self.model)
        self.assertNotIn('field_string', self.model)
        self.assertNotIn('field_datetime', self.model)
        self.assertNotIn('field_decimal', self.model)
        self.assertNotIn('field_integer', self.model)

    def test_delete_attr_style(self):
        now = datetime.now()

        self.model['field_boolean'] = True
        self.model['field_string'] = 'a short string description'
        self.model['field_datetime'] = now
        self.model['field_decimal'] = 123.123
        self.model['field_integer'] = 123

        self.assertIn('field_boolean', self.model)
        self.assertIn('field_string', self.model)
        self.assertIn('field_datetime', self.model)
        self.assertIn('field_decimal', self.model)
        self.assertIn('field_integer', self.model)

        del self.model.field_integer
        del self.model.field_boolean
        del self.model.field_string
        del self.model.field_datetime
        del self.model.field_decimal

        self.assertNotIn('field_boolean', self.model)
        self.assertNotIn('field_string', self.model)
        self.assertNotIn('field_datetime', self.model)
        self.assertNotIn('field_decimal', self.model)
        self.assertNotIn('field_integer', self.model)

    def test_field_order_manualnaming(self):
        class Container(document.BaseDocument):
            a = fields.StringField(field_name='aaa', null=False)
            z = fields.StringField(field_name='zzz', null=False)
            k = fields.StringField(field_name='kkk', null=False)
            b = fields.StringField(field_name='bbb', null=False)

        self.assertListEqual(Container._get_ordered_field_names(), ['aaa', 'zzz', 'kkk', 'bbb'])

    def test_field_order_autoname(self):
        class Container(document.BaseDocument):
            a = fields.StringField(null=False)
            z = fields.StringField(null=False)
            k = fields.StringField(null=False)
            b = fields.StringField(null=False)

        self.assertListEqual(Container._get_ordered_field_names(), ['a', 'z', 'k', 'b'])


if __name__ == '__main__':
    unittest.main()
