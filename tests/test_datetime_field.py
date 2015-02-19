__author__ = 'Bohdan Mushkevych'

import unittest
import datetime

from odm.errors import ValidationError
from odm import document, fields


class TestDocument(unittest.TestCase):
    def test_datetime_fields(self):
        class FieldContainer(document.BaseDocument):
            field_datetime = fields.DateTimeField('dt', null=False)

        dt_valid = datetime.datetime(year=2015, month=01, day=01, hour=23, minute=59, second=59)
        dt_date_valid = datetime.date(year=2015, month=01, day=01)
        valid_formats = {
            '2015-01-01 23:59:59': dt_valid,
            dt_date_valid: dt_date_valid,
            dt_valid: dt_valid,
            int(dt_valid.strftime('%s')): dt_valid
        }

        model = FieldContainer()
        for key, value in valid_formats.iteritems():
            try:
                model.field_datetime = key
                self.assertEqual(model.field_datetime, value)

                model.validate()
                self.assertTrue(True, 'ValidationError should not have been thrown')
            except ValidationError:
                self.assertTrue(False, 'ValidationError was not expected but caught')
            except ValueError:
                self.assertTrue(False, 'ValueError was not expected but caught')


if __name__ == '__main__':
    unittest.main()
