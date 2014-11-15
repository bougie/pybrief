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
