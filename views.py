import csv
import logging
from django.shortcuts import render
from django.urls import reverse, reverse_lazy, resolve

from django_filters_stoex.forms import (
    FilterstoreRetrieveForm,
    FilterstoreSaveForm,
)
from django_filters_stoex.views import FilterView
from sdc_people.filterset import MeetingFilter, PersonFilter
from .models import (
    DistrictBorough,
    DistrictCongress,
    DistrictMagisterial,
    DistrictPrecinct,
    DistrictStatehouse,
    DistrictStatesenate,
    Meeting,
    Meetingtype,
    Membershipclass,
    Person,
    Personnote,
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
    MeetingAttendanceFormset,
    MeetingForm,
    MeetingtypeForm,
    MembershipclassForm,
    PersonAttendanceFormset,
    PersonForm,
    PersonImageFormset,
    PersonLinkexternalFormset,
    PersonnoteForm,
    PersonpersonnoteFormset,
    PersonsubmembershipFormset,
    SubcommitteeForm,
    SubcommitteetypeForm,
    SubpositionForm,
    CSVOptionForm,
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
from django.http import HttpResponse, HttpResponseRedirect, QueryDict
from urllib.parse import urlencode
from django.core.exceptions import FieldError

logger = logging.getLogger(__name__)


class PersonDelete(PermissionRequiredMixin, DeleteView):
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

    def get_success_url(self):
        return reverse_lazy("sdc_people:person-list")


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


class PersonUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = "sdc_people.change_Person"
    model = Person
    form_class = PersonForm
    template_name = "sdc_people/person_update.html"

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)

        formsetclasses = {
            "images": PersonImageFormset,
            "linkexternals": PersonLinkexternalFormset,
            "submemberships": PersonsubmembershipFormset,
            "attendances": PersonAttendanceFormset,
            "personnotes": PersonpersonnoteFormset,
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

        self.object = form.save(commit=False)

        formsetclasses = {
            "images": PersonImageFormset,
            "linkexternals": PersonLinkexternalFormset,
            "submemberships": PersonsubmembershipFormset,
            "attendances": PersonAttendanceFormset,
            "personnotes": PersonpersonnoteFormset,
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
                # special processing for individual formset classes
                if formsetkey == "personnotes":
                    for form in formsetdata[formsetkey].forms:
                        if form.has_changed():
                            form_uncommitted = form.save(commit=False)
                            if form_uncommitted.author is None:
                                form_uncommitted.author = self.request.user
                                # form_uncommitted.save()
                formsetdata[formsetkey].save()
            else:
                logger.critical(formsetdata[formsetkey].errors)
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


class PersonList(PermissionRequiredMixin, FilterView):

    permission_required = "sdc_people.view_person"
    filterset_class = PersonFilter
    filterstore_urlname = "sdc_people:person-filterstore"

    def get_context_data(self, *args, **kwargs):

        context_data = super().get_context_data(*args, **kwargs)

        context_data["person_labels"] = {
            field.name: field.verbose_name.title()
            for field in Person._meta.get_fields()
            if type(field).__name__[-3:] != "Rel"
        }
        context_data["filterstore_retrieve"] = FilterstoreRetrieveForm(
            request=self.request, app_name="sdc_people", model_name="person"
        )
        context_data["filterstore_save"] = FilterstoreSaveForm()
        context_data["csv_form"] = CSVOptionForm()
        context_data["make_csv"] = self.request.POST.get("make_csv", None)
        context_data["count"] = context_data["filter"].qs.count()
        return context_data


class PersonCreate(PermissionRequiredMixin, CreateView):
    permission_required = "sdc_people.add_Person"
    model = Person
    form_class = PersonForm
    template_name = "sdc_people/person_create.html"

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)

        formsetclasses = {
            "images": PersonImageFormset,
            "linkexternals": PersonLinkexternalFormset,
            "submemberships": PersonsubmembershipFormset,
            "attendances": PersonAttendanceFormset,
            "personnotes": PersonpersonnoteFormset,
        }

        initials = {"personnotes": {"author": self.request.user}}

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
            "personnotes": PersonpersonnoteFormset,
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


class PersonCSV(PermissionRequiredMixin, FilterView):

    permission_required = "sdc_people.view_person"
    filterset_class = PersonFilter
    # filterstore_urlname = "sdc_people:person-filterstore"
    template_name = "sdc_people/csv.txt"
    content_type = "text/csv"
    headers = {"Content-Disposition": 'attachment; filename="sdc_people.csv"'}

    def dispatch(self, *args, **kwargs):
        response = super().dispatch(*args, **kwargs)
        response.headers = {
            "Content-Disposition": 'attachment; filename="sdc_people.csv"'
        }
        return response

    def get_context_data(self, *args, **kwargs):

        context_data = super().get_context_data(*args, **kwargs)

        data = []
        for person in context_data["filter"].qs:
            data.append(
                [
                    person.name_formal,
                    person.primary_email,
                ]
            )
        context_data["data"] = data
        return context_data


class MembershipclassDelete(PermissionRequiredMixin, DeleteView):
    permission_required = "sdc_people.view_membershipclass"
    model = Membershipclass

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)

        context_data["membershipclass_labels"] = {
            field.name: field.verbose_name.title()
            for field in Membershipclass._meta.get_fields()
            if type(field).__name__[-3:] != "Rel"
        }

        return context_data


