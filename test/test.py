from twisted.trial import unittest
from twisted.internet import defer
from twisted.web import error
import sys

sys.path.extend(['lib', '../lib'])
import translate
import languages

class FakeHTTP(object):

    def __init__(self):
        self.d = defer.Deferred()

    def getPage(self, *args, **kwargs):
        return self.d

class TranslateTest(unittest.TestCase):

    def testOKTranslation(self):
        fh = FakeHTTP()
        tr = translate.Translate(languages.Language(u'ITALIAN'),
                                 languages.Language(u'ENGLISH'),
                                 client=fh)
        d = tr.translate('ciao')
        def checkResult(s):
            self.assertEquals(s, 'hello')

        d.addCallback(checkResult)
        d.addErrback(lambda e: self.fail(str(e)))
        fh.d.callback('hello')

    def testOKTranslationFromLangAbbreviations(self):
        fh = FakeHTTP()
        tr = translate.Translate(languages.Language('it'),
                                 languages.Language('en'),
                                 client=fh)
        d = tr.translate('ciao')
        def checkResult(s):
            self.assertEquals(s, 'hello')

        d.addCallback(checkResult)
        d.addErrback(lambda e: self.fail(str(e)))
        fh.d.callback('hello')

    def testFailedTranslation(self):
        fh = FakeHTTP()
        tr = translate.Translate(languages.Language(u'ITALIAN'),
                                 languages.Language(u'ENGLISH'),
                                 client=fh)
        d = tr.translate('ciao')
        d.addCallback(lambda e: self.fail('Boo'))
        d.addErrback(lambda e: self.assertTrue(e.type == RuntimeError))
        fh.d.errback(RuntimeError('Blah'))




