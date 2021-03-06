class FieldDoesNotExist(Exception):
    pass


class ValidationError(AssertionError):
    """ Validation exception. """

    def __init__(self, message='', **kwargs):
        self.errors = kwargs.get('errors', {})
        self.field_name = kwargs.get('field_name')
        self.message = message

    def __str__(self):
        return str(self.message)

    def __repr__(self):
        return '{0}({1},)'.format(self.__class__.__name__, self.message)

    def __getattribute__(self, name):
        message = super(ValidationError, self).__getattribute__(name)
        if name == 'message':
            if self.field_name:
                message = f'{self.field_name}: {message}'
            if self.errors:
                message = f'{message}({self._format_errors()})'
        return message
