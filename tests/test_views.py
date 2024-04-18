from django.test import TestCase
from django.db import models
from sdc_people.models import Person, Subcommittee, Subcommitteetype, Subposition
from .setup_mixins import TestModelSetupMixin
from django.test import Client


# Ensure all required models have __str__() and ordering
class ViewBasicsTestCase(TestModelSetupMixin, TestCase):
    def test_login_required(self):
        urls = (
            ["/sdc_people/", "/sdc_people/person/list/"],
            ["/sdc_people/person/", "/sdc_people/person/list/"],
            ["/sdc_people/person/list/"],
        )
        client = Client()
        for url in urls:
            response = client.get(url[0], follow=True)
            self.assertRedirects(
                response,
                "/accounts/login/?next=" + (url[1] if len(url) == 2 else url[0]),
                302,
            )
