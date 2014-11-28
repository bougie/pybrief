#!/usr/bin/env python
import os
import sys
import time
import django
import atexit
import signal
import resource
import logging
import argparse
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, FileSystemMovedEvent

base_dir = os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(base_dir)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "pybrief.settings")
django.setup()

from blog.utils import parse_blog_file, delete_post
from blog.forms import PostForm


class Daemon:
    """A generic daemon class.

    Usage: subclass the Daemon class and override the run() method"""

    def __init__(self, name, pidfile, logdir='/tmp', loglevel=logging.INFO,
                 stdin='/dev/null', stdout='/dev/null', stderr='/dev/null'):
        self.name = name
        self.stdin = stdin
        self.stdout = stdout
        self.stderr = stderr
        self.pidfile = pidfile
        self.logdir = logdir
        self.loglevel = loglevel

    def daemonize(self):
        """do the UNIX double-fork magic, see Stevens' "Advanced
        Programming in the UNIX Environment" for details (ISBN 0201563177)
        http://www.erlenstar.demon.co.uk/unix/faq_2.html#SEC16"""

        try:
            pid = os.fork()
            if pid > 0:
                # exit first parent
                sys.exit(0)
        except OSError as e:
            logging.error("fork #1 failed: %d (%s)\n" % (e.errno, e.strerror))
            os._exit(1)

        # decouple from parent environment
        os.chdir("/")
        os.setsid()
        os.umask(0)

        # do second fork
        try:
            pid = os.fork()
            if pid > 0:
                # exit from second parent
                sys.exit(0)
        except OSError as e:
            logging.error("fork #2 failed: %d (%s)\n" % (e.errno, e.strerror))
            os._exit(1)

        # A daemon is never localized
        os.environ.setdefault("LC_ALL", "POSIX")

        # close all open file descriptors
        maxfd = resource.getrlimit(resource.RLIMIT_NOFILE)[1]
        if maxfd == resource.RLIM_INFINITY:
            maxfd = 1024
        for fd in range(0, maxfd):
            try:
                os.close(fd)
            except OSError:  # ERROR, fd wasn't open to begin with (ignored)
                pass

        # redirect standard file descriptors
        sys.stdout.flush()
        sys.stderr.flush()
        si = open(self.stdin, 'r')
        so = open(self.stdout, 'a+')
        se = open(self.stderr, 'a+')
        os.dup2(si.fileno(), sys.stdin.fileno())
        os.dup2(so.fileno(), sys.stdout.fileno())
        os.dup2(se.fileno(), sys.stderr.fileno())

        # write pidfile
        pid = str(os.getpid())
        with open(self.pidfile, 'w+') as f:
            f.write("%s\n" % pid)
        atexit.register(self._delpid)

        # Handler SIGTERM signal
        signal.signal(signal.SIGTERM, self.handler)

    def handler(self, signum, frame):
        if signum == signal.SIGTERM:
            # pidfile will be deleted by _delpid
            sys.exit(0)
        else:
            logging.debug("Signal %s caught" % (signal,))

    def log_to_file(self):
        """Create an handler to logging for logging message into a file"""

        logger = logging.getLogger()

        handler = logging.FileHandler('%s.log' % (os.path.join(self.logdir,
                                                               self.name)))
        handler.setLevel(self.loglevel)

        logger.addHandler(handler)

    def _delpid(self):
        if os.path.exists(self.pidfile):
            os.remove(self.pidfile)

    def _getpid(self):
        """Check for a pidfile to see if the daemon already runs"""

        try:
            with open(self.pidfile, 'r') as pf:
                pid = int(pf.read().strip())
        except IOError:
            pid = None

        return pid

    def start(self):
        """Start the daemon"""

        if self._getpid() is not None:
            logging.error(
                "pidfile %s already exist. Daemon already running?\n" % (
                    self.pidfile,))
            sys.exit(1)

        # Start the daemon
        self.daemonize()
        # redirect log message
        self.log_to_file()
        # launch core "app"
        self.run()

    def stop(self):
        """Stop the daemon"""

        pid = self._getpid()
        if pid is None:
            logging.error(
                "pidfile %s does not exist. Daemon not running?\n" % (
                    self.pidfile,))
            return  # not an error in a restart

        # Try killing the daemon process
        try:
            while True:
                os.kill(pid, signal.SIGTERM)
                time.sleep(0.1)
        except OSError as err:
            err = str(err)
            if err.find("No such process") > 0:
                self._delpid()
            else:
                sys.stderr.write(err)
                sys.exit(1)

    def restart(self):
        """Restart the daemon"""

        self.stop()
        self.start()

    def run(self):
        """
        You should override this method when you subclass Daemon. It will be
        called after the process has been daemonized by start() or restart().
        """


