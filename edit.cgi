#!/usr/bin/python

from model import Feed
import session
import uuid
import htmlfuncs
import datetime

form = session.form()
if form.getfirst('feed'):
    feed = Feed.get(Feed.guid == form.getfirst('feed'))
else:
    feed = Feed()

needsSave = False
for key,(prop,type) in {
        'name': ('name',str),
        'description': ('description',str),
        'interval': ('notify_interval',int),
        'unit': ('notify_unit',int),
        }.items() :
    if form.getfirst(key):
        # We're saving to a new feed, so populate its basic data
        if not feed.guid:
            feed.guid = uuid.uuid4()
        setattr(feed, prop, type(form.getfirst(key)))
        needsSave = True

if needsSave:
    now = datetime.datetime.now()
    if not feed.notify_next or now > feed.notify_next:
        feed.notify_next = now + datetime.timedelta(seconds=feed.notify_interval*feed.notify_unit)
    feed.save()

response = '''Content-type: text/html

<!DOCTYPE html>
<html>
<head>
<title>Editing Feed</title>
<link rel="stylesheet" href="style.css">
</head>
<body>
'''

if feed.guid:
    response += '''
<div id="feedlink">
<li>Feed URL: <a href="{feed_url}">{feed_url}</a></li>
</div>
'''

response += '''
<h1>Editing Feed</h1>

<form method="POST" action="edit.cgi">'''

if feed.guid:
    response += '<input type="hidden" name="feed" value="{guid}">'

response += '''
<ul class="form">
<li><label for="name">Name:</label>
    <input type="text" name="name" id="name" value="{name}" placeholder="Name of the reminder">
</li>
<li><label for="description">Description:</label>
    <textarea id="description" name="description" placeholder="A detailed description">{desc}</textarea>
</li>
<li><label for="interval">Remind every</label>
    <input type="number" name="interval" id="interval" value="{interval}" placeholder="Update interval">
    <select id="unit" name="unit">'''
for (name,secs) in [('hours',3600),
                    ('days',86400),
                    ('weeks',86400*7),
                    ('months',86400*365/12)]:
    response += '<option value="%d"%s>%s</option>' % (
        secs,
        secs == feed.notify_unit and ' selected' or '',
        name
        )
response += '''
    </select>
</li>
</ul>

<input type="submit" value="Update">
</form>

</body>
</html>
'''

print response.format(
    feed_url="%s/feed.cgi/%s" % (session.request_script_dir(), feed.guid),
    guid=feed.guid,
    name=htmlfuncs.form_sanitize(feed.name or ''),
    desc=htmlfuncs.form_sanitize(feed.description or ''),
    interval=feed.notify_interval or 1,
    )
