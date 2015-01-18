__author__ = 'Bohdan Mushkevych'

import re
import time
import decimal
import datetime

from odm.errors import ValidationError


class BaseField(object):
    """A base class for fields in a Synergy ODM document. Instances of this class
    may be added to subclasses of `Document` to define a document's schema. """

    def __init__(self, field_name, required=False, default=None,
                 choices=None, verbose_name=None, null=False):
        """
        :param field_name: name of the field in the JSON document
        :param required: If the field is required.
            Whether it has to have a value or not. Defaults to False.
        :param default: (optional) The default value for this field if no value
            has been set (or if the value has been unset).  It can be a
            callable.
        :param choices: (optional) The valid choices
        :param verbose_name: (optional) The human readable, verbose name for the field.
        :param null: (optional) Is the field value can be null. If no and there is a default value
            then the default value is set
        """
        self.field_name = field_name
        self.required = required
        self.default = default
        self.choices = choices
        self.verbose_name = verbose_name
        self.null = null

    def __get__(self, instance, owner):
        """ Descriptor for retrieving a value from a field in a document. """
        if instance is None:
            # Document class being used rather than a document object
            return self

        # retrieve value from a BaseDocument instance if available
        return instance._data.get(self.field_name)

    def __set__(self, instance, value):
        """ Descriptor for assigning a value to a field in a document. """

        # If setting to None and there is a default
        # Then set the value to the default value
        if value is None:
            if self.null:
                value = None
            elif self.default is not None:
                value = self.default
                if callable(value):
                    value = value()

        instance._data[self.field_name] = value

    def raise_error(self, message='', errors=None, field_name=None):
        """Raises a ValidationError. """
        field_name = field_name if field_name else self.field_name
        raise ValidationError(message, errors=errors, field_name=field_name)

    def to_python(self, value):
        """Convert a JSON-variable to a Python type. """
        return value

    def to_json(self, value):
        """Convert a Python type to a JSON-friendly type. """
        return self.to_python(value)

    def validate(self, value):
        """Performs validation of the value.
        :param value: value to validate
        :raise ValidationError if the value is invalid"""

        # check choices
        if self.choices:
            if isinstance(self.choices[0], (list, tuple)):
                option_keys = [k for k, v in self.choices]
                if value not in option_keys:
                    msg = ('Value %s is not listed among valid choices %s' % (value, unicode(option_keys)))
                    self.raise_error(msg)
            elif value not in self.choices:
                msg = ('Value %s is not listed among valid choices %s' % (value, unicode(self.choices)))
                self.raise_error(msg)


class NestedDocumentField(BaseField):
    """ Field wraps a stand-alone Document """

    def __init__(self, field_name, nested_klass, **kwargs):
        """
        :param field_name: name of the field in the JSON document
        :param nested_klass: BaseDocument-derived class
        :param kwargs: standard set of arguments from the BaseField
        """
        self.nested_klass = nested_klass
        kwargs.setdefault('default', lambda: nested_klass())
        super(NestedDocumentField, self).__init__(field_name, **kwargs)

    def __get__(self, instance, owner):
        value = super(NestedDocumentField, self).__get__(instance, owner)
        if value is not None:
            return value
        else:
            super(NestedDocumentField, self).__set__(instance, None)
            return super(NestedDocumentField, self).__get__(instance, owner)

    def validate(self, value):
        """Make sure that value is of the right type """
        if not isinstance(value, self.nested_klass):
            self.raise_error('NestedClass is of the wrong type: %s vs expected %s'
                       % (value.__class__.__name__, self.nested_klass.__name__))
        super(NestedDocumentField, self).validate(value)