def import_from_file(filename):
    """import the file `filename`"""

    if filename.endswith('.bp'):
        logging.debug("Importing %s" % (filename,))
        bpcontent = parse_blog_file(filename)
        if bpcontent is not None:
            try:
                PostForm(bpcontent).save()
            except Exception as e:
                logging.error("Error while importing %s : %s" % (filename,
                                                                 str(e)))


def delete_from_file(filename):
    """Delete a post in the BDD for a gevin filename"""

    if filename.endswith('.bp'):
        logging.debug("Deleting %s" % (filename,))
        try:
            delete_post(filename)
        except Exception as e:
            logging.error("Error while deleting %s : %s" % (filename, str(e)))


def import_from_files(path):
    """Import all file from a directory `path`"""

    for item in os.listdir(path):
        import_from_file(os.path.join(path, item))


class PostFileEventHandler(FileSystemEventHandler):
    def __init__(self, path, *args, **kwargs):
        self.path = path

        super(PostFileEventHandler, self).__init__(*args, **kwargs)

    def on_created(self, event):
        self._on_change(event)

    def on_modified(self, event):
        self._on_change(event)

    def on_moved(self, event):
        self._on_change(event)

    def on_deleted(self, event):
        self._on_change(event, deleted=True)

    def _on_change(self, event, deleted=False):
        if event.is_directory is False:
            if isinstance(event, FileSystemMovedEvent):
                logging.debug("%s %s -> %s" % (event.event_type,
                                               event.src_path,
                                               event.dest_path))

                path = event.dest_path
            else:
                logging.debug("%s %s" % (event.event_type, event.src_path))

                path = event.src_path

            if deleted:
                delete_from_file(path)
            else:
                import_from_file(path)


class Importer(Daemon):
    def __init__(self, name, path, *args, **kwargs):
        self.path = path

        super(Importer, self).__init__(name, *args, **kwargs)

    def run(self):
        logging.info('Start watching %s directory' % (self.path,))

        observer = Observer()
        observer.schedule(PostFileEventHandler(self.path),
                          self.path,
                          recursive=False)

        try:
            observer.start()

            while True:
                time.sleep(1)
        except Exception as e:
            logging.error("Error on watchdog : %s" % (str(e),))
            observer.stop()
        observer.join()


def main():
    parser = argparse.ArgumentParser(description='')

    parser.add_argument('action', choices=['start', 'stop', 'restart'])
    parser.add_argument('-d', '--debug', default=None, action="store_true",
                        help='activate the debug mode')

    args = parser.parse_args()

    logger = logging.getLogger()
    if getattr(args, 'debug', None) is not None:
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.INFO)

    importer = Importer('importer',
                        os.path.join(base_dir, 'data'),
                        logdir='/tmp',
                        loglevel=logger.getEffectiveLevel(),
                        stdout='/tmp/importer_stdout.log',
                        stderr='/tmp/importer_stderr.log',
                        pidfile='/tmp/importer_pybrief.pid')

    action = getattr(args, 'action', None)
    if action == 'start':
        importer.start()
    elif action == 'stop':
        importer.stop()
    elif action == 'restart':
        importer.restart()
    else:
        return 1

    return 0

if __name__ == "__main__":
    sys.exit(main())
