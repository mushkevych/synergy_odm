# -*- coding: utf-8 -*-
__author__ = 'Bohdan Mushkevych'

import unittest

from odm import document, fields
from odm.errors import ValidationError

DEFAULT_VALUE = 'default value'


class TestDocument(unittest.TestCase):
    def test_field_autonaming(self):
        class FieldContainer(document.BaseDocument):
            field_string = fields.StringField(null=False)

        value = 'abcdefghijklmnopqrstuvwxyz'
        model = FieldContainer()
        model.field_string = value

        self.assertEqual(FieldContainer.field_string.name, 'field_string')
        self.assertIn('field_string', model.to_json())
        self.assertEqual(model.to_json()['field_string'], value)
        self.assertEqual(model.field_string, value)

    def test_valid_inputs(self):
        class FieldContainer(document.BaseDocument):
            field_string = fields.StringField(name='s', null=False)

        fixtures = {
            '1': '1',
            1: '1',
            150.001: '150.001',
            u'а ти диню нині їв, га?': u'а ти диню нині їв, га?',
            u'абвгдеєжзиіїйклмнопрстуфхцчшщюяь': u'абвгдеєжзиіїйклмнопрстуфхцчшщюяь',
            u'ウィキペディアにようこそ': u'ウィキペディアにようこそ',
            'abcdefghijklmnopqrstuvwxyz': 'abcdefghijklmnopqrstuvwxyz',
            'Jan 06, 2010': 'Jan 06, 2010',
        }

        model = FieldContainer()
        for key, value in fixtures.items():
            model.field_string = key
            self.assertEqual(model.field_string, value)

    def test_constraints(self):
        min_length = 5
        max_length = 10

        class FieldContainer(document.BaseDocument):
            field_string = fields.StringField(name='s', min_length=min_length, max_length=max_length)

        valid_min = 'a' * min_length
        valid_middle = 'b' * int((min_length + max_length) / 2)
        valid_max = 'c' * max_length
        invalid_min = 'i' * (min_length - 1)
        invalid_max = 'm' * (max_length + 1)

        model = FieldContainer()
        for value in [valid_min, valid_middle, valid_max]:
            model.field_string = value
            self.assertEqual(model.field_string, value)

        for value in [invalid_min, invalid_max]:
            try:
                model.field_string = value
                self.assertTrue(False, 'ValidationError should have been thrown')
            except ValidationError:
                self.assertTrue(True, 'ValidationError was expected and caught')

    def test_choices(self):
        class FieldContainer(document.BaseDocument):
            field_string = fields.StringField(name='s', choices=['111aaa', '222bbb', '333ccc'])

        model = FieldContainer()
        model.field_string = '111aaa'
        self.assertEqual(model.field_string, '111aaa')

        try:
            model.field_string = 'tra'
            self.assertTrue(False, 'ValidationError should have been thrown')
        except ValidationError:
            self.assertTrue(True, 'ValidationError was expected and caught')

    def test_nullable_non_default(self):
        class FieldContainer(document.BaseDocument):
            field_string = fields.StringField(name='s', null=True)

        model = FieldContainer()

        try:
            model.validate()
            self.assertTrue(True, 'Validation should succeed')
        except ValidationError:
            self.assertTrue(False, 'ValidationError should not have been thrown')

        model.field_string = None
        self.assertTrue(True, 'Validation should succeed')

    def test_non_nullable_non_default(self):
        class FieldContainer(document.BaseDocument):
            field_string = fields.StringField(name='s', null=False)

        model = FieldContainer()
        try:
            model.validate()
            self.assertTrue(False, 'Validation should have failed')
        except ValidationError:
            self.assertTrue(True, 'ValidationError should not have been thrown')

        model.field_string = 'first-level string field'
        self.assertEqual(model.field_string, 'first-level string field')

        try:
            model.field_string = None
            self.assertTrue(False, 'ValidationError should have been thrown')
        except ValidationError:
            self.assertTrue(True, 'ValidationError was expected and caught')

    def test_non_nullable_default(self):
        class FieldContainer(document.BaseDocument):
            field_string = fields.StringField(name='s', null=False, default=DEFAULT_VALUE)
            field_string_empty = fields.StringField(name='empty', null=False, default='')

        model = FieldContainer()
        self.assertEqual(model.field_string, DEFAULT_VALUE)
        self.assertEqual(model.field_string_empty, '')

    def test_nullable_default(self):
        class FieldContainer(document.BaseDocument):
            field_string = fields.StringField(name='s', null=True, default=DEFAULT_VALUE)

        model = FieldContainer()
        self.assertIsNone(model.field_string)

        model.field_string = None
        self.assertIsNone(model.field_string)

    def test_nullable_non_default_jsonification(self):
        class FieldContainer(document.BaseDocument):
            field_string = fields.StringField(name='s', null=True)

        model = FieldContainer()
        json_data = model.to_json()
        self.assertIsInstance(json_data, dict)
        m2 = FieldContainer.from_json(json_data)

        self.assertIsNone(m2.field_string)

    def test_non_nullable_non_default_jsonification(self):
        class FieldContainer(document.BaseDocument):
            field_string = fields.StringField(name='s', null=False)

        model = FieldContainer()
        json_data = model.to_json()
        self.assertIsInstance(json_data, dict)
        m2 = FieldContainer.from_json(json_data)

        self.assertIsNone(m2.field_string)

    def test_non_nullable_default_jsonification(self):
        class FieldContainer(document.BaseDocument):
            field_string = fields.StringField(name='s', null=False, default=DEFAULT_VALUE)

        model = FieldContainer()
        json_data = model.to_json()
        self.assertIsInstance(json_data, dict)
        m2 = FieldContainer.from_json(json_data)

        self.assertEqual(m2.field_string, DEFAULT_VALUE)

    def test_nullable_default_jsonification(self):
        class FieldContainer(document.BaseDocument):
            field_string = fields.StringField(name='s', null=True, default=DEFAULT_VALUE)

        model = FieldContainer()
        json_data = model.to_json()
        self.assertIsInstance(json_data, dict)
        m2 = FieldContainer.from_json(json_data)

        self.assertIsNone(m2.field_string)


if __name__ == '__main__':
    unittest.main()
