__author__ = 'Bohdan Mushkevych'

from odm.errors import FieldDoesNotExist
from odm.fields import NestedDocumentField, BaseField
from odm.pyversion import PY3, txt_type


class BaseDocument(object):
    def __init__(self, **values):
        """ Initialize a document or embedded document """
        self._fields = self._get_fields()

        self._data = dict()
        for var in values.keys():
            if var not in self._fields.keys():
                msg = "The field '{0}' does not exist on the document '{1}'".format(var, self.__class__.__name__)
                raise FieldDoesNotExist(msg)

    def __delattr__(self, name):
        """Handle deletions of fields"""
        if name in self._fields:
            default = self._fields[name].default
            if callable(default):
                default = default()
            setattr(self, name, default)
        else:
            super(BaseDocument, self).__delattr__(name)

    def __setattr__(self, name, value):
        super(BaseDocument, self).__setattr__(name, value)

    def __iter__(self):
        return iter(self._fields)

    def __getitem__(self, name):
        """ Dictionary-style field getter.
        :param name: field_name of the field (not the name of the variable)
        :return: field value if present
        :raise KeyError if the given name is not among known field_names
        """
        if name not in self._fields:
            raise KeyError(name)
        field_obj = self._fields[name]
        return field_obj.__get__(self, self.__class__)

    def __setitem__(self, name, value):
        """ Dictionary-style field setter.
        :param name: field_name of the field (not the name of the variable)
        :param value: value to set
        :raise KeyError if the given name is not among known field_names
        """
        if name not in self._fields:
            raise KeyError(name)
        field_obj = self._fields[name]
        return field_obj.__set__(self, value)

    def __delitem__(self, name):
        """ Dictionary-style field deleter.
        :param name: field_name of the field (not the name of the variable)
        :raise KeyError if the given name is not among known field_names
        """
        if name not in self._fields:
            raise KeyError(name)
        field_obj = self._fields[name]
        return field_obj.__delete__(self)

    def __contains__(self, name):
        """
        :param name: field_name of the field (not the name of the variable)
        :return: True if the field is set, False if the field is None or not known
        """
        try:
            val = self.__getitem__(name)
            return val is not None
        except (KeyError, AttributeError):
            return False

    def __len__(self):
        return len(self._data)

    def __repr__(self):
        try:
            u = self.__str__()
        except (UnicodeEncodeError, UnicodeDecodeError):
            u = '[Bad Unicode data]'
        repr_type = str if u is None else type(u)
        return repr_type('<%s: %s>' % (self.__class__.__name__, u))

    def __str__(self):
        if hasattr(self, '__unicode__'):
            if PY3:
                return self.__unicode__()
            else:
                return unicode(self).encode('utf-8')
        return txt_type('%s object' % self.__class__.__name__)

    def __eq__(self, other):
        if self is other:
            return True

        if isinstance(other, self.__class__):
            try:
                return self.key == other.key
            except NotImplementedError:
                pass

        return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash(self.key)

    @property
    def key(self):
        raise NotImplementedError('property key.getter is not implemented in BaseDocument child %s'
                                  % self.__class__.__name__)

    @key.setter
    def key(self, value):
        raise NotImplementedError('property key.getter is not implemented in BaseDocument child %s'
                                  % self.__class__.__name__)

    @property
    def document(self):
        return self.to_json()

    def validate(self):
        """Ensure that all fields' values are valid and that required fields are present. """
        for field_name, field_obj in self._fields.iteritems():
            value = field_obj.get(field_name, None)

            if value is None and field_obj.null is False:
                # raise ValidationError
                pass

            if value is None and field_obj.required is True:
                # raise ValidationError
                pass

            if isinstance(field_obj, NestedDocumentField):
                nested_document = field_obj.__get__(self, self.__class__)
                nested_document.validate()
            else:
                field_obj.validate(value)

    def to_json(self):
        """Converts given document to JSON dict. """
        json_data = dict()

        for field_name, field_obj in self._fields.iteritems():
            if isinstance(field_obj, NestedDocumentField):
                nested_document = field_obj.__get__(self, self.__class__)
                value = nested_document.to_json()
            elif isinstance(field_obj, BaseField):
                value = field_obj.__get__(self, self.__class__)
            else:
                # ignore fields not derived from BaseField or NestedDocument
                continue

            if value is None:
                continue

            json_data[field_name] = value

        return json_data

    @classmethod
    def _get_fields(cls):
        _fields = dict()
        for field_name in dir(cls):
            field_obj = getattr(cls, field_name)
            if isinstance(field_obj, BaseField):
                _fields[field_obj.field_name] = field_obj
            else:
                continue

        return _fields

    @classmethod
    def from_json(cls, json_data):
        """ Converts json data to a new document instance"""
        new_instance = cls()
        for field_name, field_obj in cls._get_fields().iteritems():
            if isinstance(field_obj, NestedDocumentField):
                if field_name in json_data:
                    nested_field = field_obj.__get__(new_instance, new_instance.__class__)
                    nested_document = nested_field.from_json(json_data[field_name])
                    field_obj.__set__(new_instance, nested_document)
            elif isinstance(field_obj, BaseField):
                if field_name in json_data:
                    field_obj.__set__(new_instance, json_data[field_name])
            else:
                continue

        return new_instance
