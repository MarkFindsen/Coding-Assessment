from django.test import TestCase

from ...admission.models import Course, Intake
from ..serializers import IntakeSerializer
from datetime import date

class IntakeSerializerTests(TestCase):
    def test_intake_serializer(self):
        course = Course.objects.create(name="CSSE2310")
        intake = Intake.objects.create(start_date=date(2024, 8, 12), end_date=date(2024, 10, 15), course=course)
        
        serializer = IntakeSerializer(instance=intake)
        
        expected_data = {
            'start_date': intake.start_date.isoformat(),
            'end_date': intake.end_date.isoformat(),
        }
        
        self.assertEqual(serializer.data, expected_data)
