from django.db import models
from sdc_people.models import (
    Person,
    Subcommittee,
    Subcommitteetype,
    Submembership,
)


class TestModelSetupMixin:
    @classmethod
    def setUpTestData(cls):

        cls.text_objects = {}

        cls.text_objects["subcommitteetype_executive"] = (
            Subcommitteetype.objects.create(name="Executive")
        )
        cls.text_objects["subcommitteetype_standing"] = Subcommitteetype.objects.create(
            name="Standing"
        )
        cls.text_objects["subcommitteetype_adhoc"] = Subcommitteetype.objects.create(
            name="Ad-Hoc"
        )

        cls.text_objects["subcommittee_executive"] = Subcommittee.objects.create(
            name="Executive Committee",
            subcommitteetype=cls.text_objects["subcommitteetype_executive"],
        )
        cls.text_objects["subcommittee_membership"] = Subcommittee.objects.create(
            name="Membership Committee",
            subcommitteetype=cls.text_objects["subcommitteetype_standing"],
        )
        cls.text_objects["subcommittee_technology"] = Subcommittee.objects.create(
            name="Technology Committee",
            subcommitteetype=cls.text_objects["subcommitteetype_adhoc"],
        )


        cls.text_objects["person_ben"] = Person.objects.create(
            name_formal="Mr. Benjamin Goldberg II",
            name_first="Benjamin",
            name_friendly="Ben",
            name_last="Goldberg",
            primary_email="testing@bnmng.com",
            primary_text="757-555-1212",
            primary_voice="757-555-1212",
            voting_address="1414 Hillside Avenue Suffolk, VA 23434",
            mailing_address="PO Box 14 Suffolk, VA 23434",
        )

        cls.text_objects["submembership_ben_technology_chair"] = (
            Submembership.objects.create(
                person=cls.text_objects["person_ben"],
                position="Chair",
                ordinal=0,
            )
        )
