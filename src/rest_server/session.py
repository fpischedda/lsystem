import datetime
from persistence.mongo_model import MongoModel


#class that define a session for a user
class Session(MongoModel):

    COLLECTION = 'sessions'

    FIELDS = (MongoModel.field('user_id'),
              MongoModel.field('ip'),
              MongoModel.field('device'),
              MongoModel.field('start_date'),
              MongoModel.field('close_date'),
              MongoModel.field('last_operation_date'))

    def __init__(self, user_id, ip, device, start_date=None,
                 last_operation_date=None,
                 close_date=None):

        self.user_id = user_id
        self.ip = ip
        self.device = device
        self.start_date = start_date or datetime.datetime.utcnow()
        self.close_date = close_date
        self.last_operation_date = last_operation_date or datetime.datetime.utcnow()

    def is_expired(self, max_inactive_seconds):
        """
        returns True if the session is expired if the last operation happened
        more than max_inactive_seconds seconds ago
        """
        now = datetime.datetime.utcnow()

        return self.last_operation_date - max_inactive_seconds < now

    @classmethod
    def get_by_user_id(cls, user_id):

        return cls.get_one_by({'user_id': user_id})

    def close(self):

        now = datetime.datetime.utcnow()
        self.update_fields_by({'close_date': now}, self.get_id())

    @classmethod
    def close_by_id(cls, id):

        now = datetime.datetime.utcnow()
        cls.update_fields_by({'close_date': now}, {'_id', id})
