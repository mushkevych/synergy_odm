Synergy Object-Document Mapping
=========

Object Document Mapping for convenient python-to-json or json-to-python applications

Usage example:

    class SimpleContainer(BaseDocument):
        field_string = StringField('s')
        field_integer = IntegerField('i')
        field_boolean = BooleanField('b')
        field_datetime = DateTimeField('dt')
        field_decimal = DecimalField('d')
    
    class HostContainer(BaseDocument):
        nested_document = NestedDocumentField('nested', SimpleContainer)
        field_list = ListField('l_f')
        field_dict = DictField('l_d')

    ... somewhere in the code ...
        model = HostContainer()
        model.field_dict['aaa'] = 'bbb'
        model.field_list.append('ccc')
        model.nested_document.field_boolean = True
        model.nested_document.field_string = 'a short string description'
        model.nested_document.field_datetime = datetime.now()
        model.nested_document.field_decimal = 123.123
        model.nested_document.field_integer = 123
        
        json_document = model.to_json()
        m2 = HostContainer.from_json(json_document)

Inspired by:
[Magic Methods](http://www.rafekettler.com/magicmethods.html)
[Django ORM](https://docs.djangoproject.com/en/dev/topics/db/models/)
[Mongoengine](http://mongoengine.org/)


License:
---------
Modified BSD License. Refer to LICENSE for details.


Git repository:
---------
[GitHub project page](https://github.com/mushkevych/synergy_odm)


Metafile:
---------

    /tests/               folder contains unit test
    /odm/                 folder contains Object-Document Mapping modules


Wiki Links
---------
[Wiki Home Page](https://github.com/mushkevych/synergy_odm/wiki)


Os-Level Dependencies
---------
1. python 2.7+  
