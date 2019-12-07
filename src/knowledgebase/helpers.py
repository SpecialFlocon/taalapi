from abc import ABC
from bs4 import BeautifulSoup

import json
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

class WoordenlijstHelper(BaseHelper):
    """
    A helper that uses woordenlijst.org to determine
    whether a word is a de-woord of a het-woord.

    Return value: tuple with 3 fields: (error_code, description, accurate)
    - error_code: 0 -> success, -1 -> server-side error (failed API calls, invalid output), 1 -> client-side error (garbage input)
    - description: a short descriptive message
    - accurate: boolean. False if something is fishy (like a plural noun with 'het'). Note: it's best effort (but then again, this whole algo is).
    """

    def __init__(self, target_url='https://woordenlijst.org/api-proxy/'):
        super().__init__(target_url)

    def get(self, word):
        url_params = {'m': 'search', 'searchValue': word, 'tactical': 'true'}
        req_headers = {
            'Host': 'woordenlijst.org',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:70.0) Gecko/20100101 Firefox/70.0',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'Referer': 'https://woordenlijst.org/',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Cookie': 'has_js=1; showDetails=1',
            'Cache-Control': 'max-age=0'
        }

        response = requests.get(self.target_url, params=url_params, headers=req_headers)
        if response.status_code != requests.codes.ok:
            return (-1, "The HTTP request to woordenlijst.org API has failed.", False)

        # The request was successful, but we got an empty response. Weird.
        if not response.text:
            return (-1, "HTTP request to woordenlijst.org API succeeded, but got empty response.", False)

        api_response = None
        try:
            api_response = json.loads(response.text)
        except json.JSONDecodeError:
            return (-1, "Got invalid JSON from woordenlijst.org API.", False)

        # Try a path
        nouns = None
        try:
            # Filter out results we're not interested in (i.e. words that aren't nouns)
            results = api_response['_embedded']['exact']
            nouns = [(r['gram']['art'].lower(), r['lemma']) for r in results if r['type'].startswith('NOU')]
        except KeyError:
            return (-1, "JSON object structure from woordenlijst.org API has changed.", False)

        # No results.
        if not nouns:
            return (1, "Word (probably) doesn't exist.", False)
        # If there are multiple results, the word may have both de and het as articles.
        # Or there might be multiple word forms/meanings with the same article.
        elif len(nouns) > 1:
            articles = {n[0] for n in nouns}
            # Check if all words obtained from the API are the same as the requested one.
            # If not, mark result as inaccurate.
            accurate = all(n[1] == word for n in nouns)
            if 'de/het' in articles:
                return (0, ['de', 'het'], accurate)

            return (0, list(articles), accurate)

        # Only one result, surely it must be the correct article, unless word is different.
        noun = nouns[0]
        article = noun[0]
        return (0, [article], noun[1] == word)

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
