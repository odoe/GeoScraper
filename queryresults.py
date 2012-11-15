import urllib, urllib2, json

class QueryServer:
  def request(self, where, url):
    values = {'where':where,'returnGeometry':'true','outFields':'*','f':'json'}
    data = urllib.urlencode(values)
    req = urllib2.Request(url, data)
    result = json.load(urllib2.urlopen(req))
    return result
