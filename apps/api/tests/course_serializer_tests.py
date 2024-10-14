from django.test import TestCase

from ..serializers import CourseSerializer

class CourseSerializerTests(TestCase):
    def test_dummy(self):
        self.assertEqual(1 + 1, 2)
