import factory
from ..admission.models import Course, Intake

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