class MembershipclassDetail(PermissionRequiredMixin, DetailView):
    permission_required = "sdc_people.view_membershipclass"
    model = Membershipclass

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)

        context_data["membershipclass_labels"] = {
            field.name: field.verbose_name.title()
            for field in Membershipclass._meta.get_fields()
            if type(field).__name__[-3:] != "Rel"
        }

        return context_data


class MembershipclassUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = "sdc_people.change_Membershipclass"
    model = Membershipclass
    form_class = MembershipclassForm
    template_name = "sdc_people/membershipclass_update.html"

    def get_success_url(self):
        if "popup" in self.request.get_full_path():
            return reverse(
                "touglates:popup_closer",
                kwargs={
                    "pk": self.object.pk,
                    "app_name": "sdc_people",
                    "model_name": "Membershipclass",
                },
            )
        return reverse_lazy(
            "sdc_people:membershipclass-detail", kwargs={"pk": self.object.pk}
        )


class MembershipclassList(PermissionRequiredMixin, ListView):
    model = Membershipclass
    permission_required = "sdc_people.view_membershipclass"

    def get_context_data(self, *args, **kwargs):

        context_data = super().get_context_data(*args, **kwargs)

        context_data["membershipclass_labels"] = {
            field.name: field.verbose_name.title()
            for field in Membershipclass._meta.get_fields()
            if type(field).__name__[-3:] != "Rel"
        }
        return context_data


class MembershipclassCreate(PermissionRequiredMixin, CreateView):
    permission_required = "sdc_people.add_Membershipclass"
    model = Membershipclass
    form_class = MembershipclassForm
    template_name = "sdc_people/membershipclass_create.html"

    def get_success_url(self):

        if "popup" in self.request.get_full_path():
            return reverse(
                "touglates:popup_closer",
                kwargs={
                    "pk": self.object.pk,
                    "app_name": "sdc_people",
                    "model_name": "Membershipclass",
                },
            )
        return reverse_lazy(
            "sdc_people:membershipclass-detail", kwargs={"pk": self.object.pk}
        )


class PersonnoteDelete(PermissionRequiredMixin, DeleteView):
    permission_required = "sdc_people.view_personnote"
    model = Personnote

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)

        context_data["personnote_labels"] = {
            field.name: field.verbose_name.title()
            for field in Personnote._meta.get_fields()
            if type(field).__name__[-3:] != "Rel"
        }

        return context_data


class PersonnoteDetail(PermissionRequiredMixin, DetailView):
    permission_required = "sdc_people.view_personnote"
    model = Personnote

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)

        context_data["personnote_labels"] = {
            field.name: field.verbose_name.title()
            for field in Personnote._meta.get_fields()
            if type(field).__name__[-3:] != "Rel"
        }

        return context_data


class PersonnoteUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = "sdc_people.change_Personnote"
    model = Personnote
    form_class = PersonnoteForm
    template_name = "sdc_people/personnote_update.html"

    def get_success_url(self):
        if "popup" in self.request.get_full_path():
            return reverse(
                "touglates:popup_closer",
                kwargs={
                    "pk": self.object.pk,
                    "app_name": "sdc_people",
                    "model_name": "Personnote",
                },
            )
        return reverse_lazy(
            "sdc_people:personnote-detail", kwargs={"pk": self.object.pk}
        )


class PersonnoteList(PermissionRequiredMixin, ListView):
    model = Personnote
    permission_required = "sdc_people.view_personnote"

    def get_context_data(self, *args, **kwargs):

        context_data = super().get_context_data(*args, **kwargs)

        context_data["personnote_labels"] = {
            field.name: field.verbose_name.title()
            for field in Personnote._meta.get_fields()
            if type(field).__name__[-3:] != "Rel"
        }
        return context_data


