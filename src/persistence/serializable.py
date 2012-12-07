from collections import namedtuple


class Serializable(object):

    ID_FIELDS = None
    FIELDS = None

    def get_id(self):

        return {name: self.__dict__[name] for name in self.__class__.ID_FIELDS}

    @classmethod
    def unserialize(cls, obj):

        print("class %s" % cls)
        print("object %s" % obj)
        new_obj = {f.name: f.unserialize_func(obj[f.name]) for f in cls.FIELDS}

        print(new_obj)
        return cls(**new_obj)

    def serialize(self):

        return {f.name: f.serialize_func(self, f.name) for f in self.FIELDS}

    @classmethod
    def list_unserialize(cls, obj):

        return [cls.unserialize(o) for o in obj]

    def list_serialize(self, name):

        values = self.__dict__[name]

        return [e.serialize() for e in values]

    @classmethod
    def direct_unserialize(cls, value):
        return value

    def direct_serialize(self, name):

        return self.__dict__[name]

    @classmethod
    def nested_unserialize(cls, value):

        return cls.unserialize(value)

    def nested_serialize(self, name):

        return self.__dict__[name].serialize()

    @classmethod
    def reference_unserialize(cls, reference):

        return cls.unserialize(cls.get_by_reference(reference))

    def reference_serialize(self, name):

        return self.__dict__[name].get_id()

    @classmethod
    def get_by_reference(cls, reference):

        raise Exception("This serializable is not referentiable")

    @classmethod
    def reference_list_unserialize(cls, list):

        return [cls.unserialize(cls.get_by_reference(r)) for r in list]

    def reference_list_serialize(self, name):

        return [r.get_id() for r in self.__dict__[name]]

    @classmethod
    def field(cls, name):

        return SerializableField(name, cls.direct_serialize,
                                 cls.direct_unserialize, None)

    @classmethod
    def nested(cls, name, type):

        return SerializableField(name, cls.nested_serialize,
                                 type.nested_unserialize, type)

    @classmethod
    def list(cls, name, type):

        return SerializableField(name, cls.list_serialize,
                                 type.list_unserialize, type)

    @classmethod
    def reference(cls, name, type):

        return SerializableField(name, cls.reference_serialize,
                                 type.reference_unserialize, type)

    @classmethod
    def reference_list(cls, name, type):

        return SerializableField(name, cls.reference_list_serialize,
                                 type.reference_list_unserialize, type)


SerializableField = namedtuple('SerializableField',
                               ['name',
                                'serialize_func',
                                'unserialize_func',
                                'field_class'])
