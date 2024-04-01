from django.conf import settings
from django.conf.urls.static import static
from django.http import HttpResponse
from django.views.generic.base import RedirectView
from django.urls import path, reverse_lazy
from . import filterset, views

app_name = "sdc_people"

urlpatterns = [
    path("", RedirectView.as_view(url=reverse_lazy("sdc_people:person-list"))),
    path("person/", RedirectView.as_view(url=reverse_lazy("sdc_people:person-list"))),
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
    path("person/detail/<int:pk>/", views.PersonDetail.as_view(), name="person-detail"),
    path("person/change/<int:pk>/", views.PersonUpdate.as_view(), name="person-update"),
    path("person/add/", views.PersonCreate.as_view(), name="person-create"),
    path(
        "borough/add/",
        views.DistrictBoroughCreate.as_view(),
        name="districtborough-create",
    ),
    path(
        "borough/popup/",
        views.DistrictBoroughCreate.as_view(),
        name="districtborough-popup",
    ),
    path(
        "borough/detail/<int:pk>/",
        views.DistrictBoroughDetail.as_view(),
        name="districtborough-detail",
    ),
    path(
        "precinct/add/",
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
        "magisterial/add/",
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
        "statehouse/add/",
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
        "statesenate/add/",
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
        "congress/add/",
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
        "position/add/",
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
        "committee/add/",
        views.SubcommitteeCreate.as_view(),
        name="subcommittee-create",
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
        "committeetype/add/",
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
        "meeting/add/",
        views.MeetingCreate.as_view(),
        name="submeeting-create",
    ),
    path(
        "meeting/popup/",
        views.MeetingCreate.as_view(),
        name="submeeting-popup",
    ),
    path(
        "meeting/detail/<int:pk>/",
        views.MeetingDetail.as_view(),
        name="submeeting-detail",
    ),
    path(
        "meetingtype/add/",
        views.MeetingtypeCreate.as_view(),
        name="submeetingtype-create",
    ),
    path(
        "meetingtype/popup/",
        views.MeetingtypeCreate.as_view(),
        name="submeetingtype-popup",
    ),
    path(
        "meetingtype/detail/<int:pk>/",
        views.MeetingtypeDetail.as_view(),
        name="submeetingtype-detail",
    ),
]
