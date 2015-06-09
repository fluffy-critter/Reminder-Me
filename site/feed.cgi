#!/usr/bin/python

from model import Feed
import session
import base64
import datetime
import sys
import renderfuncs
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
now = datetime.datetime.utcnow()
notify_interval = feed.notify_interval*feed.notify_unit
notify_time = max(feed.notify_next, now - datetime.timedelta(seconds=notify_interval))

response = '''Content-type: application/rss+xml

<?xml version="1.0" encoding="utf-8"?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">
<channel>
<title><![CDATA[Reminder Me: {name}]]></title>
<atom:link href="{feed_url}" rel="self" type="application/rss+xml" />
<link>{edit_url}</link>
<description><![CDATA[A Reminder Me feed for {name}]]></description>
<language>en-us</language>'''

if notify_time < now:
    response += '''
<item>
<title><![CDATA[Reminder: {name}]]></title>
<link>{done_url}/{update_guid}</link>
<guid>{done_url}/{update_guid}</guid>
<description><![CDATA[
<p>{description}
<img src="{ping_url}">
</p>
<p>Overdue by {overdue}</p>

<p>Options:</p>

<ul>
<li><a href="{done_url}/{update_guid}">Mark completed</a></li>
<li>Snooze for: <ul>'''

    times=list(set([1800, 3600, 8*3600, 86400, 3*86400, notify_interval/2, notify_interval]))
    times.sort()

    for time in times:
        response += '<li><a href="{snooze_url}/%d">%s</a></li>' % (time, renderfuncs.format_delta(datetime.timedelta(seconds=time),False))

    response += '''
  </ul>
<li><a href="{edit_url}">Edit reminder</a></li>
</ul>
]]>
</description>
<pubDate>{notify_time}</pubDate>
</item>'''

response += '''
</channel>
</rss>''';

update_guid=md5("%s %s %s" % (feed.guid, feed.notify_next, feed.last_seen)).hexdigest()
print response.format(
    name=feed.name or '',
    description=feed.description or '',
    feed_url="%s/feed.cgi/%s" % (basedir, feed.guid),
    ping_url="%s/ping.cgi/%s/%s" % (basedir, feed.guid, update_guid),
    done_url="%s/action.cgi/%s/done" % (basedir, feed.guid),
    edit_url="%s/edit.cgi?feed=%s" % (basedir, feed.guid),
    snooze_url="%s/action.cgi/%s/snooze" % (basedir, feed.guid),
    update_guid=update_guid,
    notify_time=notify_time.strftime('%a, %d %b %Y %H:%M:%S +0000'),
    overdue=renderfuncs.format_delta(now - notify_time)
    )

