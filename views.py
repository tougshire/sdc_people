import logging
from django.shortcuts import render
from django.urls import reverse, reverse_lazy, resolve

from django_filters_stoex.forms import (
    FilterstoreRetrieveForm,
    FilterstoreSaveForm,
    CSVOptionForm,
)
from django_filters_stoex.views import FilterView
from sdc_people.filterset import PersonFilter
from .models import (
    DistrictBorough,
    DistrictCongress,
    DistrictMagisterial,
    DistrictPrecinct,
    DistrictStatehouse,
    DistrictStatesenate,
    Meeting,
    Meetingtype,
    Person,
    Subcommittee,
    Subcommitteetype,
    Subposition,
)
from .forms import (
    DistrictBoroughForm,
    DistrictCongressForm,
    DistrictMagisterialForm,
    DistrictBoroughForm,
    DistrictPrecinctForm,
    DistrictStatehouseForm,
    DistrictStatesenateForm,
    LinkexternalForm,
    MeetingForm,
    MeetingtypeForm,
    PersonAttendanceFormset,
    PersonForm,
    PersonImageFormset,
    PersonLinkexternalFormset,
    PersonsubmembershipFormset,
    SubcommitteeForm,
    SubcommitteetypeForm,
    SubpositionForm,
)
from django.views.generic.edit import (
    CreateView,
    DeleteView,
    FormView,
    UpdateView,
    FormMixin,
)
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.http import HttpResponse, QueryDict
from urllib.parse import urlencode
from django.core.exceptions import FieldError

logger = logging.getLogger(__name__)


class PersonCreate(PermissionRequiredMixin, CreateView):
    permission_required = "sdc_people.add_Person"
    model = Person
    form_class = PersonForm
    template_name = "sdc_people/person_add.html"

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)

        formsetclasses = {
            "images": PersonImageFormset,
            "linkexternals": PersonLinkexternalFormset,
            "submemberships": PersonsubmembershipFormset,
            "attendances": PersonAttendanceFormset,
        }

        for formsetkey, formsetclass in formsetclasses.items():
            if self.request.POST:
                context_data[formsetkey] = formsetclass(self.request.POST)
            else:
                context_data[formsetkey] = formsetclass()

        return context_data

    def form_valid(self, form):
        response = super().form_valid(form)

        # update_history(form, "Person", form.instance, self.request.user)

        self.object = form.save(commit=False)

        formsetclasses = {
            "images": PersonImageFormset,
            "linkexternals": PersonLinkexternalFormset,
            "submemberships": PersonsubmembershipFormset,
            "attendances": PersonAttendanceFormset,
        }
        formsetdata = {}
        formsets_valid = True
        for formsetkey, formsetclass in formsetclasses.items():
            if self.request.POST:
                formsetdata[formsetkey] = formsetclass(
                    self.request.POST, instance=self.object
                )
            else:
                formsetdata[formsetkey] = formsetclass(instance=self.object)

            if (formsetdata[formsetkey]).is_valid():
                formsetdata[formsetkey].save()
            else:
                logger.critical(formsetdata[formsetkey].errors)
                for err in formsetdata[formsetkey].errors:
                    form.add_error(None, err)
                    for formsetform in formsetdata[formsetkey].forms:
                        for err in formsetform.errors:
                            form.add_error(None, err)
                formsets_valid = False

        if not formsets_valid:
            return self.form_invalid(form)

        return response

    def get_success_url(self):

        if "popup" in self.request.get_full_path():
            return reverse(
                "touglates:popup_closer",
                kwargs={
                    "pk": self.object.pk,
                    "app_name": "sdc_people",
                    "model_name": "Person",
                },
            )
        return reverse_lazy("sdc_people:person-detail", kwargs={"pk": self.object.pk})


class PersonUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = "sdc_people.change_Person"
    model = Person
    form_class = PersonForm
    template_name = "sdc_people/person_change.html"

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)

        formsetclasses = {
            "images": PersonImageFormset,
            "linkexternals": PersonLinkexternalFormset,
            "submemberships": PersonsubmembershipFormset,
            "attendances": PersonAttendanceFormset,
        }

        for formsetkey, formsetclass in formsetclasses.items():
            if self.request.POST:
                context_data[formsetkey] = formsetclass(
                    self.request.POST, instance=self.object
                )
            else:
                context_data[formsetkey] = formsetclass(instance=self.object)

        return context_data

    def form_valid(self, form):
        response = super().form_valid(form)

        # update_history(form, "Person", form.instance, self.request.user)

        self.object = form.save(commit=False)

        formsetclasses = {
            "images": PersonImageFormset,
            "linkexternals": PersonLinkexternalFormset,
            "submemberships": PersonsubmembershipFormset,
            "attendances": PersonAttendanceFormset,
        }
        formsetdata = {}
        formsets_valid = True
        for formsetkey, formsetclass in formsetclasses.items():
            if self.request.POST:
                formsetdata[formsetkey] = formsetclass(
                    self.request.POST, instance=self.object
                )
            else:
                formsetdata[formsetkey] = formsetclass(instance=self.object)

            if (formsetdata[formsetkey]).is_valid():
                formsetdata[formsetkey].save()
            else:
                logger.critical(formsetdata[formsetkey].errors)
                for err in formsetdata[formsetkey].errors:
                    form.add_error(None, err)
                    for formsetform in formsetdata[formsetkey].forms:
                        for err in formsetform.errors:
                            form.add_error(None, err)
                formsets_valid = False

        if not formsets_valid:
            return self.form_invalid(form)

        return response

    def get_success_url(self):
        if "popup" in self.request.get_full_path():
            return reverse(
                "touglates:popup_closer",
                kwargs={
                    "pk": self.object.pk,
                    "app_name": "sdc_people",
                    "model_name": "Person",
                },
            )
        return reverse_lazy("sdc_people:person-detail", kwargs={"pk": self.object.pk})


class PersonDetail(PermissionRequiredMixin, DetailView):
    permission_required = "sdc_people.view_person"
    model = Person

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)

        context_data["person_labels"] = {
            field.name: field.verbose_name.title()
            for field in Person._meta.get_fields()
            if type(field).__name__[-3:] != "Rel"
        }

        return context_data


class PersonList(PermissionRequiredMixin, FilterView):

    permission_required = "sdc_people.view_person"
    filterset_class = PersonFilter
    filterstore_urlname = "sdc_people:person-filterstore"

    def get_context_data(self, *args, **kwargs):

        context_data = super().get_context_data(*args, **kwargs)

        context_data["filterstore_retrieve"] = FilterstoreRetrieveForm()
        context_data["filterstore_save"] = FilterstoreSaveForm()
        context_data["as_csv"] = CSVOptionForm()
        context_data["count"] = self.object_list.count()
        return context_data


class DistrictBoroughCreate(PermissionRequiredMixin, CreateView):
    permission_required = "sdc_people.add_districtborough"
    model = DistrictBorough
    form_class = DistrictBoroughForm
    template_name = "sdc_people/district_add.html"

    def get_success_url(self):
        if "popup" in self.request.get_full_path():
            return reverse(
                "touglates:popup_closer",
                kwargs={
                    "pk": self.object.pk,
                    "app_name": "sdc_people",
                    "model_name": "DistrictBorough",
                },
            )

        return reverse_lazy(
            "sdc_people:districtborough-detail", kwargs={"pk": self.object.pk}
        )


class DistrictBoroughDetail(PermissionRequiredMixin, DetailView):
    permission_required = "sdc_people.view_districtborough"
    model = DistrictBorough
    template_name = "sdc_people/district_detail.html"


class DistrictPrecinctCreate(PermissionRequiredMixin, CreateView):
    permission_required = "sdc_people.add_districtprecinct"
    model = DistrictPrecinct
    form_class = DistrictPrecinctForm
    template_name = "sdc_people/district_add.html"

    def get_success_url(self):
        if "popup" in self.request.get_full_path():
            return reverse(
                "touglates:popup_closer",
                kwargs={
                    "pk": self.object.pk,
                    "app_name": "sdc_people",
                    "model_name": "DistrictPrecinct",
                },
            )
        return reverse_lazy(
            "sdc_people:districtprecinct-detail", kwargs={"pk": self.object.pk}
        )


