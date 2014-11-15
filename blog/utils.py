import hashlib


def md5sum(filename):
    """Return the md5sum of the file

    :param filename: absolute path to the file
    :type filename: str"""

    md5 = hashlib.md5()

    with open(filename, 'rb') as f:
        for chunk in iter(lambda: f.read(128 * md5.block_size), b''):
            md5.update(chunk)

    return md5.hexdigest()


def save_post_file(filename, **kwargs):
    """Create or update the post file

    :param filename: absolute path to the file
    :type filename: str"""

    filecontent = ""

    for header in ['title', 'author', 'date', 'parser']:
        if header in kwargs and len(str(kwargs[header]).strip()) > 0:
            filecontent += "%s: %s\n" % (header, kwargs[header])
    if 'content' in kwargs:
        filecontent += "\n\n%s" % (kwargs['content'],)

    with open(filename, 'w') as f:
        f.write(filecontent)

    return md5sum(filename)


def wrap_description(content, length=255):
    """Wrap content text and return description.
    Description is from begening to the first blank line and/or the first X
    characters.

    :param content: text to wrap
    :type content: str
    :param length: number max of characters in the description
    :type length: int"""

    description = ""

    for line in content.split('\n'):
        if len(line.strip()) > 0:
            description += '%s\n' % (line,)
        else:
            break

    if len(description) > length:
        _description = ''
        for word in description.split(' '):
            if len('%s %s' % (_description, word)) < length:
                _description += ' %s' % (word,)
        description = _description

    return '%s...' % (description.lstrip().rstrip(),)
