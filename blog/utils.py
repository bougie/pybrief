import hashlib
import re
import logging
from datetime import datetime
from django.utils.dateparse import parse_datetime
import blog.models

HEADERS = ['title', 'parser', 'tags', 'author', 'date']


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

    if 'date' in kwargs:
        kwargs['date'] = kwargs['date'].strftime('%Y-%m-%d %H:%M')

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


def parse_blog_file(filename):
    """Parse the content of a blog post.

    :param filename: path to the post to parse
    :type filename: str"""

    try:
        with open(filename, 'r') as f:
            data = {'filename': filename, 'content': ''}

            in_headers = True
            nb_blank_lines = 2
            for line in f:
                if in_headers is True:  # parse headers
                    m = re.search('^(' + '|'.join(HEADERS) + '):(.*)', line)
                    if m:
                        data[m.group(1).strip()] = m.group(2).strip()
                    elif nb_blank_lines > 1:
                        nb_blank_lines -= 1
                    else:
                        in_headers = False
                else:  # parse body
                    data['content'] += line

            # Do some transformations
            if 'date' in data:
                data['create_date'] = parse_datetime(data['date'])
            else:
                data['create_date'] = datetime.now()

        return data
    except:
        return None


def delete_post(filename):
    try:
        blog.models.Post.objects.get(filename=filename).delete()
    except blog.models.Post.DoesNotExist:
        logging.error("Error while retrieving blog post to delete")
    except Exception as e:
        logging.error(str(e))
