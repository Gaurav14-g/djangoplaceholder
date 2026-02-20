import uuid
from django.db import models
from django.contrib.auth.models import User
import json
import os


class UserProfile(models.Model):
    TITLE_CHOICES = [
        ('Mr', 'Mr'),
        ('Mrs', 'Mrs'),
        ('Miss', 'Miss'),
        ('Ms', 'Ms'),
        ('Dr', 'Dr'),
    ]
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    ]
    LANGUAGE_CHOICES = [
        ('English', 'English'),
        ('Spanish', 'Spanish'),
        ('French', 'French'),
        ('Chinese', 'Chinese'),
        ('Other', 'Other'),
    ]

    LOCATION_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), "Data", "location.json")
    with open(LOCATION_FILE, "r", encoding="utf-8") as f:
        location_data = json.load(f)

    COUNTRY_CHOICES = [(country["id"], country["name"]) for country in location_data["countries"]]
    STATE_CHOICES = []
    CITY_CHOICES = []

    for country in location_data["countries"]:
        for state_page in country.get("states", []):
            for state in state_page.get("data", []):
                STATE_CHOICES.append((state["id"], state["name"]))
                for city in state["cities"].get("data", []):
                    CITY_CHOICES.append((city["id"], city["name"]))

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=10, choices=TITLE_CHOICES, null=True, blank=True)
    father_name = models.CharField(max_length=50, blank=True, null=True)
    mother_name = models.CharField(max_length=50, blank=True, null=True)
    spouse_name = models.CharField(max_length=50, blank=True, null=True)
    preferred_name = models.CharField(max_length=50, blank=True, null=True)
    previous_last_name = models.CharField(max_length=50, blank=True, null=True)
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, null=True, blank=True, default='Male')
    first_language = models.CharField(max_length=20, choices=LANGUAGE_CHOICES, default='English', null=True, blank=True)
    parents_attend_uni_or_college = models.BooleanField(default=False, null=True, blank=True)
    passport_no = models.CharField(max_length=20, null=True, blank=True)
    passport_expiry_date = models.DateField(null=True, blank=True)
    file_number = models.CharField(max_length=50, null=True, blank=True)
    zipcode = models.CharField(max_length=10, null=True, blank=True)

    country_id = models.CharField(choices=COUNTRY_CHOICES, max_length=50, null=True, blank=True)
    state_id = models.CharField(choices=STATE_CHOICES, max_length=50, null=True, blank=True)
    city_id = models.CharField(choices=CITY_CHOICES, max_length=50, null=True, blank=True)

    mailing_address = models.TextField(null=True, blank=True)
    phone_no = models.CharField(max_length=20, null=True, blank=True)
    preferred_language = models.CharField(max_length=20, null=True, blank=True)

    country_of_citizenship_id = models.CharField(choices=COUNTRY_CHOICES, max_length=50, null=True, blank=True)
    country_of_birth_id = models.CharField(choices=COUNTRY_CHOICES, max_length=50, null=True, blank=True)

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_Indigenous = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    def clean(self):
        from django.core.exceptions import ValidationError

        # Unique passport check
        if self.passport_no:
            existing = UserProfile.objects.filter(passport_no=self.passport_no).exclude(id=self.id)
            if existing.exists():
                raise ValidationError({'passport_no': 'This passport number is already in use.'})
        else:
            raise ValidationError({'passport_no': 'Passport number is required.'})

    def __str__(self):
        return str(self.user.username)