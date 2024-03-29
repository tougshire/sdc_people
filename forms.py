from django.conf import settings
from django.forms import ModelForm, inlineformset_factory, Select
from django.urls import reverse_lazy
from .models import (
    Attendance,
    DistrictBorough,
    DistrictCongress,
    DistrictMagisterial,
    DistrictPrecinct,
    DistrictStatehouse,
    DistrictStatesenate,
    Linkexternal,
    Person,
    Subcommittee,
    Subcommitteetype,
    Submembership,
    Subposition,
)
from django import forms
from touglates.widgets import TouglateDateInput, TouglateRelatedSelect


class AttendanceForm(ModelForm):
    class Meta:
        model = Attendance
        fields = [
            "person",
            "meeting",
        ]


class DistrictPrecinctForm(ModelForm):
    class Meta:
        model = DistrictPrecinct
        fields = ["number", "name"]


class DistrictPrecinctForm(ModelForm):
    class Meta:
        model = DistrictPrecinct
        fields = ["number", "name"]


class DistrictBoroughForm(ModelForm):
    class Meta:
        model = DistrictBorough
        fields = ["number", "name"]


class DistrictMagisterialForm(ModelForm):
    class Meta:
        model = DistrictMagisterial
        fields = ["number", "name"]


class DistrictStatehouseForm(ModelForm):
    class Meta:
        model = DistrictStatehouse
        fields = ["number", "name"]


class DistrictStatesenateForm(ModelForm):
    class Meta:
        model = DistrictStatesenate
        fields = ["number", "name"]


class DistrictCongressForm(ModelForm):
    class Meta:
        model = DistrictCongress
        fields = ["number", "name"]


class LinkexternalForm(ModelForm):
    class Meta:
        model = Linkexternal
        fields = [
            "person",
            "name",
            "url",
        ]


class PersonForm(ModelForm):

    class Meta:
        model = Person
        fields = [
            "application_date",
            "districtborough",
            "districtcongress",
            "districtprecinct",
            "districtstatehouse",
            "districtstatesenate",
            "dues_effective_date",
            "mailing_address",
            "membership_date",
            "membershipclass",
            "name_first",
            "name_formal",
            "name_friendly",
            "name_last",
            "primary_email",
            "primary_text",
            "primary_voice",
            "voting_address",
        ]
        widgets = {
            "districtborough": TouglateRelatedSelect(
                related_data={
                    "model": "DistrictBorough",
                    "add_url": reverse_lazy("sdc_people:districtborough-popup"),
                }
            ),
            "districtprecinct": TouglateRelatedSelect(
                related_data={
                    "model": "DistrictPrecinct",
                    "add_url": reverse_lazy("sdc_people:districtprecinct-popup"),
                }
            ),
            "districtmagisterial": TouglateRelatedSelect(
                related_data={
                    "model": "DistrictMagisterial",
                    "add_url": reverse_lazy("sdc_people:districtmagisterial-popup"),
                }
            ),
            "districtstatehouse": TouglateRelatedSelect(
                related_data={
                    "model": "DistrictStatehouse",
                    "add_url": reverse_lazy("sdc_people:districtstatehouse-popup"),
                }
            ),
            "districtstatesenate": TouglateRelatedSelect(
                related_data={
                    "model": "DistrictStatesenate",
                    "add_url": reverse_lazy("sdc_people:districtstatesenate-popup"),
                }
            ),
            "districtcongress": TouglateRelatedSelect(
                related_data={
                    "model": "DistrictCongress",
                    "add_url": reverse_lazy("sdc_people:districtcongress-popup"),
                }
            ),
            "membership_date": TouglateDateInput(),
        }


class SubmembershipForm(ModelForm):
    class Meta:
        model = Submembership
        fields = [
            "person",
            "subposition",
        ]
        widgets = {
            "subposition": TouglateRelatedSelect(
                related_data={
                    "model": "Subposition",
                    "add_url": reverse_lazy("sdc_people:subposition-popup"),
                }
            )
        }


class SubcommitteeForm(ModelForm):
    class Meta:
        model = Subcommittee
        fields = [
            "subcommitteetype",
            "name",
        ]
        widgets = {
            "subcommitteetype": TouglateRelatedSelect(
                related_data={
                    "model": "Subcommitteetype",
                    "add_url": reverse_lazy("sdc_people:subcommitteetype-popup"),
                }
            )
        }


class SubcommitteetypeForm(ModelForm):
    class Meta:
        model = Subcommitteetype
        fields = [
            "name",
            "ordinal",
        ]


class SubpositionForm(ModelForm):
    class Meta:
        model = Subposition
        fields = [
            "subcommittee",
            "name",
            "ordinal",
        ]
        widgets = {
            "subcommittee": TouglateRelatedSelect(
                related_data={
                    "model": "Subcommittee",
                    "add_url": reverse_lazy("sdc_people:subcommittee-popup"),
                }
            )
        }


PersonAttendanceFormset = inlineformset_factory(
    Person, Attendance, form=AttendanceForm, extra=10
)

PersonLinkexternalFormset = inlineformset_factory(
    Person, Linkexternal, form=LinkexternalForm, extra=10
)
PersonsubmembershipFormset = inlineformset_factory(
    Person, Submembership, form=SubmembershipForm, extra=10
)