class PersonnoteCreate(PermissionRequiredMixin, CreateView):
    permission_required = "sdc_people.add_Personnote"
    model = Personnote
    form_class = PersonnoteForm
    template_name = "sdc_people/personnote_create.html"

    def get_success_url(self):

        if "popup" in self.request.get_full_path():
            return reverse(
                "touglates:popup_closer",
                kwargs={
                    "pk": self.object.pk,
                    "app_name": "sdc_people",
                    "model_name": "Personnote",
                },
            )
        return reverse_lazy(
            "sdc_people:personnote-detail", kwargs={"pk": self.object.pk}
        )


class DistrictBoroughCreate(PermissionRequiredMixin, CreateView):
    permission_required = "sdc_people.add_districtborough"
    model = DistrictBorough
    form_class = DistrictBoroughForm
    template_name = "sdc_people/district_create.html"

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
    template_name = "sdc_people/district_create.html"

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
    template_name = "sdc_people/district_create.html"

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
    template_name = "sdc_people/district_create.html"

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
    template_name = "sdc_people/district_create.html"

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
    template_name = "sdc_people/district_create.html"

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
    permission_required = "sdc_people.add_meeting"
    model = Meeting
    form_class = MeetingForm
    template_name = "sdc_people/meeting_create.html"

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)

        formsetclasses = {
            "attendees": MeetingAttendanceFormset,
        }

        for formsetkey, formsetclass in formsetclasses.items():
            if self.request.POST:
                context_data[formsetkey] = formsetclass(self.request.POST)
            else:
                context_data[formsetkey] = formsetclass()

        return context_data

    def form_valid(self, form):
        response = super().form_valid(form)

        self.object = form.save(commit=False)

        formsetclasses = {
            "attendees": MeetingAttendanceFormset,
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
                    "model_name": "Meeting",
                },
            )
        return reverse_lazy("sdc_people:meeting-detail", kwargs={"pk": self.object.pk})


class MeetingUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = "sdc_people.add_meeting"
    model = Meeting
    form_class = MeetingForm
    template_name = "sdc_people/meeting_update.html"

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)

        formsetclasses = {
            "attendees": MeetingAttendanceFormset,
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

        self.object = form.save(commit=False)

        formsetclasses = {
            "attendees": MeetingAttendanceFormset,
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
                    "model_name": "Meeting",
                },
            )
        return reverse_lazy("sdc_people:meeting-detail", kwargs={"pk": self.object.pk})


class MeetingDetail(PermissionRequiredMixin, DetailView):
    permission_required = "sdc_people.view_meeting"
    model = Meeting
    template_name = "sdc_people/meeting_detail.html"


class MeetingList(PermissionRequiredMixin, FilterView):

    permission_required = "sdc_people.view_meeting"
    filterset_class = MeetingFilter
    filterstore_urlname = "sdc_people:meeting-filterstore"

    def get_context_data(self, *args, **kwargs):

        context_data = super().get_context_data(*args, **kwargs)

        context_data["filterstore_retrieve"] = FilterstoreRetrieveForm()
        context_data["filterstore_save"] = FilterstoreSaveForm()

        context_data["meeting_labels"] = {
            field.name: field.verbose_name.title()
            for field in Meeting._meta.get_fields()
            if type(field).__name__[-3:] != "Rel"
        }

        context_data["count"] = self.object_list.count()
        return context_data


class MeetingtypeCreate(PermissionRequiredMixin, CreateView):
    permission_required = "sdc_people.add_meetingtype"
    model = Meetingtype
    form_class = MeetingtypeForm
    template_name = "sdc_people/meetingtype_create.html"

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
            "sdc_people:meetingtype-detail", kwargs={"pk": self.object.pk}
        )


class MeetingtypeDetail(PermissionRequiredMixin, DetailView):
    permission_required = "sdc_people.view_meetingtype"
    model = Meetingtype
    template_name = "sdc_people/meeting_detail.html"


class SubcommitteeCreate(PermissionRequiredMixin, CreateView):
    permission_required = "sdc_people.add_subcommittee"
    model = Subcommittee
    form_class = SubcommitteeForm
    template_name = "sdc_people/subcommittee_create.html"

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
    template_name = "sdc_people/subcommitteetype_create.html"

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
    template_name = "sdc_people/subposition_create.html"

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
