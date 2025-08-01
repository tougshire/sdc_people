from django.urls import path, reverse_lazy
from django.views.generic.base import RedirectView

from . import views

app_name = "sdc_people"

urlpatterns = [
    path("", RedirectView.as_view(url=reverse_lazy("sdc_people:person-list"))),
    path("person/", RedirectView.as_view(url=reverse_lazy("sdc_people:person-list"))),
    path("person/detail/<int:pk>/", views.PersonDetail.as_view(), name="person-detail"),
    path("person/delete/<int:pk>/", views.PersonDelete.as_view(), name="person-delete"),
    path("person/update/<int:pk>/", views.PersonUpdate.as_view(), name="person-update"),
    path(
        "person/list/filterstore/<int:from_store>/",
        views.PersonList.as_view(),
        name="person-filterstore",
    ),
    path(
        "person/list/",
        views.PersonList.as_view(),
        name="person-list",
    ),
    path(
        "person/csv/",
        views.PersonCSV.as_view(),
        name="person-csv",
    ),
    path("person/create/", views.PersonCreate.as_view(), name="person-create"),
    path("person/popup/", views.PersonCreate.as_view(), name="person-popup"),
    path("person/emails/", views.popup_email_list, name="email-js-popup"),
    path(
        "membershipclass/",
        RedirectView.as_view(url=reverse_lazy("sdc_people:membershipclass-list")),
    ),
    path(
        "membershipclass/detail/<int:pk>/",
        views.MembershipclassDetail.as_view(),
        name="membershipclass-detail",
    ),
    path(
        "personnote/",
        RedirectView.as_view(url=reverse_lazy("sdc_people:personnote-list")),
    ),
    path(
        "personnote/detail/<int:pk>/",
        views.PersonnoteDetail.as_view(),
        name="personnote-detail",
    ),
    path(
        "personnote/delete/<int:pk>/",
        views.PersonnoteDelete.as_view(),
        name="personnote-delete",
    ),
    path(
        "personnote/update/<int:pk>/",
        views.PersonnoteUpdate.as_view(),
        name="personnote-update",
    ),
    path(
        "personnote/list/filterstore/<int:from_store>/",
        views.PersonnoteList.as_view(),
        name="personnote-filterstore",
    ),
    path(
        "personnote/list/",
        views.PersonnoteList.as_view(),
        name="personnote-list",
    ),
    path(
        "personnote/create/",
        views.PersonnoteCreate.as_view(),
        name="personnote-create",
    ),
    path(
        "personnote/popup/",
        views.PersonnoteCreate.as_view(),
        name="personnote-popup",
    ),
    path(
        "membershipclass/delete/<int:pk>/",
        views.MembershipclassDelete.as_view(),
        name="membershipclass-delete",
    ),
    path(
        "membershipclass/update/<int:pk>/",
        views.MembershipclassUpdate.as_view(),
        name="membershipclass-update",
    ),
    path(
        "membershipclass/list/filterstore/<int:from_store>/",
        views.MembershipclassList.as_view(),
        name="membershipclass-filterstore",
    ),
    path(
        "membershipclass/list/",
        views.MembershipclassList.as_view(),
        name="membershipclass-list",
    ),
    path(
        "membershipclass/create/",
        views.MembershipclassCreate.as_view(),
        name="membershipclass-create",
    ),
    path(
        "membershipclass/popup/",
        views.MembershipclassCreate.as_view(),
        name="membershipclass-popup",
    ),
    path(
        "borough/detail/<int:pk>/",
        views.DistrictBoroughDetail.as_view(),
        name="districtborough-detail",
    ),
    path(
        "borough/create/",
        views.DistrictBoroughCreate.as_view(),
        name="districtborough-create",
    ),
    path(
        "borough/popup/",
        views.DistrictBoroughCreate.as_view(),
        name="districtborough-popup",
    ),
    path(
        "precinct/update/",
        views.DistrictPrecinctCreate.as_view(),
        name="districtprecinct-create",
    ),
    path(
        "precinct/popup/",
        views.DistrictPrecinctCreate.as_view(),
        name="districtprecinct-popup",
    ),
    path(
        "precinct/detail/<int:pk>/",
        views.DistrictPrecinctDetail.as_view(),
        name="districtprecinct-detail",
    ),
    path(
        "magisterial/update/",
        views.DistrictMagisterialCreate.as_view(),
        name="districtmagisterial-create",
    ),
    path(
        "magisterial/popup/",
        views.DistrictMagisterialCreate.as_view(),
        name="districtmagisterial-popup",
    ),
    path(
        "magisterial/detail/<int:pk>/",
        views.DistrictMagisterialDetail.as_view(),
        name="districtmagisterial-detail",
    ),
    path(
        "statehouse/update/",
        views.DistrictStatehouseCreate.as_view(),
        name="districtstatehouse-create",
    ),
    path(
        "statehouse/popup/",
        views.DistrictStatehouseCreate.as_view(),
        name="districtstatehouse-popup",
    ),
    path(
        "statehouse/detail/<int:pk>/",
        views.DistrictStatehouseDetail.as_view(),
        name="districtstatehouse-detail",
    ),
    path(
        "statesenate/update/",
        views.DistrictStatesenateCreate.as_view(),
        name="districtstatesenate-create",
    ),
    path(
        "statesenate/popup/",
        views.DistrictStatesenateCreate.as_view(),
        name="districtstatesenate-popup",
    ),
    path(
        "statesenate/detail/<int:pk>/",
        views.DistrictStatesenateDetail.as_view(),
        name="districtstatesenate-detail",
    ),
    path(
        "congress/update/",
        views.DistrictCongressCreate.as_view(),
        name="districtcongress-create",
    ),
    path(
        "congress/popup/",
        views.DistrictCongressCreate.as_view(),
        name="districtcongress-popup",
    ),
    path(
        "congress/detail/<int:pk>/",
        views.DistrictCongressDetail.as_view(),
        name="districtcongress-detail",
    ),
    path(
        "position/create/",
        views.SubpositionCreate.as_view(),
        name="subposition-create",
    ),
    path(
        "position/popup/",
        views.SubpositionCreate.as_view(),
        name="subposition-popup",
    ),
    path(
        "position/detail/<int:pk>/",
        views.SubpositionDetail.as_view(),
        name="subposition-detail",
    ),
    path(
        "committee/list/",
        views.SubcommitteeList.as_view(),
        name="subcommittee-list",
    ),
    path(
        "committee/create/",
        views.SubcommitteeCreate.as_view(),
        name="subcommittee-create",
    ),
    path(
        "committee/update/<int:pk>/",
        views.SubcommitteeUpdate.as_view(),
        name="subcommittee-update",
    ),
    path(
        "committee/popup/",
        views.SubcommitteeCreate.as_view(),
        name="subcommittee-popup",
    ),
    path(
        "committee/detail/<int:pk>/",
        views.SubcommitteeDetail.as_view(),
        name="subcommittee-detail",
    ),
    path(
        "committeetype/update/",
        views.SubcommitteetypeCreate.as_view(),
        name="subcommitteetype-create",
    ),
    path(
        "committeetype/popup/",
        views.SubcommitteetypeCreate.as_view(),
        name="subcommitteetype-popup",
    ),
    path(
        "committeetype/detail/<int:pk>/",
        views.SubcommitteetypeDetail.as_view(),
        name="subcommitteetype-detail",
    ),
    path(
        "meeting/update/",
        views.MeetingCreate.as_view(),
        name="meeting-create",
    ),
    path(
        "meeting/popup/",
        views.MeetingCreate.as_view(),
        name="meeting-popup",
    ),
    path(
        "meeting/update/<int:pk>/",
        views.MeetingUpdate.as_view(),
        name="meeting-update",
    ),
    path(
        "meeting/detail/<int:pk>/",
        views.MeetingDetail.as_view(),
        name="meeting-detail",
    ),
    path(
        "meeting/delete/<int:pk>/",
        views.MeetingDelete.as_view(),
        name="meeting-delete",
    ),
    path(
        "meeting/list/",
        views.MeetingList.as_view(),
        name="meeting-list",
    ),
    path(
        "meetingtype/update/",
        views.MeetingtypeCreate.as_view(),
        name="meetingtype-create",
    ),
    path(
        "meetingtype/popup/",
        views.MeetingtypeCreate.as_view(),
        name="meetingtype-popup",
    ),
    path(
        "meetingtype/detail/<int:pk>/",
        views.MeetingtypeDetail.as_view(),
        name="meetingtype-detail",
    ),
    path("due/create/", views.DueCreate.as_view(), name="due-create"),
    path(
        "due/update/<int:pk>/",
        views.DueUpdate.as_view(),
        name="due-update",
    ),
    path(
        "due/detail/<int:pk>/",
        views.DueDetail.as_view(),
        name="due-detail",
    ),

]
