# Reminder Me

A simple Python web service to generate RSS feeds for recurring
reminders.

Demo site: [http://rm.beesbuzz.biz/](http://rm.beesbuzz.biz/)

## About

Ever need recurring reminders to do simple things, but always forget
to do it? Hate trying to deal with various reminder apps, but live in
an RSS reader for everything anyway?  Reminder Me might be for you!

This simply generates an RSS feed which will remind you to do
something after a certain period of time.  If you ignore the reminder,
it'll keep on reminding you until you say you've done the thing (as
long as your feed reader shows images, anyway).

It's good for things that you need to be reminded of when you're
otherwise reading your RSS feeds; cleaning the cat box, doing your
laundry, watering the plants, that sort of thing.  It's perfect for
errands which need to happen at a certain rough interval but which
don't necessarily need to happen at a specific time of day or week.

## Installation

You just need the following:

* An ordinary CGI-enabled directory which serves up `.cgi` files as
  CGI scripts (ideally running with suexec)
* [peewee](https://github.com/coleifer/peewee) installed (using `pip`
  or whatever installation mechanism you prefer)

To install or upgrade, just `git clone` this, point your DocumentRoot
(or equivalent) at the `site` directory, point your browser at the
deployed `install.cgi`, and then you can start making reminder
feeds. That's it!

Note that for security reasons, the database is kept outside of the
site directory, and for ease-of-configuration reasons, it uses a
relative path, `../data`. If you just want to put this in a
subdirectory of an existing web share, you'll have to do something
like this:

    git clone https://github.com/plaidfluff/Reminder-Me
    cd public_html
    ln -s ../Reminder-Me/site rm

However, that working depends on whether your web server is configured
to follow symlinks.  If you get really stuck you can just change the
file path in `site/model.py`. Whatever you do, make sure that
`reminders.db` cannot be read by web browsers - otherwise people can
find out your feed GUIDs and do nasty things to you!
