import time
import uuid
from persistence.mongo_model import MongoModel


#class that define a session for a user
class Session(MongoModel):

    ID_FIELDS = ('id', )

    COLLECTION = 'sessions'

    FIELDS = (MongoModel.field('id'),
              MongoModel.field('user_id'),
              MongoModel.field('ip'),
              MongoModel.field('device'),
              MongoModel.field('start_date'),
              MongoModel.field('close_date'),
              MongoModel.field('last_operation_date'))

    def __init__(self, user_id, ip, device, start_date=None,
                 last_operation_date=None,
                 close_date=None):

        self.id = uuid.uuid4().hex
        self.user_id = user_id
        self.ip = ip
        self.device = device
        self.start_date = start_date or time.time
        self.close_date = close_date
        self.last_operation_date = last_operation_date or time.time

    def is_expired(self, max_inactive_seconds):
        """
        returns True if the session is expired if the last operation happened
        more than max_inactive_seconds seconds ago
        """
        return self.last_operation_date - max_inactive_seconds < time.time

    @classmethod
    def get_by_id(cls, id):

        return cls.get_by({'id': id})

    @classmethod
    def get_by_user_id(cls, user_id):

        return cls.get_by({'user_id': user_id})

    @classmethod
    def close_by_id(cls, id):

        cls.update_fields({'close_date': time.time}, {'id', id})
