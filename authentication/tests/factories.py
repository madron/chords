import factory
from django.contrib.auth import models


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.User

    username = factory.Sequence(lambda n: 'test%s' % n)
    # password: pass
    password = 'pbkdf2_sha256$12000$GMh486z94kmq$yaxEmZjcLvlnBoKWNG2Y926givWTo739b6tqWnw8eBM='
    is_staff = True
    is_superuser = True
    email = 'admin@example.com'
