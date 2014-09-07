def form_sanitize(text):
    text = text.replace('&', '&amp;')
    for chr,ent in {
            '<': '&lt;',
            '>': '&gt;',
            '"': '&quot;',
            }.items():
        text = text.replace(chr, ent)
    return text

def format_delta(td,suppress_unit=True):
    suffix=''
    when = int(td.total_seconds())
    
    if not when:
        return "right now"
    
    if when < 0:
        when = -when
        suffix = " ago"
    when_left = when

    duration_list = []
    for (label,period) in [('month',86400*365/12),
                           ('week',86400*7),
                           ('day',86400),
                           ('hour',3600),
                           ('minute',60),
                           ('second',1)]:
        if when == period and suppress_unit:
            duration_list = [label]
            break

        val = when_left/period
        if val:
            duration_list.append("%d %s%s" % (
                val,
                label,
                val > 1 and 's' or ''))
            when_left -= val*period
    return "%s%s" % (', '.join(duration_list), suffix)
