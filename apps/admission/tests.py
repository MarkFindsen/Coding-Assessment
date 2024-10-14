from django.test import TestCase
from django.core.exceptions import ValidationError

class CourseModelTestCase(TestCase):
    def setUp(self):
        self.valid_name = "CSSE2310"

    def test_course_requires_name(self):
        with self.assertRaises(ValidationError):
            course = Course()
            course.full_clean()

        course = Course(name=self.valid_name)
        try:
            course.full_clean()
        except ValidationError:
            self.fail("full_clean() raised ValidationError unexpectedly!")

    def test_course_default_output(self):
        course = Course.objects.create(name=self.valid_name)
        self.assertEqual(str(course), self.valid_name)

    def test_course_name_max_length(self):
        max_length = Course._meta.get_field('name').max_length
        self.assertEqual(max_length, 50)
