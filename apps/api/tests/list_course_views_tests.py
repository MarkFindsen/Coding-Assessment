from rest_framework.test import APITestCase
from rest_framework.status import HTTP_200_OK, HTTP_401_UNAUTHORIZED, HTTP_405_METHOD_NOT_ALLOWED

from django.urls import reverse
from datetime import date

from django.contrib.auth import get_user_model
from ...admission.models import Course, Intake

User = get_user_model()

class ListCoursesTests(APITestCase):
    def setUp(self):
        self.url = reverse('api:list_courses')
        self.user = User.objects.create_user(username='mark', password='password')

        self.course_1 = Course.objects.create(name="CSSE2310")
        self.course_2 = Course.objects.create(name="DECO1800")

        self.intake_1 = Intake.objects.create(start_date=date(2024, 8, 12), end_date=date(2024, 10, 15), course=self.course_1)
        self.intake_2 = Intake.objects.create(start_date=date(2023, 2, 1), end_date=date(2024, 1, 1), course=self.course_1)
        self.intake_3 = Intake.objects.create(start_date=date(2024, 3, 5), end_date=date(2024, 7, 3), course=self.course_2)

    def test_get_unauthenticated_user(self):
        response = self.client.get(self.url, {})
        self.assertEqual(response.status_code, HTTP_401_UNAUTHORIZED)

    def test_get_authenticated(self):
        self.client.force_authenticate(user=self.user)
        
        response = self.client.get(self.url, {})
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_get_data(self):
        self.client.force_authenticate(user=self.user)
        
        response = self.client.get(self.url, {})
        
        self.assertEqual(len(response.data), 2)

        # Validate the first course and its intakes
        course_1 = response.data[0]
        self.assertEqual(course_1['name'], self.course_1.name)
        
        # Check that the intakes are serialized correctly
        intake_data = [intake['start_date'] for intake in course_1['intakes']]
        expected_intakes = [self.intake_1.start_date.isoformat(), self.intake_2.start_date.isoformat()]
        self.assertEqual(intake_data, expected_intakes)

        # Validate the second course and its intakes
        course_2 = response.data[1]
        self.assertEqual(course_2['name'], self.course_2.name)

        intake_data_2 = [intake['start_date'] for intake in course_2['intakes']]
        expected_intakes_2 = [self.intake_3.start_date.isoformat()]
        self.assertEqual(intake_data_2, expected_intakes_2)

    def test_post_unauthenticated_user(self):
        response = self.client.post(self.url, {})
        self.assertEqual(response.status_code, HTTP_401_UNAUTHORIZED)

    def test_post_not_allowed(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.post(self.url, {})
        self.assertEqual(response.status_code, HTTP_405_METHOD_NOT_ALLOWED)

    def test_put_unauthenticated_user(self):
        response = self.client.put(self.url, {})
        self.assertEqual(response.status_code, HTTP_401_UNAUTHORIZED)

    def test_put_not_allowed(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.put(self.url, {})
        self.assertEqual(response.status_code, HTTP_405_METHOD_NOT_ALLOWED)

    def test_patch_unauthenticated_user(self):
        response = self.client.patch(self.url, {})
        self.assertEqual(response.status_code, HTTP_401_UNAUTHORIZED)

    def test_patch_not_allowed(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.patch(self.url, {})
        self.assertEqual(response.status_code, HTTP_405_METHOD_NOT_ALLOWED)

    def test_delete_unauthenticated_user(self):
        response = self.client.delete(self.url, {})
        self.assertEqual(response.status_code, HTTP_401_UNAUTHORIZED)

    def test_delete_not_allowed(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.delete(self.url, {})
        self.assertEqual(response.status_code, HTTP_405_METHOD_NOT_ALLOWED)
