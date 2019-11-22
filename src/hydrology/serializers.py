from rest_framework import serializers

from hydrology.models import Hydropost, WeatherImage


class HydropostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Hydropost
        fields = ('code', 'nameEn', 'name', 'lat', 'lon',)
        read_only_fields = ('code', )


class WeatherImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = WeatherImage
        fields = ('image', 'uploaded_at')
        read_only_fields = ('uploaded_at',)
