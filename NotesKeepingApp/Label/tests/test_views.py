from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse
import django
django.setup()
# Create your tests here.


class Data(APITestCase):
    def setUp(self):
        self.register_url = reverse("register")
        self.label_post_url = reverse("label")
        self.label_url = 'http://127.0.0.1:8000/label/1'

        self.valid_label_data = {'user': 1,
                                 'label_name': "note 1",
                                 }
        self.valid_label_put_data = {'user': 1,
                                     'label': "note 1",
                                     }
        self.invalid_label_data = {'user': 15,
                                   'label': "note 1",
                                   }
        self.valid_registration_data = {'first_name': "Gopinath",
                                        'last_name': "Das",
                                        'email': "iitiangokul@gmail.com",
                                        'user_name': "gopinathdas",
                                        'password': "bluelagoon"}


class NotesTest(Data):

    def test_given_valid_label_details(self):
        self.client.post(self.register_url, self.valid_registration_data, format='json')
        self.client.post(self.label_post_url, self.valid_label_data, format='json')

        response = self.client.get(self.label_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.put(self.label_url, self.valid_label_put_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = self.client.delete(self.label_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)

    def test_given_invalid_label_details(self):
        response = self.client.post(self.label_post_url, self.invalid_label_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        response = self.client.get(self.label_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        response = self.client.put(self.label_url, self.valid_label_put_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        response = self.client.delete(self.label_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)