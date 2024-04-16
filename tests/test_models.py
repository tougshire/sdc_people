from django.test import TestCase
from django.db import models
from sdc_people.models import Person


# Ensure all required models have __str__() and ordering
class ModelBasicsTestCase(TestCase):
    def setUp(self):
        self.check_objects = {}

        self.check_objects["person"] = Person.objects.create(
            name_formal="Mr. Benjamin Goldberg II",
            name_first="Benjamin",
            name_friendly="Ben",
            name_last="Goldberg",
            primary_email="testing@bnmng.com",
            primary_text="757-555-1212",
            primary_voice="757-555-1212",
            voting_address="1313 Hillside Avenue Suffolk, VA 23434",
        )
        self.check_objects["person"].check_str = "Mr. Benjamin Goldberg II (Ben)"

    def test_str(self):
        for key, obj in self.check_objects.items():
            print(obj)
            self.assertNotEqual(obj.__str__(), models.Model.__str__(obj))
            self.assertEqual(obj.__str__(), obj.check_str)
