#!/usr/bin/python

from model import Feed
import session
import datetime
import base64

argv = session.argv()

feed = Feed.get(guid=argv[1])
now = datetime.datetime.utcnow()
if not feed.last_seen or feed.last_seen < now - datetime.timedelta(seconds=3600):
    feed.last_seen = datetime.datetime.utcnow()
    feed.save()

data=base64.b64decode('R0lGODlhAQABAIAAAP///wAAACH5BAEAAAAALAAAAAABAAEAAAICRAEAOw==')

print '''Content-type: image/gif
Content-length: %d

%s''' % (len(data), data)
