
import simplejson

from languages import Translation, Language
from urllib import urlencode
from twisted.web import client
from twisted.internet import defer, reactor

GOOGLE_TRANSLATE_API_URL = 'http://ajax.googleapis.com/ajax/services/language/translate?%s'

class Translate(object):
    
    def __init__(self, language_origin, language_destiny, client=client):
        self.lo = language_origin
        self.ld = language_destiny
        self.client = client
        self.translation = Translation(self.lo, self.ld)
        
    def _create_url(self, word):
        params = urlencode({"q":word, "langpair":str(self.translation), 
                            "hl":"it","ie":"UTF-8", "v":"1.0", "oe":"UTF-8"})
        request_url = GOOGLE_TRANSLATE_API_URL % params
        return request_url
    
    def translate(self, word):
        
        def gotResponse(r):
            try:
                json = simplejson.loads(r)
                translated_text = json[u'responseData'][u'translatedText']
            except ValueError:
                translated_text = r
            rv.callback(translated_text)
                
        rv = defer.Deferred()
        response_url = self._create_url(word)
        response = self.client.getPage(response_url,method='GET') \
                         .addCallback(gotResponse) \
                         .addErrback(lambda e: rv.errback(e))
        return rv
                                                            
