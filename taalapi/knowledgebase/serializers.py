from django.contrib.auth.models import User

from rest_framework import serializers

from .models import Lidwoord, Woord


class LidwoordSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='lidwoord-detail')

    class Meta:
        model = Lidwoord
        fields = '__all__'

class WoordSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='woord-detail')

    class Meta:
        model = Woord
        fields = '__all__'
