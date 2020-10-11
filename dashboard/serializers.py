from rest_framework import serializers

from league.models import Archer


class ArcherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Archer
        fields = ['id', 'full_name', 'get_sex_display', 'get_experience_display']
