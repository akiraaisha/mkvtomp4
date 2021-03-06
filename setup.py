import sys
import os
import subprocess as sp
from distutils.core import setup, Command
from simplemkv.tomp4 import __doc__
try:
    from simplemkv.version import __version__
except ImportError:
    __version__ = 'unknown'


# A list of classifiers can be found here:
#   http://pypi.python.org/pypi?%3Aaction=list_classifiers
classifiers = """\
Natural Language :: English
Development Status :: 4 - Beta
Environment :: Console
Topic :: Multimedia
Topic :: Multimedia :: Sound/Audio :: Conversion
Topic :: Multimedia :: Video :: Conversion
Intended Audience :: End Users/Desktop
License :: OSI Approved :: MIT License
Programming Language :: Python
Operating System :: OS Independent
"""


def write_version(v):
    f = open('simplemkv/version.py', 'w')
    try:
        f.write('__version__ = %s\n' % repr(v))
    finally:
        f.close()


def git_version():
    cmd = ['git', 'describe', '--abbrev=4']
    try:
        proc = sp.Popen(cmd, stdout=sp.PIPE)
        stdout = proc.communicate()[0].rstrip('\n')
    except OSError:
        sys.stderr.write('git not found: leaving __version__ alone\n')
        return __version__
    if proc.returncode != 0:
        sys.stderr.write('git describe failed: leaving __version__ alone\n')
        return __version__
    ver = stdout.lstrip('mkvtomp4-v')
    write_version(ver)
    try:
        proc = sp.Popen(['git', 'update-index', '-q', '--refresh'])
        proc.communicate()
    except OSError:
        return ver
    if proc.returncode != 0:
        return ver
    try:
        proc = sp.Popen(['git', 'diff-index', '--name-only', 'HEAD', '--'], stdout=sp.PIPE)
        stdout = proc.communicate()[0]
    except OSError:
        sys.stderr.write('git diff-index failed\n')
    if stdout.strip('\n'):
        ver = ver + '-dirty'
        write_version(ver)
    return ver


if sys.version_info < (2, 3):
    _setup = setup
    def setup(**kwargs):
        if kwargs.has_key("classifiers"):
            del kwargs["classifiers"]
        _setup(**kwargs)


doclines_ = __doc__.split("\n")
codeopts = {
    'name': 'mkvtomp4',
    'description': doclines_[0],
    'long_description': "\n".join(doclines_[2:]),
    'author': 'Gavin Beatty',
    'author_email': 'gavinbeatty@gmail.com',
    'maintainer': 'Gavin Beatty',
    'maintainer_email': 'gavinbeatty@gmail.com',
    'license': 'http://opensource.org/licenses/MIT',
    'platforms': ["any"],
    'classifiers': filter(None, classifiers.split("\n")),
    'url': 'http://code.google.com/p/mkvtomp4/',
    'version': __version__,
    'scripts': ['mkvtomp4.py'],
    'py_modules': ['simplemkv.version', 'simplemkv.info', 'simplemkv.tomp4'],
}
fullopts = codeopts.copy()
fullopts['data_files'] = [
    ('share/doc/mkvtomp4', ['README.mkd', 'LICENSE', 'doc/mkvtomp4.txt']),
    ('share/man/man1', ['doc/mkvtomp4.1', 'doc/mkvtomp4.1.html']),
]


if __name__ == '__main__':
    __version__ = git_version()
    fullopts['version'] = __version__
    setup(**fullopts)
