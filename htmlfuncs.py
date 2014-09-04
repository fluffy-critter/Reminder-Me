def form_sanitize(text):
    text = text.replace('&', '&amp;')
    for chr,ent in {
            '<': '&lt;',
            '>': '&gt;',
            '"': '&quot;',
            }.items():
        text = text.replace(chr, ent)
    return text
