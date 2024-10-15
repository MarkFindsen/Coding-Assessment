from django.test import TestCase
from django.core.exceptions import ValidationError

from ..models import Course, Intake
from datetime import date

class IntakeModelTestCase(TestCase):
    def setUp(self):
        self.valid_course = Course.objects.create(name="CSSE2310")
        self.valid_start_date = date(2024, 8, 12)
        self.valid_end_date = date(2024, 10, 1)

    def test_intake_default_output(self):
        intake = Intake.objects.create(
            start_date=self.valid_start_date,
            end_date=self.valid_end_date,
            course=self.valid_course
        )
        self.assertEqual(str(intake), "CSSE2310: 2024-08-12 to 2024-10-01")

    def test_intake_dates_valid(self):
        intake = Intake(
            start_date=date(2023, 1, 1),
            end_date=date(2023, 12, 31),
            course=self.valid_course
        )
        try:
            intake.full_clean()
        except ValidationError:
            self.fail("full_clean() raised ValidationError unexpectedly!")

    def test_intake_dates_invalid(self):
        invalid_end_date = date(2024, 8, 10)
        
        intake = Intake(
            start_date=self.valid_start_date,
            end_date=invalid_end_date,
            course=self.valid_course
        )
        with self.assertRaises(ValidationError):
            intake.full_clean()

    def test_intake_dates_equal(self):
        intake = Intake(
            start_date=self.valid_start_date,
            end_date=self.valid_start_date,
            course=self.valid_course
        )
        try:
            intake.full_clean()
        except ValidationError:
            self.fail("full_clean() raised ValidationError unexpectedly!")

    def test_intake_missing_dates(self):
        intake = Intake(course=self.valid_course)
        with self.assertRaises(ValidationError):
            intake.full_clean()

    def test_intake_missing_course(self):
        intake = Intake(
            start_date=date(2023, 1, 1),
            end_date=date(2023, 12, 31)
        )
        with self.assertRaises(ValidationError):
            intake.full_clean()

    def test_intake_cascade_delete(self):
        Intake.objects.create(
            start_date=self.valid_start_date,
            end_date=self.valid_end_date,
            course=self.valid_course
        )

        self.assertEqual(Intake.objects.count(), 1)
        self.valid_course.delete()
        self.assertEqual(Intake.objects.count(), 0)

    def test_intake_multiple_cascade_delete(self):
        valid_course_1 = Course.objects.create(name="DECO1800")
        valid_course_2 = Course.objects.create(name="CSSE2310")

        Intake.objects.create(
            start_date=self.valid_start_date,
            end_date=self.valid_end_date,
            course=valid_course_1
        )
        Intake.objects.create(
            start_date=self.valid_start_date,
            end_date=self.valid_end_date,
            course=valid_course_2
        )

        # There should be 2 intake objects
        self.assertEqual(Intake.objects.count(), 2)

        valid_course_1.delete()
        
        # Ensure the count is now 1 (the other intake should still exist)
        self.assertEqual(Intake.objects.count(), 1)

        # Ensure the remaining intake still exists by checking its course
        remaining_intake = Intake.objects.get(course_id=valid_course_2.pk)
        self.assertIsNotNone(remaining_intake)
        
        # Ensure that the intake related to the deleted course does not exist
        with self.assertRaises(Intake.DoesNotExist):
            Intake.objects.get(course_id=valid_course_1.pk)
