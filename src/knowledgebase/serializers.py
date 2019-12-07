from django.contrib.auth.models import User

from rest_framework import serializers

from .models import Lidwoord, Woord


class LidwoordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lidwoord
        fields = '__all__'

class WoordSerializer(serializers.ModelSerializer):
    lidwoord_name = serializers.StringRelatedField(many=True, read_only=True, source='lidwoord')

    class Meta:
        model = Woord
        fields = '__all__'
