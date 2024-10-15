from rest_framework.test import APITestCase
from rest_framework.status import HTTP_200_OK, HTTP_401_UNAUTHORIZED, HTTP_405_METHOD_NOT_ALLOWED

from django.urls import reverse
from datetime import date

from django.contrib.auth import get_user_model
from ..model_factories import CourseFactory, IntakeFactory, UserFactory

User = get_user_model()

class ListCoursesTests(APITestCase):
    def setUp(self):
        self.url = reverse('api:list_courses')
        self.user = UserFactory()

        self.course_1 = CourseFactory(name="CSSE2310")
        self.course_2 = CourseFactory(name="DECO1800")

        self.intake_1 = IntakeFactory(start_date='2024-08-12', end_date='2024-10-15', course=self.course_1)
        self.intake_2 = IntakeFactory(start_date='2023-02-01', end_date='2024-01-01', course=self.course_1)
        self.intake_3 = IntakeFactory(start_date='2024-03-05', end_date='2024-07-03', course=self.course_2)

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
        expected_intakes = [self.intake_1.start_date, self.intake_2.start_date]
        self.assertEqual(intake_data, expected_intakes)

        # Validate the second course and its intakes
        course_2 = response.data[1]
        self.assertEqual(course_2['name'], self.course_2.name)

        intake_data_2 = [intake['start_date'] for intake in course_2['intakes']]
        expected_intakes_2 = [self.intake_3.start_date]
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
