import re
import urllib.request
import http.client
import html.parser


def get_content_type(url):
    """Get the content type of a page

    :param url: url to get the content type
    :type url: str"""

    content_type = None

    try:
        connection = http.client.HTTPConnection(
            get_domain_link(url),
            timeout=2)
        connection.request("HEAD", '/')
        response = connection.getresponse()
        if response is not None:
            content_type = response.getheader('Content-Type')
            if content_type is not None:
                content_type = content_type.split(';')[0]
    except:
        content_type = None
    finally:
        return content_type


def get_title_link(url):
    """Get the page title for a given URL

    :param url: url to get the title
    :type url: str"""

    title = None

    if get_content_type(url) in ['text/html']:
        try:
            req = urllib.request.Request(url)
            req.add_header('User-agent', 'Mozilla/5.0')

            response = urllib.request.urlopen(req, timeout=2)
            try:
                response_charset = response.getheader(
                    'Content-Type').split(';')[1].split('=')[1]
            except:
                # Charset does not exists in the Content-Type header
                # Using UTF-8 charset by default
                response_charset = 'UTF-8'
            content = str(response.read(), response_charset)

            tpattern = re.search(
                '<head.*>.*<title.*>(.*)</title>.*</head>',
                content,
                flags=re.IGNORECASE | re.DOTALL
            )

            if tpattern is not None:
                # Remove useless spaces and convert HTML entities
                # into human readable ones
                ti = map(lambda s: s.translate(s.maketrans("\n\t\r", "   ")),
                         tpattern.group(1).split("\n"))
                h = html.parser.HTMLParser()

                title = h.unescape(" ".join(ti).strip())
        except Exception:
            title = None

    return title


def get_domain_link(url):
    """Get the FQDN of a given url

    :param url: url to get the domain
    :type url: str"""

    domain = None

    try:
        tpattern = re.search("(https?://)?(.*)",
                             url,
                             flags=re.IGNORECASE | re.DOTALL)
        if tpattern is not None:
            if tpattern.group(2) is not None:
                domain = tpattern.group(2)
            else:
                domain = tpattern.group(1)
            domain = domain.split('/')[0]

            # remove trailing slash
            if domain.endswith('/'):
                domain = domain[:-1]
            domain = domain.split('/')[0]
    except:
        domain = None
    finally:
        return domain
