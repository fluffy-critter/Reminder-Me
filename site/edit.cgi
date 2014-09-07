#!/usr/bin/python

from model import Feed
import session
import uuid
import htmlfuncs
import datetime
import sys

feedValid = False
newFeed = False

form = session.form()
if form.getfirst('feed'):
    feed = Feed.get(guid=form.getfirst('feed'))
    feedValid = True
else:
    feed = Feed(guid = uuid.uuid4())
    newFeed = True

needsSave = False
for key,(prop,type) in {
        'name': ('name',str),
        'description': ('description',str),
        'interval': ('notify_interval',int),
        'unit': ('notify_unit',int),
        }.items() :
    if form.getfirst(key) != None:
        setattr(feed, prop, type(form.getfirst(key)))
        needsSave = True

errors = []
if needsSave:
    if not feed.name:
        errors.append("Reminder needs a name.")
    elif len(feed.name) > 255:
        errors.append("Name should be a reasonable length.")

    if len(feed.description) > 255:
        errors.append("Description should be a reasonable length.")

    if feed.notify_interval <= 0 or feed.notify_unit <= 0:
        errors.append("Time units should make sense.")

    now = datetime.datetime.utcnow()
    if not feed.notify_next or now > feed.notify_next:
        feed.notify_next = now + datetime.timedelta(seconds=feed.notify_interval*feed.notify_unit)

    if not errors:
        try:
            feed.save(force_insert=newFeed)
            feedValid = True
            print '''Location: {edit_url}
Content-type: text/html

<a href="{edit_url}">Saved; redirecting...</a>'''.format(
    edit_url='%s?feed=%s'%(session.request_script_path(),feed.guid))
            sys.exit()
        
        except Exception as e:
            errors.append(e.message)

response = '''Content-type: text/html

<!DOCTYPE html>
<html>
<head>
<title>Editing Feed{title_name}</title>
<link rel="stylesheet" href="style.css">
</head>
<body>
'''

response += '''
<div class="container">
<h1>Editing Feed</h1>
'''

if errors:
    if len(errors) == 1:
        response += '<div class="error">Error: <span>%s</span></div>' % errors[0]
    else:
        response += '<div class="error">Errors:<ul>'
        for err in errors:
            response += '<li>%s</li>' % err
        response += '</ul></div>'


response += '''<div><form method="POST" action="edit.cgi">'''

if feedValid:
    response += '<input type="hidden" name="feed" value="{guid}">'

response += '''
<ul class="form">
<li><label for="name">Name:</label> <span class="required">(required)</span>
    <input type="text" name="name" id="name" value="{name}" placeholder="Name of the reminder">
</li>
<li><label for="description">Description:</label> (HTML okay)
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

</form></div>
</div>
'''

if feedValid:
    response += '''
<div class="container" id="feedlink">
<h1>Feed URL</h1>
<div><a href="{feed_url}">{feed_url}</a></div>
</div>
'''

response += '''
<p class="back"><a href=".">Reminder Me</a></p>

</body>
</html>
'''

print response.format(
    feed_url="%s/feed.cgi/%s" % (session.request_script_dir(), feed.guid),
    guid=feed.guid,
    title_name=htmlfuncs.form_sanitize(feed.name and (': %s'%feed.name) or ''),
    name=htmlfuncs.form_sanitize(feed.name or ''),
    desc=htmlfuncs.form_sanitize(feed.description or ''),
    interval=feed.notify_interval or 1,
    )
