#!env/bin/python

from model import Feed
import datetime
import renderfuncs
import session
import sys

argv = session.argv()
form = session.form()

feed = Feed.get(guid=argv[1])
action = argv[2]

now = datetime.datetime.utcnow()

drift = 0
if action == 'done':
    when = feed.notify_interval * feed.notify_unit
    drift = max(0,min((now - feed.notify_next).seconds, when/4))
elif action == 'snooze':
    if len(argv) > 3:
        when = int(argv[3])
    else:
        when = 3600
else:
    print '''Status: 400 Bad request
Content-type: text/html

Unknown action %s''' % action
    sys.exit(1)

feed.notify_next = now + datetime.timedelta(seconds=when-drift)
feed.save()

response = 'Content-type: text/html\n'

if form.getfirst('edit'):
    response += 'Location: %s/edit.cgi?feed=%s\n' % (session.request_script_dir(),feed.guid)

response += '''
<html><head><title>Alarm reset: {name}</title>
<link rel="stylesheet" href="{base_url}/style.css">
</head>
<body>

<div class="container">
<h1>Alarm reset</h1>
<div>
<p id="reset">Alarm "<span class="name">{name}</span>" has been reset.'''

if when:
    response += '''
You won't be notified for another <span class="duration">{duration}</span>.
'''

response += '''
</p>

<p>Actions:</p>
<ul>
<li><a href="{edit_url}?feed={guid}">Edit this reminder</a></li>
<li><a href="{edit_url}">Create another reminder</a></li>
<li><a href="{base_url}">Visit the Reminder Me site</a></li>
</ul>
</div>
</div>

<p class="back"><a href=".">Reminder Me</a></p>

</body></html>'''

basedir=session.request_script_dir()

print response.format(guid=feed.guid,
                      name=feed.name,
                      edit_url="%s/edit.cgi" % basedir,
                      base_url=basedir,
                      duration=renderfuncs.format_delta(datetime.timedelta(seconds=when)))

