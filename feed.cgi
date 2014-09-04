#!/usr/bin/python

from model import Feed
import session
import base64
import datetime
import sys
from hashlib import md5

argv = session.argv()

try:
    guid = argv[1]
    feed = Feed.get(Feed.guid == guid)
except:
    print '''Status: 404 Not Found
Content-type: text/html

The requested feed is not available.
'''
    sys.exit(1)

basedir=session.request_script_dir()

response = '''Content-type: application/rss+xml

<?xml version="1.0" encoding="utf-8"?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">
<channel>
<title><![CDATA[Reminder Me: {name}]]></title>
<atom:link href="{feed_url}" rel="self" type="application/rss+xml" />
<link>{edit_url}</link>
<description><![CDATA[A Reminder Me feed for {name}]]></description>
<language>en-us</language>'''

if feed.notify_next < datetime.datetime.now():
    response += '''
<item>
<title><![CDATA[Reminder: {name}]]></title>
<link>{done_url}</link>
<guid>{update_guid}</guid>
<description><![CDATA[
<p>{description}
<img src="{ping_url}">
</p>

<p>Options:</p>

<ul>
<li><a href="{done_url}">Mark completed</a></li>
<li>Snooze for: <ul>
  <li><a href="{snooze_url}/1800">30 minutes</a></li>
  <li><a href="{snooze_url}/3600">1 hour</a></li>
  <li><a href="{snooze_url}/28800">8 hours</a></li>
  <li><a href="{snooze_url}/86400">1 day</a></li>
  </ul>
<li><a href="{edit_url}">Edit reminder</a></li>
</ul>
]]>
</description>
<pubDate>{last_seen}</pubDate>
</item>'''

response += '''
</channel>
</rss>''';

update_guid=md5("%s %s" % (feed.guid, feed.last_seen)).hexdigest()
print response.format(
    name=feed.name,
    description=feed.description,
    feed_url="%s/feed.cgi/%s" % (basedir, feed.guid),
    ping_url="%s/ping.cgi/%s/%s" % (basedir, feed.guid, update_guid),
    done_url="%s/action.cgi/%s/done" % (basedir, feed.guid),
    edit_url="%s/edit.cgi?feed=%s" % (basedir, feed.guid),
    snooze_url="%s/action.cgi/%s/snooze" % (basedir, feed.guid),
    update_guid=update_guid,
    last_seen=feed.last_seen
    )

