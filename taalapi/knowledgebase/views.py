from rest_framework import viewsets

from .models import Lidwoord, Woord
from .serializers import LidwoordSerializer, WoordSerializer


class LidwoordenViewSet(viewsets.ModelViewSet):
    """
    Implement all the operations on lidwoord model
    """

    queryset = Lidwoord.objects.all()
    serializer_class = LidwoordSerializer

class WoordenViewSet(viewsets.ModelViewSet):
    """
    Implement all the operations on woord model
    """

    queryset = Woord.objects.all()
    serializer_class = WoordSerializer
