from persistence.mongo_model import MongoModel


class ModelWithAutoId(MongoModel):

    COLLECTION = 'tests'
    FIELDS = (MongoModel.field('some_field'), )

    def __init__(self, some_field, *kwds):

        self.some_field = some_field
        super(ModelWithAutoId, self).__init__(*kwds)


def test_model_with_auto_id_field():

    m = ModelWithAutoId('a value')

    id = m.save()

    assert m.get_id() == id

    m.some_field = 'another value'

    id = m.save()

    assert id is not None

    mm = ModelWithAutoId.get_one_by(id)

    assert m.some_field == mm.some_field
