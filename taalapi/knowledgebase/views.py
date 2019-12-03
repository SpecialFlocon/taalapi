from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .helpers import WelkLidwoordHelper
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

    @action(detail=False, methods=['get'], url_path='search/(?P<query>[a-z0-9]+)')
    def search(self, request, query):
        h = WelkLidwoordHelper()
        matching_words = Woord.objects.filter(woord__contains=query)[:5]

        # If no matches were returned, attempt to learn word
        if len(matching_words) == 0:
            helper_article_list = []
            helper_response = h.get(query)

            # If first value of the tuple is 0 (no error), extract article(s)
            # TODO(thepib): do something useful with failure values
            if helper_response[0] == 0:
                helper_article_list = helper_response[1]
                article_list = [Lidwoord.objects.get(lidwoord=a).id for a in helper_article_list]

                word = Woord.objects.create(woord=query)
                word.lidwoord.add(*article_list)

                # Somewhat dirty trick to pick up the newly added word
                matching_words = Woord.objects.filter(id=word.id)

        serializer = self.get_serializer(matching_words, many=True)
        return Response(serializer.data)