class ListField(BaseField):
    """ Field represents standard Python collection `list` """

    def __init__(self, field_name, **kwargs):
        kwargs.setdefault('default', lambda: [])
        super(ListField, self).__init__(field_name, **kwargs)

    def __get__(self, instance, owner):
        value = super(ListField, self).__get__(instance, owner)
        if value is not None:
            return value
        else:
            super(ListField, self).__set__(instance, None)
            return super(ListField, self).__get__(instance, owner)

    def validate(self, value):
        """Make sure that the inspected value is of type `list` or `tuple` """
        if not isinstance(value, (list, tuple)) or isinstance(value, basestring):
            self.raise_error('Only lists and tuples may be used in a list field')
        super(ListField, self).validate(value)


class DictField(BaseField):
    """A dictionary field that wraps a standard Python dictionary. This is
    similar to an embedded document, but the structure is not defined. """

    def __init__(self, field_name, **kwargs):
        kwargs.setdefault('default', lambda: {})
        super(DictField, self).__init__(field_name, **kwargs)

    def __get__(self, instance, owner):
        value = super(DictField, self).__get__(instance, owner)
        if value is not None:
            return value
        else:
            super(DictField, self).__set__(instance, None)
            return super(DictField, self).__get__(instance, owner)

    def validate(self, value):
        """Make sure that the inspected value is of type `dict` """
        if not isinstance(value, dict):
            self.raise_error('Only dictionaries may be used in a DictField')

        super(DictField, self).validate(value)


class StringField(BaseField):
    """A unicode string field. """

    def __init__(self, field_name, regex=None, max_length=None, min_length=None, **kwargs):
        self.regex = re.compile(regex) if regex else None
        self.max_length = max_length
        self.min_length = min_length
        super(StringField, self).__init__(field_name, **kwargs)

    def to_python(self, value):
        if isinstance(value, unicode):
            return value
        try:
            value = value.decode('utf-8')
        except:
            pass
        return value

    def validate(self, value):
        if not isinstance(value, basestring):
            self.raise_error('StringField only accepts string values')

        if self.max_length is not None and len(value) > self.max_length:
            self.raise_error('String value is too long')

        if self.min_length is not None and len(value) < self.min_length:
            self.raise_error('String value is too short')

        if self.regex is not None and self.regex.match(value) is None:
            self.raise_error('String value did not match validation regex')

        super(StringField, self).validate(value)


class IntegerField(BaseField):
    """ An integer field. """

    def __init__(self, field_name, min_value=None, max_value=None, **kwargs):
        self.min_value, self.max_value = min_value, max_value
        super(IntegerField, self).__init__(field_name, **kwargs)

    def to_python(self, value):
        try:
            value = int(value)
        except ValueError:
            pass
        return value

    def validate(self, value):
        try:
            value = int(value)
        except:
            self.raise_error('%s could not be converted to int' % value)

        if self.min_value is not None and value < self.min_value:
            self.raise_error('IntegerField value is too small')

        if self.max_value is not None and value > self.max_value:
            self.raise_error('IntegerField value is too large')

        super(IntegerField, self).validate(value)


