import unittest

from Products.Five import zcml
from Products.Five import fiveconfigure
from Products.PloneTestCase import PloneTestCase as ptc
from Products.PloneTestCase.layer import PloneSite
ptc.setupPloneSite()

import collective.js.underscore

class TestCase(ptc.PloneTestCase):
    class layer(PloneSite):
        @classmethod
        def setUp(cls):
            fiveconfigure.debug_mode = True
            zcml.load_config('configure.zcml',
                             collective.js.underscore)
            fiveconfigure.debug_mode = False

        @classmethod
        def tearDown(cls):
            pass

def test_suite():
    return unittest.TestSuite()

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
