from rest_framework import serializers
from django.contrib.auth.models import User
from api.UserProfile.model import UserProfile
import json
import os

# Load location JSON
LOCATION_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), "Data", "location.json")
with open(LOCATION_FILE, "r", encoding="utf-8") as f:
    location_data = json.load(f)

country_dict = {}
state_dict = {}
city_dict = {}

for country in location_data["countries"]:
    country_dict[str(country["id"])] = country["name"]
    for state_page in country.get("states", []):
        for state in state_page.get("data", []):
            state_dict[str(state["id"])] = state["name"]
            for city in state.get("cities", {}).get("data", []):
                city_dict[str(city["id"])] = city["name"]


class UserProfileSerializer(serializers.ModelSerializer):
    user_email = serializers.EmailField(source='user.email', read_only=True)
    user_username = serializers.CharField(source='user.username', read_only=True)
    first_name = serializers.CharField(source='user.first_name', read_only=True)
    last_name = serializers.CharField(source='user.last_name', read_only=True)
    user = serializers.PrimaryKeyRelatedField(read_only=True)

    country_name = serializers.SerializerMethodField()
    state_name = serializers.SerializerMethodField()
    city_name = serializers.SerializerMethodField()
    country_of_citizenship_name = serializers.SerializerMethodField()
    country_of_birth_name = serializers.SerializerMethodField()

    passport_no = serializers.CharField(required=True, allow_blank=False, max_length=50)

    class Meta:
        model = UserProfile
        fields = [
            'id', 'title', 'preferred_name', 'previous_last_name', 'father_name', 'mother_name',
            'spouse_name', 'file_number', 'date_of_birth', 'gender', 'first_language',
            'parents_attend_uni_or_college', 'passport_no', 'passport_expiry_date', 'zipcode',
            'country_id', 'country_name',
            'state_id', 'state_name',
            'city_id', 'city_name',
            'mailing_address', 'phone_no', 'preferred_language',
            'country_of_citizenship_id', 'country_of_citizenship_name',
            'country_of_birth_id', 'country_of_birth_name',
            'user', 'user_email', 'user_username', 'first_name', 'last_name',
            'is_Indigenous', 'created_at', 'updated_at', 'deleted_at',
        ]
        read_only_fields = ['user', 'created_at', 'updated_at', 'deleted_at']

    def get_country_name(self, obj):
        return country_dict.get(str(obj.country_id)) if obj.country_id else None

    def get_state_name(self, obj):
        return state_dict.get(str(obj.state_id)) if obj.state_id else None

    def get_city_name(self, obj):
        return city_dict.get(str(obj.city_id)) if obj.city_id else None

    def get_country_of_citizenship_name(self, obj):
        return country_dict.get(str(obj.country_of_citizenship_id)) if obj.country_of_citizenship_id else None

    def get_country_of_birth_name(self, obj):
        return country_dict.get(str(obj.country_of_birth_id)) if obj.country_of_birth_id else None

    def validate(self, data):
        passport_no = data.get('passport_no')

        if not passport_no:
            raise serializers.ValidationError({
                'passport_no': 'Passport number is required.'
            })

        existing = UserProfile.objects.filter(passport_no=passport_no)
        if self.instance:
            existing = existing.exclude(id=self.instance.id)

        if existing.exists():
            raise serializers.ValidationError({
                'passport_no': 'This passport number is already in use.'
            })

        return data

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance