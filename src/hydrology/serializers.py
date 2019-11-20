from rest_framework import serializers

from hydrology.models import Hydropost


class HydropostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Hydropost
        fields = ('code', 'nameEn', 'name', 'lat', 'lon',)
        read_only_fields = ('code', )