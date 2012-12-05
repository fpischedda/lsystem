from persistence import mongo_connection
from persistence.serializable import Serializable


class MongoModel(Serializable):

    ID_FIELDS = ("__id")

    COLLECTION_NAME = ""

    def __init__(self):

        super(MongoModel, self).__init__()

    @classmethod
    def get_collection(cls):

        db = mongo_connection.get_default_db()
        return db[cls.COLLECTION_NAME]

    @classmethod
    def get_object_id(cls, obj):

        return {name: obj.getattr(name) for name in cls.ID_FIELDS}

    @classmethod
    def insert(cls, obj):

        collection = cls.get_collection()
        s = obj.serialize()
        collection.insert(s)

    def update(self, obj):

        collection = MongoModel.get_collection()
        s = self.serialize()
        id = MongoModel.get_object_id(obj)
        collection.update(id, s)

    @classmethod
    def get_by_id(cls, id):

        return cls.get_one_by(id)

    @classmethod
    def get_one_by(cls, fields):

        u = cls.collection.find_one(fields)

        if u is not None:
            return cls.unserialize(u)

        return None

    @classmethod
    def find_by(cls, opts):

        return None
