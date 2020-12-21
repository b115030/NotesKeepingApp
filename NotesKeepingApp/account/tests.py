from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from decouple import config

User = get_user_model()


class Data(APITestCase):
    def setUp(self):
        self.register_url = config('URL')+'register/'#'http://127.0.0.1:8000/register/'
        self.login_url = config('URL')+'login/'#'http://127.0.0.1:8000/login/'
        self.valid_registration_data = {'first_name': "Gopinath",
                                        'last_name': "Das",
                                        'email': "iitiangokul@gmail.com",
                                        'user_name': "gopinathdas",
                                        'password': "bluelagoon"}
        self.invalid_registration_data = {'first_name': "asd",
                                          'last_name': "qwerty",
                                          'email': "abcemailcom",
                                          'user_name': "as"}
        self.valid_login_data = {
            'email': "iitiangokul@gmail.com",
            'password': "bluelagoon"}
        self.invalid_login_data = {
            'email': "iitiangokul@gmail.com",
            'password': "adminpass"}


class RegistrationTest(Data):

    def test_given_valid_details_returns_201(self):
        
        """
        positive Test cases for registration

        """
        response = self.client.post(self.register_url, self.valid_registration_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_given_invalid_details_return_400(self):
        """
        Negative Test cases for registration

        """        

        response = self.client.post(self.register_url, self.invalid_registration_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class LoginTest(Data):

    def test_given_valid_credentials_login_returns_200(self):
        """
        positive Test cases for login 
        """

        self.client.post(self.register_url, self.valid_registration_data, format='json')
        user = User.objects.filter(email=self.valid_registration_data['email']).first()
        user.is_active = True
        user.save()

        response = self.client.post(self.login_url, self.valid_login_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_given_invalid_credentials_for_login_returns_401(self):
        """
        Negative Test cases for login 
        """

        self.client.post(self.register_url, self.valid_registration_data, format='json')
        user = User.objects.filter(email=self.valid_registration_data['email']).first()
        user.is_active = True
        user.save()

        response = self.client.post(self.login_url, self.invalid_login_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)