from django.contrib.auth.models import User

from rest_framework import serializers

from .models import Lidwoord, Woord


class LidwoordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lidwoord
        fields = '__all__'

class WoordSerializer(serializers.ModelSerializer):
    lidwoord = serializers.StringRelatedField()

    class Meta:
        model = Woord
        fields = '__all__'
