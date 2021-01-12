from django.test import TestCase
from decouple import config
# Create your tests here.
from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
import json
import django
django.setup()

User = get_user_model()

class Data(APITestCase):
    def setUp(self):
        self.register_url = reverse("register")#config('URL')+'register/'#'http://127.0.0.1:8000/register/'
        self.note_post_url = reverse("notes:AddNote")#config('URL')+'create-note/'#'http://127.0.0.1:8000/note/'
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
        #Then login through user
        self.login_url = reverse('login')
        self.getall = reverse('AllNotes')
        self.login_data = {"email":"iiitiangokul@gmail.com", "password":"bluelagoon"}

        #Then add notes as user
        self.note1 = {"title":"title", "description":"descrpiton"}
        self.note2 = {"title":"title2", "description":"description2"}
        """
        this method setup all the url and data which was required by all test cases
        """
        self.register_url = reverse("register")
        self.login_url = reverse("login")
        self.label_post_url = reverse("label")
        self.label_url = reverse("specific-label", kwargs={'pk': 1})
        self.note_post_url = reverse("notes:AddNote")
        self.note_url = reverse("notes:UpdateNote", kwargs={'pk': 1})
        self.note_archived_url = reverse("notes:Archive")
        self.note_pinned_url = reverse("notes:Pinned")
        self.note_trash_url = reverse("notes:Trash")
        self.note_search_url = reverse("notes:AddNote")+"?search_term="+ "valid"

        self.invalid_registration_data = {'first_name': "abc",
                                            'last_name': "def",
                                            'email': "abc123@gmail.com",
                                            'user_name': "abcdef"}
        self.valid_login_data = {
            'email': "iiitiangokul@gmail.com",
            'password': "bluelagoon"}
        self.invalid_login_data = {
            'email': "123@gmail.com",
            'password': "abcdef"}

        self.valid_label_data = {
            'name': "label note",
        }

        self.valid_label_put_data = {'name': "Test Note",
                                        }
        self.invalid_label_data = {'labelname': "wrong note",
                                    }

        self.valid_note_put_data = {
            "title": "randomnote",
            "description": "random description",
            'is_archived': True,
            'is_pinned': True,
            'labels': ["label note"],
            'collaborators': ["iiitiangokul@gmail.com"]
        }
        self.invalid_note_data = {
            'title': "note title",
            'description': "this is my description",
            'labels': "Qwerty Note",
            'collaborators': ["abc123@gmail.com"]
        }

        self.valid_note_data = {
            "title": "valid note",
            "description": "this is my test note",
            'is_archived': True,
            'is_pinned': True,
            'labels': ["label note"],
            "collaborators": ["iiitiangokul@gmail.com"]
        }
        self.valid_note_data2 = {
            "title": "valid note 2",
            "description": "this is my 2nd test note",
            "is_trashed": True,
            "labels": ["label note"],
            "collaborators": ["iiitiangokul@gmail.com"]
        }



