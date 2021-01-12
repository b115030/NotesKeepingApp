from django.urls import reverse, resolve
import django
django.setup()

class TestUrls:
    def test_url(self):
        path = reverse("register")
        assert resolve(path).view_name == "register"

    def test_login_url(self):
        path = reverse("login")
        assert resolve(path).view_name == "login"