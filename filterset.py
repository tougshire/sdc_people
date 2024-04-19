import django_filters
from .models import Person, Meeting, Membershipclass, Subcommittee
from django.db import models
from django import forms
from django_filters_stoex.filters import CrossFieldSearchFilter
from touglates.widgets import DropdownSelectMultiple


class PersonFilter(django_filters.FilterSet):
    filterset_name = forms.CharField()
    combined_text_search = CrossFieldSearchFilter(
        label="Name",
        field_name="name_last,name_first,name_middles,name_friendly",
        lookup_expr="icontains",
        help_text="Any part of the person's name",
    )

    subcommittee__in = django_filters.ModelMultipleChoiceFilter(
        label="Sub-committee",
        field_name="submembership__subposition__subcommittee",
        queryset=Subcommittee.objects.all(),
        help_text="Any of the subcomittees of which the person is a member",
        widget=DropdownSelectMultiple(),
    )
    # try:
    #     subcommittee__in.widget = DropdownSelectMultiple()
    #     print("tp244j755")
    # except NameError:
    #     try:
    #         subcommittee__in.widget = touglates.DropdownSelectMultiple()
    #     except NameError:
    #         pass

    membershipclass = django_filters.ModelMultipleChoiceFilter(
        queryset=Membershipclass.objects.all(), widget=forms.CheckboxSelectMultiple()
    )
    orderbyfields = django_filters.OrderingFilter(
        fields=(
            "name_friendly",
            "name_first",
            "name_last",
            "membershipclass",
            "membership_date",
            "districtprecinct",
            "districtborough",
            "districtstatehouse",
            "districtstatesenate",
            "districtcongress",
        ),
    )

    class Meta:
        model = Person
        fields = []
        # [
        #     "name_friendly",
        #     "name_first",
        #     "name_last",
        #     "membershipclass",
        #     "membershipclass__is_quorum_member",
        #     "membership_date",
        #     "districtprecinct",
        #     "districtborough",
        #     "districtstatehouse",
        #     "districtstatesenate",
        #     "districtcongress",
        #     "primary_voice",
        #     "primary_text",
        #     "primary_email",
        #     "voting_address",
        #     "mailing_address",
        # ]


class MeetingFilter(django_filters.FilterSet):
    filterset_name = forms.CharField()

    membershiptype = django_filters.ModelMultipleChoiceFilter(
        queryset=Membershipclass.objects.all(), widget=forms.CheckboxSelectMultiple()
    )
    orderbyfields = django_filters.OrderingFilter(
        fields=(
            "when_held",
            "meetingtype",
        ),
    )

    class Meta:
        model = Meeting
        fields = [
            "when_held",
            "meetingtype",
        ]
