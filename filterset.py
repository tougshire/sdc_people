import django_filters
from .models import Person, Membershipclass
from django.db import models
from django import forms
from django_filters_stoex.filters import MultipleFieldsContainsFilter


class PersonFilter(django_filters.FilterSet):
    filterset_name = forms.CharField()
    combined_text_search = MultipleFieldsContainsFilter(
        label="text search",
        field_name="name_last,name_first,name_middles,name_friendly",
        lookup_expr="icontains",
    )

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
        fields = [
            "name_friendly",
            "name_first",
            "name_last",
            "membershipclass",
            "membershipclass",
            "membership_date",
            "districtprecinct",
            "districtborough",
            "districtstatehouse",
            "districtstatesenate",
            "districtcongress",
            "primary_voice",
            "primary_text",
            "primary_email",
            "voting_address",
            "mailing_address",
        ]