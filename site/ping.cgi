#!env/bin/python

from model import Feed
import session
import datetime
import base64

data=base64.b64decode('R0lGODlhAQABAIAAAP///wAAACH5BAEAAAAALAAAAAABAAEAAAICRAEAOw==')
print '''Content-type: image/gif
Content-Length: %s
''' % len(data)

argv = session.argv()

feed = Feed.get(guid=argv[1])
feed.last_seen = datetime.datetime.utcnow()
feed.save()

print data

