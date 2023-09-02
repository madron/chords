import factory
from .. import models


class SongFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Song

    title = factory.Sequence(lambda n: 'title{}'.format(n))
