from rest_framework import serializers
from social_network.models import Country


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        exclude = ()
