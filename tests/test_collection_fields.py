__author__ = 'Bohdan Mushkevych'

import unittest

from odm import document, fields


class EmbeddedCollections(document.BaseDocument):
    field_list = fields.ListField('s')
    field_dict = fields.DictField('i')
    field_id = fields.ObjectIdField(field_name='_id', null=True)


class TestDocument(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.model = EmbeddedCollections()

    def tearDown(self):
        del self.model

    def test_getter_setter(self):
        test_dict = dict()
        for i in range(1, 100):
            self.model.field_dict[i] = i * 100
            test_dict[i] = i * 100

        for i in range(1, 100):
            self.model.field_list.append(i)

        self.assertItemsEqual(self.model.field_list, range(1, 100))
        self.assertDictEqual(self.model.field_dict, test_dict)

    def test_jsonification(self):
        test_dict = dict()
        for i in range(1, 100):
            self.model.field_dict[i] = i * 100
            test_dict[i] = i * 100

        for i in range(1, 100):
            self.model.field_list.append(i)

        json_data = self.model.to_json()
        self.assertIsInstance(json_data, dict)
        m2 = EmbeddedCollections.from_json(json_data)

        self.assertItemsEqual(m2.field_list, range(1, 100))
        self.assertDictEqual(m2.field_dict, test_dict)


if __name__ == '__main__':
    unittest.main()
