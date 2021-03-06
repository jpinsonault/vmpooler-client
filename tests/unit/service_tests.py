"""
.. module:: vmpooler_client.tests.unit.service_tests
   :synopsis: Unit tests for functions interacting with the vmpooler API.
   :platform: Unix, Linux, Windows
   :license: BSD
.. moduleauthor:: Ryan Gard <ryan.gard@puppetlabs.com>
.. moduleauthor:: Joe Pinsonault <joe.pinsonault@puppetlabs.com>
"""

#===================================================================================================
# Imports
#===================================================================================================
from lib import service
from unittest import main, TestCase, skipIf
from mock import patch

#===================================================================================================
# Globals
#===================================================================================================
SKIP_EVERYTHING = False

#===================================================================================================
# Mocks
#===================================================================================================
class _HttpResponse(object):
  def __init__(self, status, return_value='default', reason='default'):
    self.status = status
    self.reason = reason
    self._return_value = return_value

  def read(self):
    return self._return_value

#===================================================================================================
# Tests
#===================================================================================================
class ServiceTests(TestCase):
  """Tests for the ResourceConfig class in the config module."""

  def setUp(self):
    self.vmpooler_url = 'vmpooler.delivery.puppetlabs.net'
    self.template_name = 'centos-4-x86_64'
    self.hostname = 'j2bgvv6x1ihqslx'
    self.auth_token = 'bdct6vxix5yfxndry32kmark0pyhriq9'

  @skipIf(SKIP_EVERYTHING, 'Skip if we are creating/modifying tests!')
  def test01_get_vm(self):
    """Happy path test to verify retrieving VM instances from the pooler."""

    # Construct mock return object.
    json_body = """
      {{
        "ok": true,
        "{0}": {{
          "hostname": "{1}",
          "ok": true
        }},
        "domain": "delivery.puppetlabs.net"
      }}""".format(self.template_name, self.hostname)

    resp = _HttpResponse(200, json_body)

    # Patch
    with patch.object(service, '_make_request', return_value=resp) as mock_func:
      self.assertEqual(service.get_vm(self.vmpooler_url,
                                      self.template_name,
                                      self.auth_token),
                       self.hostname)
