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
            'no': False,
            0: False,
            '0': False,
            'False': False,
            'false': False,
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
                self.assertEqual(model.field_boolean, value)

                model.validate()
                self.assertTrue(False, 'ValidationError should have been thrown for value {0}'
                                .format(value))
            except ValidationError:
                self.assertTrue(True, 'ValidationError was not expected but caught for value {0}'
                                .format(value))
            except ValueError:
                self.assertTrue(False, 'ValueError was not expected but caught for value {0}'
                                .format(value))


if __name__ == '__main__':
    unittest.main()
