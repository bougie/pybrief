#!/usr/bin/env python
import os
import sys
import time
import django
import fnmatch
import atexit
import signal
import resource
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

base_dir = os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(base_dir)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "pybrief.settings")
django.setup()

from blog.utils import parse_blog_file
from blog.forms import PostForm


class Daemon:
    """A generic daemon class.

    Usage: subclass the Daemon class and override the run() method"""

    def __init__(self, pidfile, stdin='/dev/null', stdout='/dev/null',
                 stderr='/dev/null'):
        self.stdin = stdin
        self.stdout = stdout
        self.stderr = stderr
        self.pidfile = pidfile

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
            sys.stderr.write("fork #1 failed: %d (%s)\n" % (e.errno,
                                                            e.strerror))
            sys.exit(1)

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
            sys.stderr.write("fork #2 failed: %d (%s)\n" % (e.errno,
                                                            e.strerror))
            sys.exit(1)

        # close all open file descriptors
        maxfd = resource.getrlimit(resource.RLIMIT_NOFILE)[1]
        if (maxfd == resource.RLIM_INFINITY):
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

        # A daemon is never localized
        os.environ.setdefault("LC_ALL", "POSIX")

        # write pidfile
        atexit.register(self._delpid)
        pid = str(os.getpid())
        with open(self.pidfile, 'w+') as f:
            f.write("%s\n" % pid)

        # Handler SIGTERM signal
        signal.signal(signal.SIGTERM, self.handler)

    def handler(self, signum, frame):
        if signum == signal.SIGTERM:
            # pidfile will be deleted by _delpid
            atexit.exit(0)

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
            sys.stderr.write(
                "pidfile %s already exist. Daemon already running?\n" % (
                    self.pidfile,))
            sys.exit(1)

        # Start the daemon
        self.daemonize()
        self.run()

    def stop(self):
        """Stop the daemon"""

        pid = self._getpid()
        if pid is not None:
            sys.stderr.write(
                "pidfile %s already exist. Daemon already running?\n" % (
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


def import_files(path):
    for item in os.listdir(path):
        filename = os.path.join(path, item)
        if fnmatch.fnmatch(filename, '*.bp'):
            bpcontent = parse_blog_file(filename)
            if bpcontent is not None:
                try:
                    PostForm(bpcontent).save()
                except Exception as e:
                    print(str(e))


class PostFileEventHandler(FileSystemEventHandler):
    def __init__(self, path, *args, **kwargs):
        self.path = path

        super(PostFileEventHandler, self).__init__(*args, **kwargs)

    def on_any_event(self, event):
        import_files(self.path)


class Importer(Daemon):
    def __init__(self, path, *args, **kwargs):
        self.path = path

        super(Importer, self).__init__(*args, **kwargs)

    def run(self):
        observer = Observer()
        observer.schedule(PostFileEventHandler(self.path),
                          self.path,
                          recursive=False)

        try:
            observer.start()

            while True:
                time.sleep(1)
        except Exception as e:
            sys.stderr.write("Error on watchdog : %s" % (str(e)))
            observer.stop()
        observer.join()


def main():
    importer = Importer(os.path.join(base_dir, 'data'),
                        pidfile='/tmp/importer_pybrief.pid',
                        stdout='/tmp/stdout.log',
                        stderr='/tmp/stderr.log')
    importer.start()

    return 0

if __name__ == "__main__":
    sys.exit(main())
