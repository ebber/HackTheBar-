
import urllib
from lxml import html

url = "192.168.1.1:88/status"
page = html.fromstring(urllib.urlopen(url).read())

print page