class DistrictPrecinctDetail(PermissionRequiredMixin, DetailView):
    permission_required = "sdc_people.view_districtprecinct"
    model = DistrictPrecinct
    template_name = "sdc_people/district_detail.html"


class DistrictMagisterialCreate(PermissionRequiredMixin, CreateView):
    permission_required = "sdc_people.add_districtmagisterial"
    model = DistrictMagisterial
    form_class = DistrictMagisterialForm
    template_name = "sdc_people/district_add.html"

    def get_success_url(self):
        if "popup" in self.request.get_full_path():
            return reverse(
                "touglates:popup_closer",
                kwargs={
                    "pk": self.object.pk,
                    "app_name": "sdc_people",
                    "model_name": "DistrictMagisterial",
                },
            )
        return reverse_lazy(
            "sdc_people:districtmagisterial-detail", kwargs={"pk": self.object.pk}
        )


class DistrictMagisterialDetail(PermissionRequiredMixin, DetailView):
    permission_required = "sdc_people.view_districtmagisterial"
    model = DistrictMagisterial
    template_name = "sdc_people/district_detail.html"


class DistrictStatehouseCreate(PermissionRequiredMixin, CreateView):
    permission_required = "sdc_people.add_districtstatehouse"
    model = DistrictStatehouse
    form_class = DistrictStatehouseForm
    template_name = "sdc_people/district_add.html"

    def get_success_url(self):
        if "popup" in self.request.get_full_path():
            return reverse(
                "touglates:popup_closer",
                kwargs={
                    "pk": self.object.pk,
                    "app_name": "sdc_people",
                    "model_name": "DistrictStatehouse",
                },
            )
        return reverse_lazy(
            "sdc_people:districtstatehouse-detail", kwargs={"pk": self.object.pk}
        )


class DistrictStatehouseDetail(PermissionRequiredMixin, DetailView):
    permission_required = "sdc_people.view_districtstatehouse"
    model = DistrictStatehouse
    template_name = "sdc_people/district_detail.html"


class DistrictStatesenateCreate(PermissionRequiredMixin, CreateView):
    permission_required = "sdc_people.add_districtstatesenate"
    model = DistrictStatesenate
    form_class = DistrictStatesenateForm
    template_name = "sdc_people/district_add.html"

    def get_success_url(self):
        if "popup" in self.request.get_full_path():
            return reverse(
                "touglates:popup_closer",
                kwargs={
                    "pk": self.object.pk,
                    "app_name": "sdc_people",
                    "model_name": "DistrictStatesenate",
                },
            )
        return reverse_lazy(
            "sdc_people:districtstatesenate-detail", kwargs={"pk": self.object.pk}
        )


class DistrictStatesenateDetail(PermissionRequiredMixin, DetailView):
    permission_required = "sdc_people.view_districtstatesenate"
    model = DistrictStatesenate
    template_name = "sdc_people/district_detail.html"


class DistrictCongressCreate(PermissionRequiredMixin, CreateView):
    permission_required = "sdc_people.add_districtcongress"
    model = DistrictCongress
    form_class = DistrictCongressForm
    template_name = "sdc_people/district_add.html"

    def get_success_url(self):
        if "popup" in self.request.get_full_path():
            return reverse(
                "touglates:popup_closer",
                kwargs={
                    "pk": self.object.pk,
                    "app_name": "sdc_people",
                    "model_name": "DistrictCongress",
                },
            )
        return reverse_lazy(
            "sdc_people:districtcongress-detail", kwargs={"pk": self.object.pk}
        )


class DistrictCongressDetail(PermissionRequiredMixin, DetailView):
    permission_required = "sdc_people.view_districtcongress"
    model = DistrictCongress
    template_name = "sdc_people/subposition_detail.html"


