from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .helpers import WoordenlijstHelper
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

    @action(detail=False, methods=['get'], url_path='search/(?P<query>[a-zA-Z]+)')
    def search(self, request, query):
        h = WoordenlijstHelper()
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
            # If first value of the tuple is -1 (fetch error), HTML parsing code be faililng, yield server error
            elif helper_response[0] == -1:
                data = {'error': helper_response[1]}
                return Response(data=data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            # If first value of the tuple is 1 (word not found), bail out with a 404
            elif helper_response[0] == 1:
                return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(matching_words, many=True)
        return Response(serializer.data)
