from django.test import TestCase
from django.db import models
from .setup_mixins import TestModelSetupMixin
from sdc_people.models import Person, Subcommittee, Subcommitteetype, Subposition


# Ensure all required models have __str__() and ordering
class ModelBasicsTestCase(TestModelSetupMixin, TestCase):
    def setUp(self):
        self.str = {}
        self.str["subcommitteetype_executive"] = "Executive"
        self.str["subcommittee_technology"] = "Technology Committee"
        self.str["subposition_technology_chair"] = "Chair, Technology Committee"
        self.str["person_ben"] = "Mr. Benjamin Goldberg II (Ben)"

    def test_str(self):

        for key, obj in self.text_objects.items():
            self.assertNotEqual(obj.__str__(), models.Model.__str__(obj))
            if key in self.str:
                self.assertEqual(obj.__str__(), self.str[key])
