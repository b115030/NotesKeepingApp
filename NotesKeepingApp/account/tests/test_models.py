from mixer.backend.django import mixer
import pytest
import django
django.setup()
@pytest.mark.django_db
class TestModels:
    def test_account(self):
        user = mixer.blend('account.User')
        assert user.id == 1

    def test_accounts(self):
        user = mixer.blend('account.User')
        assert user.id !=0
