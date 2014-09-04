#!/usr/bin/python

from model import Feed
import session
import datetime
import base64

argv = session.argv()

feed = Feed.get(guid=argv[1])
feed.last_seen = datetime.datetime.now()
feed.save()

data=base64.b64decode('R0lGODlhAQABAIAAAP///wAAACH5BAEAAAAALAAAAAABAAEAAAICRAEAOw==')

print '''Content-type: image/gif
Content-length: %d

%s''' % (len(data), data)
