import datetime

from django import forms
from django.forms import ModelForm, SelectDateWidget, inlineformset_factory
from django.urls import reverse_lazy

from touglates.widgets import TouglatesRelatedSelect

from .models import (
    Attendance,
    DistrictBorough,
    DistrictCongress,
    DistrictMagisterial,
    DistrictPrecinct,
    DistrictStatehouse,
    DistrictStatesenate,
    Due,
    Duestat,
    Image,
    Linkexternal,
    Meeting,
    Meetingtype,
    Membershipclass,
    Person,
    Personnote,
    Subcommittee,
    Subcommitteetype,
    Submembership,
    Subposition,
)


class AttendanceForm(ModelForm):
    class Meta:
        model = Attendance
        fields = [
            "person",
            "meeting",
        ]
        widgets = {
            "meeting": TouglatesRelatedSelect(
                related_data={
                    "model_name": "Meeting",
                    "app_name": "sdc_people",
                    "add_url": reverse_lazy("sdc_people:meeting-popup"),
                }
            ),
            "person": TouglatesRelatedSelect(
                related_data={
                    "model_name": "Person",
                    "app_name": "sdc_people",
                    "add_url": reverse_lazy("sdc_people:person-popup"),
                },
                add_filter_input="true",
            ),
        }


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


class DueForm(ModelForm):
    class Meta:
        model = Due
        fields = [
            "due_date",
        ]


class DuestatForm(ModelForm):
    class Meta:
        model = Duestat
        fields = [
            "due",
            "person",
            "effective_date",
            "status",
        ]


class ImageForm(ModelForm):
    class Meta:
        model = Image
        fields = [
            "person",
            "imagefile",
            "imagetype",
        ]


class LinkexternalForm(ModelForm):
    class Meta:
        model = Linkexternal
        fields = [
            "person",
            "linkexternaltype",
            "url",
        ]


class MeetingForm(ModelForm):
    class Meta:
        model = Meeting
        fields = [
            "meetingtype",
            "when_held",
            "had_quorum",
            "meetingtype",
        ]
        widgets = {
            "meetingtype": TouglatesRelatedSelect(
                related_data={
                    "model_name": "Meetingtype",
                    "app_name": "sdc_people",
                    "add_url": reverse_lazy("sdc_people:meetingtype-popup"),
                }
            ),
            "when_held": SelectDateWidget(
                years=[datetime.date.today().year - 1, datetime.date.today().year]
                + list(
                    range(
                        datetime.date.today().year - 10, datetime.date.today().year + 10
                    )
                ),
            ),
        }


class MeetingtypeForm(ModelForm):
    class Meta:
        model = Meetingtype
        fields = [
            "name",
            "ordinal",
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
            "demog_is_veteran",
        ]
        widgets = {
            "districtborough": TouglatesRelatedSelect(
                related_data={
                    "model_name": "DistrictBorough",
                    "app_name": "sdc_people",
                    "add_url": reverse_lazy("sdc_people:districtborough-popup"),
                }
            ),
            "districtprecinct": TouglatesRelatedSelect(
                related_data={
                    "model_name": "DistrictPrecinct",
                    "app_name": "sdc_people",
                    "add_url": reverse_lazy("sdc_people:districtprecinct-popup"),
                }
            ),
            "districtmagisterial": TouglatesRelatedSelect(
                related_data={
                    "model_name": "DistrictMagisterial",
                    "app_name": "sdc_people",
                    "add_url": reverse_lazy("sdc_people:districtmagisterial-popup"),
                }
            ),
            "districtstatehouse": TouglatesRelatedSelect(
                related_data={
                    "model_name": "DistrictStatehouse",
                    "app_name": "sdc_people",
                    "add_url": reverse_lazy("sdc_people:districtstatehouse-popup"),
                }
            ),
            "districtstatesenate": TouglatesRelatedSelect(
                related_data={
                    "model_name": "DistrictStatesenate",
                    "app_name": "sdc_people",
                    "add_url": reverse_lazy("sdc_people:districtstatesenate-popup"),
                }
            ),
            "districtcongress": TouglatesRelatedSelect(
                related_data={
                    "model_name": "DistrictCongress",
                    "app_name": "sdc_people",
                    "add_url": reverse_lazy("sdc_people:districtcongress-popup"),
                }
            ),
            "membershipclass": TouglatesRelatedSelect(
                related_data={
                    "model_name": "Membershipclass",
                    "app_name": "sdc_people",
                    "add_url": reverse_lazy("sdc_people:membershipclass-popup"),
                }
            ),
            "membership_date": SelectDateWidget(
                years=[datetime.date.today().year - 1, datetime.date.today().year]
                + list(
                    range(
                        datetime.date.today().year - 10, datetime.date.today().year + 10
                    )
                ),
            ),
            "dues_effective_date": SelectDateWidget(
                years=[datetime.date.today().year - 1, datetime.date.today().year]
                + list(
                    range(
                        datetime.date.today().year - 10, datetime.date.today().year + 10
                    )
                ),
            ),
            "application_date": SelectDateWidget(
                years=[datetime.date.today().year - 1, datetime.date.today().year]
                + list(
                    range(
                        datetime.date.today().year - 10, datetime.date.today().year + 10
                    )
                ),
            ),
        }


class MembershipclassForm(ModelForm):
    class Meta:
        model = Membershipclass
        fields = [
            "name",
            "is_member",
            "is_quorum_member",
            "is_participant",
            "ordinal",
        ]


class PersonnoteForm(ModelForm):
    class Meta:
        model = Personnote
        fields = [
            "person",
            "personnotetype",
            "content",
            "when",
            "expiration",
            "is_flagged",
        ]


class SubmembershipForm(ModelForm):
    class Meta:
        model = Submembership
        fields = [
            "person",
            "subposition",
        ]
        widgets = {
            "subposition": TouglatesRelatedSelect(
                related_data={
                    "model_name": "Subposition",
                    "app_name": "sdc_people",
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
            "subcommitteetype": TouglatesRelatedSelect(
                related_data={
                    "model_name": "Subcommitteetype",
                    "app_name": "sdc_people",
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
            "subcommittee": TouglatesRelatedSelect(
                related_data={
                    "model_name": "Subcommittee",
                    "app_name": "sdc_people",
                    "add_url": reverse_lazy("sdc_people:subcommittee-popup"),
                }
            )
        }


class CSVOptionForm(forms.Form):
    make_csv = forms.BooleanField(
        label="CSV",
        initial=False,
        required=False,
        help_text="Download the result as a CSV file",
    )

DueDuestatFormset = inlineformset_factory (
    Due, Duestat, form=DuestatForm, extra=1
)

MeetingAttendanceFormset = inlineformset_factory(
    Meeting, Attendance, form=AttendanceForm, extra=50
)

PersonAttendanceFormset = inlineformset_factory(
    Person, Attendance, form=AttendanceForm, extra=10
)

PersonImageFormset = inlineformset_factory(Person, Image, form=ImageForm, extra=10)

PersonLinkexternalFormset = inlineformset_factory(
    Person, Linkexternal, form=LinkexternalForm, extra=10
)
PersonsubmembershipFormset = inlineformset_factory(
    Person, Submembership, form=SubmembershipForm, extra=10
)
PersonpersonnoteFormset = inlineformset_factory(
    Person, Personnote, form=PersonnoteForm, extra=10
)
