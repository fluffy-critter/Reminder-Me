#!/usr/bin/python

import model
import session

print 'Content-type: text/html\n\n'

print '<p>Creating schema...'
model.create_tables()
print 'Done.</p>'

