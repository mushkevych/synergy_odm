__author__ = 'Bohdan Mushkevych'

import time
import unittest
import datetime

from odm.errors import ValidationError
from odm.pyversion import str_types
from odm import document, fields


class TestDocument(unittest.TestCase):
    def test_date_formats(self):
        class FieldContainer(document.BaseDocument):
            field_datetime = fields.DateTimeField('dt', null=False)

        utc_timestamp = time.time()
        dt_valid = datetime.datetime(year=2015, month=1, day=1, hour=23, minute=59, second=59)
        dt_valid_timestamp = int(dt_valid.strftime('%s'))
        dt_date_valid = datetime.date(year=2015, month=1, day=1)
        valid_formats = {
            '2015-01-01 23:59:59': dt_valid,
            dt_date_valid: dt_date_valid,
            dt_valid: dt_valid,
            dt_valid_timestamp: datetime.datetime.utcfromtimestamp(dt_valid_timestamp),
            utc_timestamp: datetime.datetime.utcfromtimestamp(utc_timestamp)
        }

        model = FieldContainer()
        for key, value in valid_formats.items():
            try:
                model.field_datetime = key
                self.assertEqual(model.field_datetime, value)

                model.validate()
                self.assertTrue(True, 'ValidationError should not have been thrown')
            except ValidationError:
                self.assertTrue(False, 'ValidationError was not expected but caught')
            except ValueError:
                self.assertTrue(False, 'ValueError was not expected but caught')

    def test_jsonification(self):
        class FieldContainer(document.BaseDocument):
            field_datetime = fields.DateTimeField('dt', null=False)

        dt_valid = datetime.datetime(year=2015, month=1, day=1, hour=23, minute=59, second=59)
        model = FieldContainer(field_datetime=dt_valid)

        json_data = model.to_json()
        self.assertIsInstance(json_data, dict)
        self.assertIsInstance(json_data['dt'], str_types)
        m2 = FieldContainer.from_json(json_data)
        self.assertEqual(model.field_datetime, m2.field_datetime)

        json_data['dt'] = dt_valid
        self.assertIsInstance(json_data['dt'], datetime.datetime)
        m3 = FieldContainer.from_json(json_data)
        self.assertEqual(model.field_datetime, m3.field_datetime)


if __name__ == '__main__':
    unittest.main()
