import bleach
added_tags = ['br', 'div', 'u', 'span', 'p', 'h1', 'h2', 'h3', 'h4',
              'h5', 'h6', 'pre', 'img', 'src', 'table', 'tr', 'td', 'tbody']
added_attrbt = {'*': ['style', 'href', 'rel', 'src',
                      'data-filename', 'alt', 'background-color', 'class']}
styles = ['background-color', 'color', 'font-family',
          'width', 'height', 'src', 'text-align','margine-left']
protocols = ['data', 'http', 'https']
attbs = bleach.sanitizer.ALLOWED_ATTRIBUTES
attbs.update(added_attrbt)
tags = bleach.sanitizer.ALLOWED_TAGS + added_tags


def cl(data):
    html = data.read()
    html = html.decode("utf-8")
    cleaned = bleach.clean(html, tags=tags, attributes=attbs,
                          styles=styles, protocols=protocols)
    return cleaned