from django.test import TestCase
from datetime import date

from ...admission.models import Course, Intake
from ..serializers import CourseSerializer

class CourseSerializerTests(TestCase):
    def setUp(self):
        self.course = Course.objects.create(name="CSSE2310")

        self.intake_1 = Intake.objects.create(start_date=date(2024, 8, 12), end_date=date(2024, 10, 15), course=self.course)
        self.intake_2 = Intake.objects.create(start_date=date(2023, 2, 1), end_date=date(2024, 1, 1), course=self.course)

    def test_course_serializer_empty_intakes(self):
        course_no_intakes = Course.objects.create(name="DECO1800")
        serializer = CourseSerializer(instance=course_no_intakes)
        
        expected_data = {
            'name': course_no_intakes.name,
            'intakes': []  # No intakes should result in an empty list
        }
        
        self.assertEqual(serializer.data, expected_data)
    
    def test_course_serializer_with_intakes(self):
        serializer = CourseSerializer(instance=self.course)
        
        expected_data = {
            'name': self.course.name,
            'intakes': [
                {'start_date': self.intake_1.start_date.isoformat(), 'end_date': self.intake_1.end_date.isoformat()},
                {'start_date': self.intake_2.start_date.isoformat(), 'end_date': self.intake_2.end_date.isoformat()},
            ]
        }
        
        self.assertEqual(serializer.data, expected_data)
