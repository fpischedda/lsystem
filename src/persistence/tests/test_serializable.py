from persistence.serializable import Serializable


class Field(Serializable):

    ID_FIELDS = ('id_field', )
    FIELDS = (Serializable.field('id_field'), )

    def __init__(self, id_field):

        self.id_field = id_field


class ReferencedField(Serializable):

    ID_FIELD = 'id_field'
    FIELDS = (Serializable.field('some_field'), )

    def __init__(self, some_field):

        self.some_field = some_field

    @classmethod
    def get_by_reference(cls, id):

        return cls.unserialize({'id_field': id['id_field'],
                                'some_field': 'some value'})


class Nested(Serializable):

    FIELDS = (Serializable.nested('nested', Field), )

    def __init__(self, nested):

        self.nested = nested


class List(Serializable):

    FIELDS = (Serializable.list('a_list', Field), )

    def __init__(self, a_list):

        self.a_list = a_list


class Reference(Serializable):

    FIELDS = (Serializable.reference('referenced', ReferencedField), )

    def __init__(self, referenced):

        self.referenced = referenced


class ReferenceList(Serializable):

    FIELDS = (Serializable.reference_list('list_of_referenced', ReferencedField), )

    def __init__(self, list_of_referenced):

        self.list_of_referenced = list_of_referenced


def test_field_serialization():
    """test serialization of a class with a simple field"""
    f = Field('simple')

    s = f.serialize()

    assert s == {'id_field': 'simple'}


def test_field_unserialization():
    """test unserialization of a class with a simple field"""

    s = {'id_field': 'simple'}
    obj = Field.unserialize(s)

    assert obj.id_field == 'simple'


def test_nested_serialization():
    """test serialization of a class with a nested field"""

    f = Field('nested')
    s = Nested(f).serialize()

    assert s['nested'] == {'id_field': 'nested'}


def test_nested_unserialization():
    """test unserialization of a class with a nested field"""

    s = {'nested': {'id_field': 'nested'}}
    obj = Nested.unserialize(s)

    assert obj.nested.id_field == 'nested'


def test_list_serialization():
    """test serialization of a class with a list field"""

    f1 = Field('nested_in_list1')
    f2 = Field('nested_in_list2')
    s = List([f1, f2]).serialize()

    assert s['a_list'] == [{'id_field': 'nested_in_list1'},
                           {'id_field': 'nested_in_list2'}]


def test_list_unserialization():
    """test unserialization of a class with a list field"""

    s = {'a_list': [{'id_field': 'nested_in_list1'},
                    {'id_field': 'nested_in_list2'}]}

    obj = List.unserialize(s)

    assert obj.a_list[0].id_field == 'nested_in_list1' and obj.a_list[1].id_field == 'nested_in_list2'


def test_reference_serialization():
    """test serialization of a class with a reference field"""

    f = ReferencedField('some value')
    f.set_id('some id')
    s = Reference(f).serialize()

    print(s)
    assert s == {'referenced': {'id_field': 'some id'}}


def test_reference_unserialization():
    """test unserialization of a class with a reference field"""
    s = {'referenced': {'id_field': 'some id'}}
    r = Reference.unserialize(s)

    assert r.referenced.some_field == 'some value'


def test_reference_list_serialization():
    """test serialization of a class with a list of reference fields"""

    r1 = ReferencedField('value1')
    r1.set_id('referenced_in_list1')
    r2 = ReferencedField('value2')
    r2.set_id('referenced_in_list2')
    s = ReferenceList([r1, r2]).serialize()

    assert s['list_of_referenced'] == [{'id_field': 'referenced_in_list1'},
                                       {'id_field': 'referenced_in_list2'}]


def test_reference_list_unserialization():
    """test unserialization of a class with a list of referenced fields"""

    s = {'list_of_referenced': [{'id_field': 'referenced_in_list1'},
                                {'id_field': 'referenced_in_list2'}]}

    r = ReferenceList.unserialize(s)
    assert r.list_of_referenced[0].some_field == 'some value'
