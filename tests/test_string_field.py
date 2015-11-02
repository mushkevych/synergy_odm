# -*- coding: utf-8 -*-
__author__ = 'Bohdan Mushkevych'

import unittest

from odm import document, fields


class TestDocument(unittest.TestCase):
    def test_valid_formats(self):
        class FieldContainer(document.BaseDocument):
            field_string = fields.StringField('s', null=False)

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

if __name__ == '__main__':
    unittest.main()
