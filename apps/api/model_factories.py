import factory
from ..admission.models import Course, Intake
from django.contrib.auth import get_user_model

class CourseFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Course
    
    name = factory.Faker('name')

class IntakeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Intake
    
    start_date = factory.Faker('date')
    end_date = factory.Faker('date')
    course = factory.SubFactory(CourseFactory)

class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = get_user_model()

    username = factory.Faker('user_name')
    password = factory.Faker('password')
