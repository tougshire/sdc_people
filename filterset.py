import django_filters
from .models import (
    DistrictBorough,
    DistrictCongress,
    DistrictPrecinct,
    DistrictStatehouse,
    DistrictStatesenate,
    Person,
    Meeting,
    Membershipclass,
    Subcommittee,
)
from django.db import models
from django import forms
from django_filters_stoex.filters import ChainableOrderingFilter, CrossFieldSearchFilter
from touglates.widgets import DropdownSelectMultiple


class PersonFilter(django_filters.FilterSet):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

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

    membershipclass = django_filters.ModelMultipleChoiceFilter(
        queryset=Membershipclass.objects.all(), widget=DropdownSelectMultiple()
    )
    membershipclass__is_quorum_member = django_filters.MultipleChoiceFilter(
        field_name="membershipclass__is_quorum_member",
        label="Is Quorum Member",
        choices=Membershipclass._meta.get_field("is_quorum_member").choices,
        widget=DropdownSelectMultiple(),
    )
    membershipclass__is_member = django_filters.MultipleChoiceFilter(
        field_name="membershipclass__is_member",
        label="Is Member",
        choices=Membershipclass._meta.get_field("is_member").choices,
        widget=DropdownSelectMultiple(),
    )
    precinct = django_filters.ModelMultipleChoiceFilter(
        field_name="districtprecinct",
        queryset=DistrictPrecinct.objects.all(),
        widget=DropdownSelectMultiple(),
    )
    borough = django_filters.ModelMultipleChoiceFilter(
        field_name="districtborough",
        queryset=DistrictBorough.objects.all(),
        widget=DropdownSelectMultiple(),
    )
    statehouse = django_filters.ModelMultipleChoiceFilter(
        field_name="districtstatehouse",
        queryset=DistrictStatehouse.objects.all(),
        widget=DropdownSelectMultiple(),
    )
    statesenate = django_filters.ModelMultipleChoiceFilter(
        field_name="districtstatesenate",
        queryset=DistrictStatesenate.objects.all(),
        widget=DropdownSelectMultiple(),
    )
    congress = django_filters.ModelMultipleChoiceFilter(
        field_name="districtcongress",
        queryset=DistrictCongress.objects.all(),
        widget=DropdownSelectMultiple(),
    )

    def optional_boolian(self, queryset, name, value=None):
        if value is None:
            return queryset
        else:
            return queryset.filter(**{name: value})

    orderbyfields_available = [
        ("name_friendly", "Friendly Name"),
        ("name_first", "First Name"),
        ("name_last", "Last Name"),
        ("membershipclass", "Membership Class"),
        ("membershipclass__is_member", "Is Member"),
        ("membershipclass__is_quorum_member", "Is Quorum Member"),
        ("membership_date", "Membership Date"),
        ("districtprecinct", "Precinct"),
        ("districtborough", "Borough"),
        ("districtstatehouse", "State House"),
        ("districtstatesenate", "State Senate"),
        ("districtcongress", "Congress"),
    ]
    orderbyfields = ChainableOrderingFilter(fields=orderbyfields_available)
    orderbyfields1 = ChainableOrderingFilter(fields=orderbyfields_available)
    orderbyfields2 = ChainableOrderingFilter(fields=orderbyfields_available)

    class Meta:
        model = Person
        fields = []


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
