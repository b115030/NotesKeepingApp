import pytest
from mixer.backend.django import mixer
import django
django.setup()

# pytestmark = pytest.mark.django_db

@pytest.mark.django_db
class TestModels:
    def test_notes(self):
        note = mixer.blend('notes.Note')
        assert note.id == 1

    def test_accounts(self):
        user = mixer.blend('notes.Note')
        assert user.id !=0