class MeetingCreate(PermissionRequiredMixin, CreateView):
    permission_required = "sdc_people.add_subcommittee"
    model = Meeting
    form_class = MeetingForm
    template_name = "sdc_people/subcommittee_add.html"

    def get_success_url(self):
        if "popup" in self.request.get_full_path():
            return reverse(
                "touglates:popup_closer",
                kwargs={
                    "pk": self.object.pk,
                    "app_name": "sdc_people",
                    "model_name": "Meeting",
                },
            )
        return reverse_lazy(
            "sdc_people:subcommittee-detail", kwargs={"pk": self.object.pk}
        )


class MeetingDetail(PermissionRequiredMixin, DetailView):
    permission_required = "sdc_people.view_subcommittee"
    model = Meeting
    template_name = "sdc_people/district_detail.html"


class MeetingtypeCreate(PermissionRequiredMixin, CreateView):
    permission_required = "sdc_people.add_subcommitteetype"
    model = Meetingtype
    form_class = MeetingtypeForm
    template_name = "sdc_people/subcommitteetype_add.html"

    def get_success_url(self):
        if "popup" in self.request.get_full_path():
            return reverse(
                "touglates:popup_closer",
                kwargs={
                    "pk": self.object.pk,
                    "app_name": "sdc_people",
                    "model_name": "Meetingtype",
                },
            )
        return reverse_lazy(
            "sdc_people:subcommitteetype-detail", kwargs={"pk": self.object.pk}
        )


class MeetingtypeDetail(PermissionRequiredMixin, DetailView):
    permission_required = "sdc_people.view_subcommitteetype"
    model = Meetingtype
    template_name = "sdc_people/district_detail.html"


class SubcommitteeCreate(PermissionRequiredMixin, CreateView):
    permission_required = "sdc_people.add_subcommittee"
    model = Subcommittee
    form_class = SubcommitteeForm
    template_name = "sdc_people/subcommittee_add.html"

    def get_success_url(self):
        if "popup" in self.request.get_full_path():
            return reverse(
                "touglates:popup_closer",
                kwargs={
                    "pk": self.object.pk,
                    "app_name": "sdc_people",
                    "model_name": "Subcommittee",
                },
            )
        return reverse_lazy(
            "sdc_people:subcommittee-detail", kwargs={"pk": self.object.pk}
        )


class SubcommitteeDetail(PermissionRequiredMixin, DetailView):
    permission_required = "sdc_people.view_subcommittee"
    model = Subcommittee
    template_name = "sdc_people/district_detail.html"


class SubcommitteetypeCreate(PermissionRequiredMixin, CreateView):
    permission_required = "sdc_people.add_subcommitteetype"
    model = Subcommitteetype
    form_class = SubcommitteetypeForm
    template_name = "sdc_people/subcommitteetype_add.html"

    def get_success_url(self):
        if "popup" in self.request.get_full_path():
            return reverse(
                "touglates:popup_closer",
                kwargs={
                    "pk": self.object.pk,
                    "app_name": "sdc_people",
                    "model_name": "Subcommitteetype",
                },
            )
        return reverse_lazy(
            "sdc_people:subcommitteetype-detail", kwargs={"pk": self.object.pk}
        )


class SubcommitteetypeDetail(PermissionRequiredMixin, DetailView):
    permission_required = "sdc_people.view_subcommitteetype"
    model = Subcommitteetype
    template_name = "sdc_people/district_detail.html"


class SubpositionCreate(PermissionRequiredMixin, CreateView):
    permission_required = "sdc_people.add_subposition"
    model = Subposition
    form_class = SubpositionForm
    template_name = "sdc_people/subposition_add.html"

    def get_success_url(self):
        if "popup" in self.request.get_full_path():
            return reverse(
                "touglates:popup_closer",
                kwargs={
                    "pk": self.object.pk,
                    "app_name": "sdc_people",
                    "model_name": "Subposition",
                },
            )
        return reverse_lazy(
            "sdc_people:subposition-detail", kwargs={"pk": self.object.pk}
        )


class SubpositionDetail(PermissionRequiredMixin, DetailView):
    permission_required = "sdc_people.view_subposition"
    model = Subposition
    template_name = "sdc_people/district_detail.html"
