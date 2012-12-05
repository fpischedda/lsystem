from collections import namedtuple


class Serializable(object):

    FIELDS = None

    @classmethod
    def unserialize(cls, obj):
        return cls(**obj)

    def serialize(self):

        return {f.name: f.func(self, f.name) for f in self.FIELDS}

    def direct_field(self, name):

        return self.__dict__[name]

    def serialize_field(self, name):

        return self.__dict__[name].serialize()

    def serialize_list(self, name):

        values = self.direct_field(name)

        return [e.serialize() for e in values]

    @classmethod
    def declare_field(cls, name, func=None):

        f = func or cls.direct_field

        return SerializableField(name, f)

SerializableField = namedtuple('SerializableField', ['name', 'func'])
