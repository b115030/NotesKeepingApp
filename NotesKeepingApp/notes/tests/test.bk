from django.test import TestCase
from decouple import config
# Create your tests here.
from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse


class Data(APITestCase):
    def setUp(self):
        self.register_url = reverse("register")#config('URL')+'register/'#'http://127.0.0.1:8000/register/'
        self.note_post_url = reverse("AddNote")#config('URL')+'create-note/'#'http://127.0.0.1:8000/note/'
        self.note_url = config('URL')+'note/1'#'http://127.0.0.1:8000/note/1'

        self.valid_note_data = {'user': 1,
                                'title': "test note ",
                                'description': "note 1",
                                'label': "note 1",
                                'color': '#AAAA36',
                                'collaborate': [1],
                                }
        self.valid_note_put_data = {'user': 1,
                                    'title': "test note 2",
                                    'description': "second note",
                                    'label': "note 1",
                                    'color': '#AAAA36',
                                    'collaborate': [1],
                                    }
        self.invalid_note_data = {'user': 1,
                                  'description': "note a note",
                                  'label': "note 1",
                                  'color': '#AAAA36',
                                  'collaborate': [1],
                                  }
        self.valid_registration_data = {'first_name': "Gopinath",
                                        'last_name': "Das",
                                        'email': "iitiangokul@gmail.com",
                                        'user_name': "gopinathdas",
                                        'password': "bluelagoon"}


class NotesTest(Data):

    def test_given_valid_note_url(self):
        self.client.post(self.register_url, self.valid_registration_data, format='json')
        self.client.post(self.note_post_url, self.valid_note_data, format='json')

        response = self.client.get(self.note_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        

        response = self.client.put(self.note_url, self.valid_note_put_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = self.client.delete(self.note_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)

    def test_given_invalid_note_details_for_crud(self):
        response = self.client.post(self.note_post_url, self.invalid_note_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        response = self.client.get(self.note_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        response = self.client.put(self.note_url, self.valid_note_put_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        response = self.client.delete(self.note_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)