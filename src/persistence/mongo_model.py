from persistence import mongo_connection
from persistence.serializable import Serializable


class MongoModel(Serializable):

    ID_FIELD = "_id"

    COLLECTION = ""

    def __init__(self):

        super(MongoModel, self).__init__()

    @classmethod
    def get_collection(cls):

        db = mongo_connection.get_default_db()
        return db[cls.COLLECTION]

    @classmethod
    def get_object_id(cls, obj):

        return {cls.ID_FIELD: obj.getitem[cls.ID_FIELD]}

    @classmethod
    def unserialize(cls, obj):

        res = super(MongoModel, cls).unserialize(obj)

        res.set_id(obj[cls.ID_FIELD])

        return res

    def save(self):

        prev_id = self.get_id_value()
        s = self.serialize()
        id = self.get_collection().save(s, manipulate=True)

        if prev_id is None:
            self.set_id(id)

        return self.get_id()

    def insert(self):

        collection = self.get_collection()
        s = self.serialize()
        return collection.insert(s)

    def update(self):

        collection = self.get_collection()
        s = self.serialize()
        collection.update(s, self.get_id())
        return self.get_id()

    @classmethod
    def get_by_id(cls, reference):

        ref = {cls.ID_FIELD: reference}
        return cls.get_one_by(ref)

    @classmethod
    def get_by_reference(cls, reference):

        return cls.get_one_by(reference)

    @classmethod
    def get_one_by(cls, fields):

        collection = cls.get_collection()
        o = collection.find_one(fields)

        if o is not None:
            return cls.unserialize(o)

        return None

    @classmethod
    def all(cls):

        res = cls.get_collection().find()

        objs = [cls.unserialize(o) for o in res if o is not None]

        return objs

    @classmethod
    def find_by(cls, opts):

        res = cls.get_collection().find(opts)

        objs = [cls.unserialize(o) for o in res]

        return objs
