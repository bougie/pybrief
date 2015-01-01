import re
import urllib.request
import html.parser


def get_title_link(url):
    """Get the page title for a given URL

    :param url: url you which get the title
    :type url: str"""

    title = None

    try:
        req = urllib.request.Request(url)
        req.add_header('User-agent', 'Mozilla/5.0')

        response = urllib.request.urlopen(req)
        try:
            response_charset = response.getheader(
                'Content-Type').split(';')[1].split('=')[1]
        except:
            # Charset does not exists in the Content-Type header
            # Using UTF-8 charset by default
            response_charset = 'UTF-8'
        content = str(response.read(), response_charset)

        tpattern = re.search(
            '<head.*>.*<title>(.*)</title>.*</head>',
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
    finally:
        return title


def get_domain_link(url):
    domain = None

    try:
        tpattern = re.search(
            "(https?://)?(.*/)?(.*)",
            url,
            flags=re.IGNORECASE | re.DOTALL)
        if tpattern is not None:
            if tpattern.group(2) is not None:
                domain = tpattern.group(2)
            else:
                domain = tpattern.group(3)

            # remove trailing slash
            if domain.endswith('/'):
                domain = domain[:-1]
    except:
        domain = None
    finally:
        return domain
