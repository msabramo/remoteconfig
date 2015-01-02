import httpretty

from remoteconfig import config


class TestRemoteConfig(object):
  @httpretty.activate
  def test_read(self):
    config_url = 'http://test-remoteconfig.com/config.ini'
    config_content = '[section]\n\nkey = value\n'
    httpretty.register_uri(httpretty.GET, config_url, body=config_content)
    config.read(config_url)

    assert config_content == str(config)
