import base64
import os
import requests
import tempfile
import time


def _url_content_cache_file(url):
  return os.path.join(tempfile.gettempdir(), 'url-content-cache-%s' % base64.urlsafe_b64encode(url))


def url_content(url, cache_duration=None, from_cache_on_error=False):
  """
  Get content for the given URL

  :param str url: The URL to get content from
  :param int cache_duration: Optionally cache the content for the given duration to avoid downloading too often.
  :param bool from_cache_on_error: Return cached content on any HTTP request error if available.
  """
  cache_file = _url_content_cache_file(url)

  if cache_duration:
    if os.path.exists(cache_file):
      stat = os.stat(cache_file)
      cached_time = stat.st_mtime
      if time.time() - cached_time < cache_duration:
        with open(cache_file) as fp:
          return fp.read()

  try:
    response = requests.get(url)
    response.raise_for_status()
    content = response.text

  except Exception:
    if from_cache_on_error and os.path.exists(cache_file):
      with open(cache_file) as fp:
        return fp.read()
    else:
      raise

  if cache_duration or from_cache_on_error:
    with open(cache_file, 'w') as fp:
      fp.write(content)

  return content
