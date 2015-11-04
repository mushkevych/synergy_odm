__author__ = 'Bohdan Mushkevych'

import unittest

from odm.errors import ValidationError
from odm import document, fields


class TestDocument(unittest.TestCase):
    def test_valid_formats(self):
        class FieldContainer(document.BaseDocument):
            field_boolean = fields.BooleanField('b', null=False)

        fixtures = {
            '1': True,
            1: True,
            'yes': True,
            'True': True,
            'tRue': True,
            'true': True,
            True: True,
            'no': False,
            0: False,
            '0': False,
            'False': False,
            'false': False,
            False: False,
        }

        model = FieldContainer()
        for key, value in fixtures.items():
            try:
                model.field_boolean = key
                self.assertEqual(model.field_boolean, value)

                model.validate()
                self.assertTrue(True, 'ValidationError should not have been thrown for pair {0}:{1}'
                                .format(key, value))
            except ValidationError:
                self.assertTrue(False, 'ValidationError was not expected but caught for pair {0}:{1}'
                                .format(key, value))
            except ValueError:
                self.assertTrue(False, 'ValueError was not expected but caught for pair {0}:{1}'
                                .format(key, value))

    def test_invalid_formats(self):
        class FieldContainer(document.BaseDocument):
            field_boolean = fields.BooleanField('b', null=False)

        fixtures = [2, 'ye', 'Tru', '3']

        model = FieldContainer()
        for value in fixtures:
            try:
                model.field_boolean = value
                self.assertTrue(False, 'ValidationError should have been thrown for value {0}'.format(value))
            except ValueError:
                self.assertTrue(True, 'ValueError was expected and caught for value {0}'.format(value))

    def test_custom_true_false(self):
        class FieldContainer(document.BaseDocument):
            field_boolean = fields.BooleanField('b', true_values=['5', '6', 'ya'], false_values=['2', 'n/a'])

        fixtures = {
            True: True,
            '5': True,
            6: True,
            'Ya': True,
            'N/A': False,
            2: False,
            False: False
        }

        model = FieldContainer()
        for key, value in fixtures.items():
            try:
                model.field_boolean = key
                self.assertEqual(model.field_boolean, value, 'Pair {0}:{1} does not match'.format(key, value))
            except ValidationError:
                self.assertTrue(False, 'ValidationError was not expected but caught for pair {0}:{1}'
                                       .format(key, value))
            except ValueError:
                self.assertTrue(False, 'ValueError was not expected but caught for pair {0}:{1}'
                                       .format(key, value))

    def test_nullable(self):
        class FieldContainer(document.BaseDocument):
            field_boolean = fields.BooleanField('b', null=True)

        model = FieldContainer()

        try:
            model.validate()
            self.assertTrue(True, 'Validation should succeed')
        except ValidationError:
            self.assertTrue(False, 'ValidationError should not have been thrown')

        model.field_boolean = None
        self.assertTrue(True, 'Validation should succeed')

    def test_non_nullable(self):
        class FieldContainer(document.BaseDocument):
            field_boolean = fields.BooleanField('b', null=False)

        model = FieldContainer()
        try:
            model.validate()
            self.assertTrue(False, 'Validation should have failed')
        except ValidationError:
            self.assertTrue(True, 'ValidationError should not have been thrown')

        model.field_boolean = True
        self.assertTrue(model.field_boolean)

        try:
            model.field_boolean = None
            self.assertTrue(False, 'ValidationError should have been thrown')
        except ValidationError:
            self.assertTrue(True, 'ValidationError was expected and caught')

    def test_nullable_jsonification(self):
        class FieldContainer(document.BaseDocument):
            field_boolean = fields.BooleanField('b', null=True)

        model = FieldContainer()
        json_data = model.to_json()
        self.assertIsInstance(json_data, dict)
        m2 = FieldContainer.from_json(json_data)

        self.assertIsNone(m2.field_boolean)

    def test_non_nullable_jsonification(self):
        class FieldContainer(document.BaseDocument):
            field_boolean = fields.BooleanField('b', null=False)

        model = FieldContainer()
        json_data = model.to_json()
        self.assertIsInstance(json_data, dict)
        m2 = FieldContainer.from_json(json_data)

        self.assertIsNone(m2.field_boolean)


if __name__ == '__main__':
    unittest.main()
