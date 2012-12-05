from persistence.mongo_model import MongoModel
from core.item import Item


class ItemModel(Item, MongoModel):

    COLLECTION_NAME = "items"

    FIELDS = (MongoModel.declare_field('name'),
              MongoModel.declare_field('quantity'),
              MongoModel.declare_field('usable'),
              MongoModel.declare_field('user_id'))

    def __init__(self, name, quantity, usable, user_id, **kwds):

        super(ItemModel, self).__init__(name, quantity, usable, user_id, **kwds)

    @classmethod
    def get_by_user_id(cls, user_id):

        return cls.get_one_by({'user_id': user_id})
