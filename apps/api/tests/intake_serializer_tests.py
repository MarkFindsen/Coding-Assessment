from django.test import TestCase

from ..model_factories import CourseFactory, IntakeFactory
from ..serializers import IntakeSerializer
from datetime import date

class IntakeSerializerTests(TestCase):
    def test_intake_serializer(self):
        course = CourseFactory(name="CSSE2310")
        intake = IntakeFactory(start_date=date(2024, 8, 12), end_date=date(2024, 10, 15), course=course)

        serializer = IntakeSerializer(instance=intake)
        
        expected_data = {
            'start_date': intake.start_date.isoformat(),
            'end_date': intake.end_date.isoformat(),
        }
        
        self.assertEqual(serializer.data, expected_data)
