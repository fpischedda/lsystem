from collections import namedtuple


class Serializable(object):

    ID_FIELD = None
    FIELDS = None

    def get_id(self):

        try:
            return {self.ID_FIELD: self.__dict__[self.ID_FIELD]}
        except KeyError:

            return None

    def set_id(self, id):

        self.__dict__[self.ID_FIELD] = id

    def get_id_value(self):

        try:
            return self.__dict__[self.ID_FIELD]
        except KeyError:

            return None

    @classmethod
    def unserialize(cls, obj):

        new_obj = {f.name: f.unserialize_func(obj[f.name]) for f in cls.FIELDS}

        return cls(**new_obj)

    def serialize(self):

        obj = {f.name: f.serialize_func(self, f.name) for f in self.FIELDS}
        if self.ID_FIELD not in self.FIELDS:

            id = self.get_id_value()
            if id is not None:
                obj[self.ID_FIELD] = self.get_id_value()

        return obj

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

        return cls.get_by_reference(reference)

    def reference_serialize(self, name):

        return self.__dict__[name].get_id()

    @classmethod
    def get_by_reference(cls, reference):

        raise Exception("This serializable is not referentiable")

    @classmethod
    def exists_by_reference(cls, reference):

        raise Exception("This serializable is not referentialbe")

    @classmethod
    def reference_list_unserialize(cls, list):

        return [cls.get_by_reference(r) for r in list]

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
