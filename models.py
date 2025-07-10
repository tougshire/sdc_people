from datetime import date
import uuid

from django.conf import settings
from django.db import models
from django.utils import timezone

ORDINAL_FIRST = 1
ORDINAL_MEDIUM = 5
ORDINAL_CHOICES = [
    (1, "First"),
    (2, "Second"),
    (3, "Third"),
    (4, "Before Medium"),
    (5, "Medium"),
    (6, "After Medium"),
    (7, "Third Last"),
    (8, "Second Last"),
    (9, "Last"),
]
PRIORITY_HIGHEST = 1
PRIORITY_MEDIUM = 5
PRIORITY_CHOICES = [
    (1, "Highest"),
    (2, "Very High"),
    (3, "High"),
    (4, "Above Medium"),
    (5, "Medium"),
    (6, "Below Medium"),
    (7, "Low"),
    (8, "Second Lowest"),
    (9, "Lowest"),
]


class Subcommitteetype(models.Model):
    name = models.CharField("name", max_length=50, help_text="The name of the type,")
    ordinal = models.IntegerField(
        "ordinal",
        choices=ORDINAL_CHOICES,
        default=ORDINAL_MEDIUM,
        help_text="A number assigned for sorting, with lowest number first",
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "subcommittee type"
        ordering = ("ordinal", "name")


class Subcommittee(models.Model):
    name = models.CharField(
        "name", max_length=50, help_text="The name of the subcommittee,"
    )
    subcommitteetype = models.ForeignKey(
        Subcommitteetype,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        help_text="The type of submcommittee",
    )

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        saved = super().save(*args, **kwargs)
        memberposition, created = Subposition.objects.get_or_create(
            subcommittee=self, name="Member"
        )

    class Meta:
        verbose_name = "subcommittee"
        ordering = ("subcommitteetype", "name")


class Subposition(models.Model):
    subcommittee = models.ForeignKey(
        Subcommittee,
        on_delete=models.CASCADE,
        help_text="The subcommittee to which this title is attached",
    )
    name = models.CharField(
        "name", max_length=50, help_text="The name of the position,"
    )

    ordinal = models.IntegerField(
        "ordinal",
        choices=ORDINAL_CHOICES,
        default=ORDINAL_MEDIUM,
        help_text="A number assigned for sorting",
    )
    display_format = models.CharField(
        max_length=60,
        default="{position} {committee}",
    )

    def __str__(self):
        try:
            return self.display_format.format(
                position=self.name, committee=self.subcommittee.name
            )
        except:
            return "{} {}".format(self.name, self.subcommittee)

    class Meta:
        verbose_name = "Position"
        ordering = ("subcommittee", "ordinal", "name")


class Membershipclass(models.Model):
    MEMBERSHIP_NO = 0
    MEMBERSHIP_PROSPECTIVE = 11
    MEMBERSHIP_PENDING = 12
    MEMBERSHIP_YES = 111

    name = models.CharField(
        "name", max_length=50, help_text="The name of the membership class,"
    )
    is_member = models.IntegerField(
        "is member",
        choices=(
            (MEMBERSHIP_NO, "no"),
            (MEMBERSHIP_PENDING, "prospective"),
            (MEMBERSHIP_PENDING, "pending"),
            (MEMBERSHIP_YES, "yes"),
        ),
        default=MEMBERSHIP_NO,
        help_text="If a person of this class is considered a member of the committee",
    )
    is_quorum_member = models.IntegerField(
        "is quorum member",
        choices=(
            (MEMBERSHIP_NO, "no"),
            (MEMBERSHIP_PENDING, "pending"),
            (MEMBERSHIP_YES, "yes"),
        ),
        default=MEMBERSHIP_NO,
        help_text="If a person of this class can be part of a quorum",
    )
    is_participant = models.IntegerField(
        "is a participant",
        choices=(
            (MEMBERSHIP_NO, "no"),
            (MEMBERSHIP_YES, "yes"),
        ),
        default=MEMBERSHIP_NO,
        help_text="If a person of this class participates and has interest in the committee - attends meetings, volunteers, etc..",
    )

    ordinal = models.IntegerField(
        "ordinal",
        choices=ORDINAL_CHOICES,
        default=ORDINAL_MEDIUM,
        help_text="A number assigned for sorting, with lowest number first",
    )

    def get_is_quorum_member_yesno(self):
        try:
            return "yes" if self.is_quorum_member == self.MEMBERSHIP_YES else "no"
        except:
            return "no"

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "membership class"
        ordering = (
            "ordinal",
            "is_member",
            "is_quorum_member",
            "name",
        )


class DistrictMagisterial(models.Model):
    number = models.CharField(
        "number",
        max_length=5,
        blank=True,
        help_text='The number of the district.  This can include letters (ex "11a").  Precede with "0"\'s as necessary to maintain sort order',
    )

    name = models.CharField(
        "name",
        max_length=50,
        blank=True,
        help_text="The name of the district",
    )

    def __str__(self):
        return (self.number + " " + self.name).strip()

    class Meta:
        verbose_name = "magisterial district"
        ordering = (
            "number",
            "name",
        )


class DistrictPrecinct(models.Model):
    number = models.CharField(
        "number",
        max_length=5,
        blank=True,
        help_text='The number of the district.  This can include letters (ex "11a").  Precede with "0"\'s as necessary to maintain sort order',
    )

    name = models.CharField(
        "name",
        max_length=50,
        blank=True,
        help_text="The name of the district, which may be numeric",
    )

    def __str__(self):
        return (self.number + " " + self.name).strip()

    class Meta:
        verbose_name = "precinct"
        ordering = (
            "number",
            "name",
        )


class DistrictBorough(models.Model):
    number = models.CharField(
        "number",
        max_length=5,
        blank=True,
        help_text='The number of the district.  This can include letters (ex "11a").  Precede with "0"\'s as necessary to maintain sort order',
    )

    name = models.CharField(
        "name",
        max_length=50,
        blank=True,
        help_text="The name of the borough, which may be numeric",
    )

    def __str__(self):
        return (self.number + " " + self.name).strip()

    class Meta:
        verbose_name = "borough"
        ordering = (
            "number",
            "name",
        )


class DistrictStatesenate(models.Model):
    number = models.CharField(
        "number",
        max_length=5,
        blank=True,
        help_text='The number of the district.  This can include letters (ex "11a").  Precede with "0"\'s as necessary to maintain sort order',
    )

    name = models.CharField(
        "name",
        max_length=5,
        blank=True,
        help_text="The number of the state senate district",
    )

    def __str__(self):
        return (self.number + " " + self.name).strip()

    class Meta:
        verbose_name = "state senate district"
        ordering = (
            "number",
            "name",
        )


class DistrictStatehouse(models.Model):
    number = models.CharField(
        "number",
        max_length=5,
        blank=True,
        help_text='The number of the district.  This can include letters (ex "11a").  Precede with "0"\'s as necessary to maintain sort order',
    )

    name = models.CharField(
        "name",
        max_length=5,
        blank=True,
        help_text="The number of the house of delegates district",
    )

    def __str__(self):
        return (self.number + " " + self.name).strip()

    class Meta:
        verbose_name = "house of delegates district"
        ordering = (
            "number",
            "name",
        )


class DistrictCongress(models.Model):
    number = models.CharField(
        "number",
        max_length=5,
        blank=True,
        help_text='The number of the district.  This can include letters (ex "11a").  Precede with "0"\'s as necessary to maintain sort order',
    )

    name = models.CharField(
        "name",
        max_length=5,
        blank=True,
        help_text="The number of the congressional district",
    )

    def __str__(self):
        return (self.number + " " + self.name).strip()

    class Meta:
        verbose_name = "congressional district"
        ordering = (
            "number",
            "name",
        )


class Meetingtype(models.Model):
    name = models.CharField("name", max_length=100, help_text="The name of the type")
    ordinal = models.IntegerField(
        "ordinal",
        choices=ORDINAL_CHOICES,
        default=ORDINAL_MEDIUM,
        help_text="A number assigned for sorting, with lowest number first",
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = (
            "ordinal",
            "name",
        )


class Meeting(models.Model):
    meetingtype = models.ForeignKey(
        Meetingtype,
        on_delete=models.SET_NULL,
        null=True,
        help_text="The type of meeting",
    )
    when_held = models.DateField(
        "date", default=date.today, help_text="The date of the meeting"
    )
    had_quorum = models.BooleanField(
        "quorum", default=True, help_text="If the meeting had a quorum"
    )

    def __str__(self):
        return "{}: {}".format(self.when_held, self.meetingtype.name)

    class Meta:
        ordering = ("-when_held", "meetingtype")


class Person(models.Model):
    name_first = models.CharField(
        "first name",
        max_length=50,
        help_text="The legal first name of the individual",
    )
    name_formal = models.CharField(
        "formal name",
        max_length=100,
        help_text="The full name of the individual including title (Mr. Ms, Dr., etc..), middle names, and suffixes, to the extent known",
    )
    name_friendly = models.CharField(
        "friendly name",
        max_length=20,
        help_text="Either the first name or a nickname that the person prefers to be addressed as in an informal setting",
    )
    name_last = models.CharField(
        "last name",
        blank=True,
        max_length=50,
        help_text="The legal last name of the individual",
    )
    name_middles = models.CharField(
        "middle names",
        max_length=100,
        help_text="The person's middle names",
    )
    primary_voice = models.CharField(
        "primary voice phone number",
        max_length=50,
        blank=True,
        help_text="The phone number to be used for voice calls",
    )
    primary_text = models.CharField(
        "primary text phone number",
        max_length=50,
        blank=True,
        help_text="The phone number to be used for text messages",
    )
    primary_email = models.EmailField(
        "primary email adddress",
        max_length=250,
        blank=True,
        help_text="The person's email address",
    )
    voting_address = models.TextField(
        "voting address", blank=True, help_text="The person's voting address"
    )
    mailing_address = models.TextField(
        "mailing address",
        blank=True,
        help_text="The person's mailing address if different from voting address",
    )
    districtprecinct = models.ForeignKey(
        DistrictPrecinct,
        verbose_name="precinct",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text="The person's voting precinct",
    )
    districtmagisterial = models.ForeignKey(
        DistrictMagisterial,
        verbose_name="magisterial district",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text="The person's magisterial district",
    )

    districtborough = models.ForeignKey(
        DistrictBorough,
        verbose_name="Borough",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text="The person's borough",
    )
    districtstatehouse = models.ForeignKey(
        DistrictStatehouse,
        verbose_name="House of Delegates District",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text="The person's House of Delegates district",
    )
    districtstatesenate = models.ForeignKey(
        DistrictStatesenate,
        verbose_name="State Senate District",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text="The person's State Senate district",
    )
    districtcongress = models.ForeignKey(
        DistrictCongress,
        verbose_name="Congressional District",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text="The person's congressional district",
    )
    membershipclass = models.ForeignKey(
        Membershipclass,
        verbose_name="membership class",
        null=True,
        on_delete=models.SET_NULL,
        help_text="The person's class of membership",
    )
    membership_date = models.DateField(
        "membership status date",
        blank=True,
        null=True,
        help_text="The date of the current class and status of membership, if applicable",
    )
    application_date = models.DateField(
        "Most Recent Application Date",
        null=True,
        blank=True,
        help_text="The date of this person's most recent membership application",
    )
    dues_effective_date = models.DateField(
        "Dues Effective Date",
        null=True,
        blank=True,
        help_text="The effective date of the most recent dues (often the date of the caucus or meeting in which the person was admitted)",
    )
    demog_is_veteran = models.BooleanField(
        "veteran", default=False, help_text="Is this person a military veteran"
    )

    def __str__(self):
        return "{} ({})".format(self.name_formal, self.name_friendly)

    def get_attendance(self):
        meetings = Meeting.objects.all()
        if hasattr(settings, "SDC_PEOPLE"):
            if "meetingtypes_for_attendance" in settings.SDC_PEOPLE:
                meetings = meetings.filter(
                    meetingtype__name__in=settings.SDC_PEOPLE[
                        "meetingtypes_for_attendance"
                    ]
                )
        attendance_binary = ""
        for meeting in meetings:
            if meeting.attendance_set.filter(person=self).exists():
                attendance_binary = attendance_binary + "Y,"
            else:
                attendance_binary = attendance_binary + "n,"
        return attendance_binary[:-1]

    def get_memberships(self):
        submemberships = []
        for submembership in self.submembership_set.all():
            submemberships.append(submembership.subposition.__str__())

        return submemberships

    def get_memberships_as_divs(self):
        return "<div>" + ("</div><div>".join(self.get_memberships())) + "</div>"

    class Meta:
        verbose_name = "Person"
        verbose_name_plural = "People"
        ordering = (
            "name_last",
            "name_friendly",
            "membershipclass",
        )


class Personnotetype(models.Model):
    name = models.CharField("name", max_length=50, help_text="The name of the type")

    def __str__(self):
        return self.name

    class Meta:
        ordering = ("name",)
        verbose_name = "Type of note"


class Personnote(models.Model):
    person = models.ForeignKey(
        Person,
        on_delete=models.CASCADE,
        help_text="The person to which this link belongs",
    )
    personnotetype = models.ForeignKey(
        Personnotetype,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        help_text="The name of the link,",
    )
    content = models.CharField(
        max_length=255, blank=True, help_text="The content of the note"
    )
    when = models.DateTimeField(
        "date", default=timezone.now, help_text="The date of the note"
    )
    is_flagged = models.BooleanField(
        "is flagged",
        default=True,
        help_text="Flagged notes display an icon in the list view and appear by default in the detail view",
    )
    expiration = models.DateField(
        "expiration date",
        null=True,
        blank=True,
        help_text="The expected or actual date when the note is no longer true",
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text="The author of the note",
    )


class Imagetype(models.Model):
    name = models.CharField("name", max_length=50, help_text="The name of the type")

    def __str__(self):
        return self.name

    class Meta:
        ordering = ("name",)
        verbose_name = "Image type"


class Image(models.Model):
    person = models.ForeignKey(
        Person,
        on_delete=models.CASCADE,
        help_text="The person to which this link belongs",
    )
    imagefile = models.ImageField("file", upload_to="personimages")
    imagetype = models.ForeignKey(
        Imagetype,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        help_text="The type of image,",
    )


class Linkexternaltype(models.Model):
    name = models.CharField("name", max_length=50, help_text="The name of the type,")

    def __str__(self):
        return self.name

    class Meta:
        ordering = ("name",)
        verbose_name = "Name for External Link"


class Linkexternal(models.Model):
    person = models.ForeignKey(
        Person,
        on_delete=models.CASCADE,
        help_text="The person to which this link belongs",
    )
    linkexternaltype = models.ForeignKey(
        Linkexternaltype,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        help_text="The name of the link,",
    )
    url = models.URLField("url", help_text="The url of the link")

    def __str__(self):
        return "[{}]({})".format(self.type, self.url)

    class Meta:
        verbose_name = "External Link"


class Submembership(models.Model):
    person = models.ForeignKey(
        Person,
        on_delete=models.CASCADE,
        help_text="The peson who is a member of the subcommittee",
    )
    subposition = models.ForeignKey(
        Subposition,
        on_delete=models.CASCADE,
        help_text="The committee and position in which the person is a member",
    )

    def __str__(self):
        return "{}->{}".format(self.person, self.subposition)

    class Meta:
        verbose_name = "Subcommittee Membership"
        ordering = ("subposition", "person")


class Due(models.Model):
    due_date = models.DateField(
        "due date", null=True, blank=True, help_text="The date this payment is/was due"
    )


class Duestat(models.Model):
    due = models.ForeignKey(
        Due, on_delete=models.CASCADE, help_text="The due which applies to this person"
    )
    person = models.ForeignKey(
        Person,
        on_delete=models.CASCADE,
        help_text="The person to whom this dues action applies",
    )
    effective_date = models.DateField(
        "effective date",
        null=True,
        blank=True,
        help_text="The effective date of the payment or waiver (the date the action counts as - which may be different from the actual date of transaction)",
    )
    status = models.IntegerField(
        "status",
        default=0,
        choices=[(0, "Incomplete"), (1, "Complete")],
        help_text="The status of this status assignment",
    )


class Attendance(models.Model):
    person = models.ForeignKey(
        Person,
        on_delete=models.CASCADE,
        help_text="The person who attended the meeting",
    )
    meeting = models.ForeignKey(
        Meeting,
        on_delete=models.CASCADE,
        help_text="The meeting which the person attended",
    )

    def __str__(self):
        return "{} at {}".format(self.person, self.meeting)

    class Meta:
        ordering = ("person__name_last", "meeting")


