import factory
from factory import fuzzy
from factory.django import DjangoModelFactory

from .models import User


class UserFactory(DjangoModelFactory):
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    email = factory.Sequence(lambda n: f"{n}@xyz.com")

    class Meta:
        model = User
        skip_postgeneration_save = True

    @factory.post_generation
    def password(obj, create, password, **_):
        if not create:
            return
        password_text = password or fuzzy.FuzzyText(length=15).fuzz()
        obj.set_password(password_text)
        obj.password_text = password_text
        obj.save()
