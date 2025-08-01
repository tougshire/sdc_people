from django.contrib import admin
from django.contrib.admin.widgets import (
    RelatedFieldWidgetWrapper,
    FilteredSelectMultiple,
)
from django.db import models
from django import forms
from .models import (
    Attendance,
    DistrictBorough,
    DistrictCongress,
    DistrictMagisterial,
    DistrictPrecinct,
    DistrictStatehouse,
    DistrictStatesenate,
    Linkexternal,
    Linkexternaltype,
    Image,
    Imagetype,
    Personnote,
    Personnotetype,
    Meeting,
    Meetingtype,
    Membershipclass,
    Person,
    Subcommittee,
    Subcommitteetype,
    Submembership,
    Subposition,
)


class AttendanceInlineForm(forms.ModelForm):
    model = Attendance


class ImageInlineForm(forms.ModelForm):
    model = Image
    select_type = forms.ModelChoiceField(
        Imagetype.objects,
        required=False,
        help_text="Select a type already in the system, or type a new type in the Name field",
    )


class LinkexternalInlineForm(forms.ModelForm):
    model = Linkexternal
    select_type = forms.ModelChoiceField(
        Linkexternaltype.objects,
        required=False,
        help_text="Select a type already in the system, or type a new type in the Name field",
    )


class PersonnoteInlineForm(forms.ModelForm):
    model = Personnote
    select_type = forms.ModelChoiceField(
        Linkexternaltype.objects,
        required=False,
        help_text="Select a type already in the system, or type a new type in the Name field",
    )


class PersonModelForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name in [
            "districtprecinct",
            "districtmagisterial",
            "districtborough",
            "districtstatehouse",
            "districtstatesenate",
            "districtcongress",
            "membershipclass",
        ]:
            self.fields[field_name].widget.can_add_related = True
            self.fields[field_name].widget.can_change_related = False
            self.fields[field_name].widget.can_delete_related = False
            self.fields[field_name].widget.can_view_related = False

    class Meta:
        model = Person
        fields = [
            "name_formal",
            "name_first",
            "name_middles",
            "name_last",
            "name_friendly",
            "membershipclass",
            "membership_date",
            "districtprecinct",
            "districtmagisterial",
            "districtborough",
            "districtcongress",
            "districtstatesenate",
            "districtstatehouse",
            "primary_voice",
            "primary_text",
            "primary_email",
            "voting_address",
            "mailing_address",
            "application_date",
            "dues_effective_date",
            "demog_is_veteran",
        ]


class AttendanceInline(admin.TabularInline):

    model = Attendance
    extra = 0


class ImageInline(admin.TabularInline):

    model = Image
    form = ImageInlineForm

    extra = 0


class LinkexternalInline(admin.TabularInline):

    model = Linkexternal
    form = LinkexternalInlineForm
    template = "sdc_people/admin/linkexternal_inline_form.html"

    extra = 0


class MembershipclassInline(admin.TabularInline):
    model = Membershipclass
    extra = 0
    min_num = 1


class PersonnoteInline(admin.TabularInline):

    model = Personnote
    form = PersonnoteInlineForm

    extra = 0


class SubmembershipInline(admin.TabularInline):

    model = Submembership
    extra = 0


class AttendanceAdmin(admin.ModelAdmin):
    pass


class DistrictMagisterialAdmin(admin.ModelAdmin):
    pass


class DistrictPrecinctAdmin(admin.ModelAdmin):
    pass


class DistrictBoroughAdmin(admin.ModelAdmin):
    pass


class DistrictStatesenateAdmin(admin.ModelAdmin):
    pass


class DistrictStatehouseAdmin(admin.ModelAdmin):
    pass


class DistrictCongressAdmin(admin.ModelAdmin):
    pass


class ImageAdmin(admin.ModelAdmin):
    pass


class ImagetypeAdmin(admin.ModelAdmin):
    pass


class LinkexternalAdmin(admin.ModelAdmin):
    pass


class LinkexternaltypeAdmin(admin.ModelAdmin):
    pass


class MeetingAdmin(admin.ModelAdmin):
    pass


class MeetingtypeAdmin(admin.ModelAdmin):
    pass


class MembershipclassAdmin(admin.ModelAdmin):

    list_display = ["name", "is_member", "is_quorum_member", "is_participant"]


class PersonAdmin(admin.ModelAdmin):
    @admin.display(description="positionlist")
    def submembershiplist(self, obj):
        return ",".join(
            [
                submembership.subposition.__str__()
                for submembership in obj.submembership_set.all()
            ]
        )

    list_display = ["__str__", "membershipclass", "submembershiplist"]
    inlines = [SubmembershipInline, ImageInline, LinkexternalInline, AttendanceInline]
    form = PersonModelForm
    add_form_template = "sdc_people/admin/person_change_form.html"
    change_form_template = "sdc_people/admin/person_change_form.html"


class PersonnoteAdmin(admin.ModelAdmin):
    pass


class PersonnotetypeAdmin(admin.ModelAdmin):
    pass


class SubcommitteetypeAdmin(admin.ModelAdmin):
    pass


class SubcommitteeAdmin(admin.ModelAdmin):
    pass


class SubpositionAdmin(admin.ModelAdmin):
    pass


class SubmembershipAdmin(admin.ModelAdmin):
    pass


admin.site.register(Attendance, AttendanceAdmin)

admin.site.register(DistrictMagisterial, DistrictMagisterialAdmin)

admin.site.register(DistrictPrecinct, DistrictPrecinctAdmin)

admin.site.register(DistrictBorough, DistrictBoroughAdmin)

admin.site.register(DistrictStatesenate, DistrictStatesenateAdmin)

admin.site.register(DistrictStatehouse, DistrictStatehouseAdmin)

admin.site.register(DistrictCongress, DistrictCongressAdmin)

admin.site.register(Image, ImageAdmin)

admin.site.register(Imagetype, ImagetypeAdmin)

admin.site.register(Linkexternal, LinkexternalAdmin)

admin.site.register(Linkexternaltype, LinkexternaltypeAdmin)

admin.site.register(Meeting, MeetingAdmin)

admin.site.register(Meetingtype, MeetingtypeAdmin)

admin.site.register(Membershipclass, MembershipclassAdmin)

admin.site.register(Person, PersonAdmin)

admin.site.register(Personnote, PersonnoteAdmin)

admin.site.register(Personnotetype, PersonnotetypeAdmin)

admin.site.register(Subcommitteetype, SubcommitteetypeAdmin)

admin.site.register(Subcommittee, SubcommitteeAdmin)

admin.site.register(Subposition, SubpositionAdmin)

admin.site.register(Submembership, SubmembershipAdmin)
