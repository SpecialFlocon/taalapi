from abc import ABC
from bs4 import BeautifulSoup

import requests


class BaseHelper(ABC):
    """
    An abstract class that can be derived to define a helper,
    a piece of code that can grab arbitrary data from websites.
    """

    target_url = None

    def __init__(self, target_url):
        self.target_url = target_url

    def get(self, word):
        """
        Since every website is different and can't be bothered to offer APIs,
        we need to work our way through HTML documents.
        Therefore, this method is implementation-specific.
        """

        pass

class WelkLidwoordHelper(BaseHelper):
    """
    A helper that uses the WelkLidwoord website to determine
    whether a word is a de-woord or a het-woord.
    """

    def __init__(self, target_url='https://welklidwoord.nl'):
        super().__init__(target_url)

    def get(self, word):
        query_url = "{}/{}".format(self.target_url, word)
        possible_values = {'obvious': ['De', 'Het'], 'ambiguous': ['Het of de', 'De of het']}

        response = requests.get(query_url)
        soup = BeautifulSoup(response.text, "html.parser")
        s = None

        try:
            # Path in welklidwoord.nl is #content>h1>span (for now, at least.)
            s = soup.find(id='content').find('h1').find('span').string
        except AttributeError:
            # Unsurprisingly, something went wrong while looking for the info we need.
            # That's expected to happen more often than one would think, so we're prepared.
            return (-1, "Website document structure has changed.")

        # Somehow, the document structure was left intact,
        # but we were unable to extract the string?
        if not s:
            return (-1, "Expected article, got empty string.")

        # Try to extract article string from possible values, give up if not possible.
        pv_list = [x for v in possible_values.values() for x in v]
        if s not in pv_list:
            return (-1, "Unknown article value obtained from website.")

        raw_article = str(s)

        # If we've gotten an ambiguous answer (de of het, het of de), word may not exist.
        # Look for clues in the HTML document.
        if raw_article in possible_values['ambiguous']:
            try:
                # WelkLidwoord displays a message in #content>h3 tag
                s = soup.find(id='content').find('h3').string
            except AttributeError:
                pass
            else:
                # Yep, that's a solid test
                if 'Helaas' in s:
                    return (1, "Word (probably) doesn't exist.")

            article = ['de', 'het']
        else:
            article = [raw_article.lower()]

        return (0, article)