class DecimalField(BaseField):
    """A fixed-point decimal number field. """

    def __init__(self, field_name, min_value=None, max_value=None, force_string=False,
                 precision=2, rounding=decimal.ROUND_HALF_UP, **kwargs):
        """
        :param min_value: Validation rule for the minimum acceptable value.
        :param max_value: Validation rule for the maximum acceptable value.
        :param force_string: Store as a string.
        :param precision: Number of decimal places to store.
        :param rounding: The rounding rule from the python decimal library:

            - decimal.ROUND_CEILING (towards Infinity)
            - decimal.ROUND_DOWN (towards zero)
            - decimal.ROUND_FLOOR (towards -Infinity)
            - decimal.ROUND_HALF_DOWN (to nearest with ties going towards zero)
            - decimal.ROUND_HALF_EVEN (to nearest with ties going to nearest even integer)
            - decimal.ROUND_HALF_UP (to nearest with ties going away from zero)
            - decimal.ROUND_UP (away from zero)
            - decimal.ROUND_05UP (away from zero if last digit after rounding towards zero would have been 0 or 5; otherwise towards zero)

            Defaults to: ``decimal.ROUND_HALF_UP``

        """
        self.min_value = min_value
        self.max_value = max_value
        self.force_string = force_string
        self.precision = precision
        self.rounding = rounding

        super(DecimalField, self).__init__(field_name, **kwargs)

    def to_python(self, value):
        if value is None:
            return value

        # Convert to string for python 2.6 before casting to Decimal
        try:
            value = decimal.Decimal("%s" % value)
        except decimal.InvalidOperation:
            return value
        return value.quantize(decimal.Decimal(".%s" % ("0" * self.precision)), rounding=self.rounding)

    def to_json(self, value, use_db_field=True):
        if value is None:
            return value
        if self.force_string:
            return unicode(value)
        return float(self.to_python(value))

    def validate(self, value):
        if not isinstance(value, decimal.Decimal):
            if not isinstance(value, basestring):
                value = unicode(value)
            try:
                value = decimal.Decimal(value)
            except Exception, exc:
                self.raise_error('Could not convert value to decimal: %s' % exc)

        if self.min_value is not None and value < self.min_value:
            self.raise_error('DecimalField value is too small')

        if self.max_value is not None and value > self.max_value:
            self.raise_error('DecimalField value is too large')

        super(DecimalField, self).validate(value)


class BooleanField(BaseField):
    """A boolean field type. """

    def to_python(self, value):
        try:
            value = bool(value)
        except ValueError:
            pass
        return value

    def validate(self, value):
        if not isinstance(value, bool):
            self.raise_error('BooleanField only accepts boolean values')


class DateTimeField(BaseField):
    """A datetime field.

    Uses the python-dateutil library if available alternatively use time.strptime
    to parse the dates.  Note: python-dateutil's parser is fully featured and when
    installed you can utilise it to convert varying types of date formats into valid
    python datetime objects.

    Note: Microseconds are rounded to the nearest millisecond.
      Pre UTC microsecond support is effectively broken.
      Use :class:`~mongoengine.fields.ComplexDateTimeField` if you
      need accurate microsecond support.
    """

    def validate(self, value):
        new_value = self.to_json(value)
        if not isinstance(new_value, (datetime.datetime, datetime.date)):
            self.raise_error(u'cannot parse date "%s"' % value)

    def to_json(self, value):
        if value is None:
            return value
        if isinstance(value, datetime.datetime):
            return value
        if isinstance(value, datetime.date):
            return datetime.datetime(value.year, value.month, value.day)
        if callable(value):
            return value()

        if not isinstance(value, (basestring, str, unicode)):
            return None

        # split usecs, because they are not recognized by strptime.
        if '.' in value:
            try:
                value, usecs = value.split('.')
                usecs = int(usecs)
            except ValueError:
                return None
        else:
            usecs = 0
        kwargs = {'microsecond': usecs}
        try:  # Seconds are optional, so try converting seconds first.
            return datetime.datetime(*time.strptime(value,
                                                    '%Y-%m-%d %H:%M:%S')[:6], **kwargs)
        except ValueError:
            try:  # Try without seconds.
                return datetime.datetime(*time.strptime(value,
                                                        '%Y-%m-%d %H:%M')[:5], **kwargs)
            except ValueError:  # Try without hour/minutes/seconds.
                try:
                    return datetime.datetime(*time.strptime(value,
                                                            '%Y-%m-%d')[:3], **kwargs)
                except ValueError:
                    return None


class ObjectIdField(BaseField):
    """A field wrapper around ObjectIds. """
    def to_python(self, value):
        if not isinstance(value, basestring):
            value = unicode(value)
        return value

    def to_json(self, value):
        if not isinstance(value, basestring):
            try:
                return unicode(value)
            except Exception, e:
                # e.message attribute has been deprecated since Python 2.6
                self.raise_error(message=unicode(e))
        return value

    def validate(self, value):
        try:
            unicode(value)
        except:
            self.raise_error('Invalid Object ID')
