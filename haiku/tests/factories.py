import factory
from django.contrib.auth import get_user_model


class UserFactory(factory.DjangoModelFactory):
    # This class was adapted from edx-platform/common/djangoapps/student/tests/factories.py.
    class Meta:
        model = get_user_model()
        django_get_or_create = ['username', 'email']

    username = factory.Sequence(u'robot{0}'.format)
    email = factory.Sequence(u'robot+test+{0}@edx.org'.format)
    password = factory.PostGenerationMethodCall('set_password', 'test')
    first_name = factory.Sequence(u'Robot{0}'.format)
    last_name = 'Test'
    is_staff = False
    is_active = True
    is_superuser = False