class NotesTest(Data):

    def test_given_valid_note_url(self):
        self.client.post(self.register_url, self.valid_registration_data, format='json')
        self.client.post(self.note_post_url, self.valid_note_data, format='json')
        response = self.client.get(self.note_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_given_valid_note(self):
        response = self.client.put(self.note_url, self.valid_note_put_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    def test_given_valid_note_url_(self):
        response = self.client.delete(self.note_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)

    def test_given_invalid_note_(self):
        response = self.client.post(self.note_post_url, self.invalid_note_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_given_invalid_note_details_for_crud(self):
        response = self.client.delete(self.note_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_view_get_all_notes(self):
        response = self.client.post(self.login_url, self.login_data, format = 'json')
        token = json.loads(response._container[0]).get('request_id')
        get_all = reverse('notes:GetAllNote')
        response = self.client.get(get_all, HTTP_TOKEN=token)
        self.client.post(self.note_post_url, self.note1, format="json", HTTP_TOKEN = token)
        self.client.post(self.note_post_url, self.note2, format="json", HTTP_TOKEN = token)
        assert response.status_code == status.HTTP_200_OK

    # def test_delete_note(self):



    def test_search_notes(self):
        
        search_word = "?search_for=t"
        search_url = reverse("notes:NoteSearch")+str(search_word)
        response = self.client.get(search_url, HTTP_TOKEN = token)
        assert response.status_code == status.HTTP_200_OK
class LabelTest(Data):

    def test_given_valid_label_details_for_crud(self):
        self.client.post(self.register_url, self.valid_registration_data, format='json')
        user = User.objects.filter(email=self.valid_registration_data['email']).first()
        user.is_verified = True
        user.is_active = True
        user.save()
        response = self.client.post(self.login_url, self.valid_login_data, format='json')
        headers = response.data['data']

        response = self.client.post(self.label_post_url, self.valid_label_data, HTTP_AUTHORIZATION=headers,
                                    format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = self.client.get(self.label_url, HTTP_AUTHORIZATION=headers, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.delete(self.label_url, HTTP_AUTHORIZATION=headers, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_given_invalid_label_details_for_crud(self):
        self.client.post(self.register_url, self.valid_registration_data, format='json')
        user = User.objects.filter(email=self.valid_registration_data['email']).first()
        user.is_verified = True
        user.is_active = True
        user.save()
        response = self.client.post(self.login_url, self.valid_login_data, format='json')
        headers = response.data['data']
        response = self.client.post(self.label_post_url, self.invalid_label_data, HTTP_AUTHORIZATION=headers,
                                    format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        response = self.client.get(self.label_url, HTTP_AUTHORIZATION=headers, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        response = self.client.put(self.label_url, self.valid_label_put_data, HTTP_AUTHORIZATION=headers, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        response = self.client.delete(self.label_url, HTTP_AUTHORIZATION=headers, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class NoteTest(Data):
    """
    Test case for validating Notes class with valid and invalid details.
    """

    def test_notes_with_valid_details(self):
        """
        Test case for validating Labels class with valid details.
        """
        client = APIClient()
        self.client.post(self.register_url, self.valid_registration_data, format='json')
        user = User.objects.filter(email=self.valid_registration_data['email']).first()
        user.is_verified = True
        user.is_active = True
        user.save()
        response = client.post(self.login_url, self.valid_login_data, format='json')
        headers = response.data['data']

        response = self.client.post(self.label_url, self.valid_label_data, HTTP_AUTHORIZATION=headers, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response = client.post(self.note_post_url, self.valid_note_data, HTTP_AUTHORIZATION=headers, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = client.put(self.note_url, self.valid_note_put_data, HTTP_AUTHORIZATION=headers, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.get(self.note_url, HTTP_AUTHORIZATION=headers, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.delete(self.note_url, HTTP_AUTHORIZATION=headers, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_notes_with_invalid_details(self):
        """
        Test case for validating Labels class with invalid details.
        """
        client = APIClient()
        self.client.post(self.register_url, self.valid_registration_data, format='json')
        user = User.objects.filter(email=self.valid_registration_data['email']).first()
        user.is_verified = True
        user.is_active = True
        user.save()
        response = client.post(self.login_url, self.valid_login_data, format='json')
        headers = response.data['data']

        response = self.client.post(self.note_post_url, self.invalid_note_data, HTTP_AUTHORIZATION=headers,
                                    format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        response = self.client.get(self.note_url, HTTP_AUTHORIZATION=headers, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        response = self.client.put(self.note_url, self.valid_note_put_data, HTTP_AUTHORIZATION=headers, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        response = self.client.delete(self.note_url, HTTP_AUTHORIZATION=headers, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class ArchivedViewTest(Data):
    """
    ArchivedViewTest class with valid and invalid details.
    """

    def test_archived_view_for_valid_details(self):
        
        client = APIClient()
        self.client.post(self.register_url, self.valid_registration_data, format='json')
        user = User.objects.filter(email=self.valid_registration_data['email']).first()
        user.is_verified = True
        user.is_active = True
        user.save()
        response = self.client.post(self.login_url, self.valid_login_data, format='json')
        headers = response.data['data']
        self.client.post(self.label_url, self.valid_label_data, HTTP_AUTHORIZATION=headers, format='json')
        client.post(self.note_post_url, self.valid_note_data, HTTP_AUTHORIZATION=headers, format='json')
        client.post(self.note_post_url, self.valid_note_data2, HTTP_AUTHORIZATION=headers, format='json')

        response = client.get(self.note_archived_url, HTTP_AUTHORIZATION=headers, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = client.get(self.single_note_archived_url, HTTP_AUTHORIZATION=headers, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class PinnedViewTest(Data):
    """
    PinnedView class with valid and invalid details.
    """

    def test_pinned_view_for_valid_details(self):
        
        client = APIClient()
        self.client.post(self.register_url, self.valid_registration_data, format='json')
        user = User.objects.filter(email=self.valid_registration_data['email']).first()
        user.is_verified = True
        user.is_active = True
        user.save()
        response = self.client.post(self.login_url, self.valid_login_data, format='json')
        headers = response.data['data']
        self.client.post(self.label_url, self.valid_label_data, HTTP_AUTHORIZATION=headers, format='json')
        client.post(self.note_post_url, self.valid_note_data, HTTP_AUTHORIZATION=headers, format='json')
        client.post(self.note_post_url, self.valid_note_data2, HTTP_AUTHORIZATION=headers, format='json')

        response = client.get(self.note_pinned_url, HTTP_AUTHORIZATION=headers, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TrashViewTest(Data):

    def test_trash_view_for_valid_details(self):
        client = APIClient()
        self.client.post(self.register_url, self.valid_registration_data, format='json')
        user = User.objects.filter(email=self.valid_registration_data['email']).first()
        user.is_verified = True
        user.is_active = True
        user.save()
        response = self.client.post(self.login_url, self.valid_login_data, format='json')
        headers = response.data['data']
        self.client.post(self.label_url, self.valid_label_data, HTTP_AUTHORIZATION=headers, format='json')
        client.post(self.note_post_url, self.valid_note_data2, HTTP_AUTHORIZATION=headers, format='json')

        response = self.client.get(self.note_trash_url, HTTP_AUTHORIZATION=headers, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # response = self.client.get(self.single_note_trash_url, HTTP_AUTHORIZATION=headers, format='json')
        # self.assertEqual(response.status_code, status.HTTP_200_OK)


class SearchViewTest(Data):

    def test_search_view_for_valid_details(self):
        client = APIClient()
        self.client.post(self.register_url, self.valid_registration_data, format='json')
        user = User.objects.filter(email=self.valid_registration_data['email']).first()
        user.is_verified = True
        user.is_active = True
        user.save()
        response = self.client.post(self.login_url, self.valid_login_data, format='json')
        headers = response.data['data']
        self.client.post(self.label_url, self.valid_label_data, HTTP_AUTHORIZATION=headers, format='json')
        client.post(self.note_post_url, self.valid_note_data, HTTP_AUTHORIZATION=headers, format='json')
        response = self.client.get(self.note_search_url, HTTP_AUTHORIZATION=headers, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)