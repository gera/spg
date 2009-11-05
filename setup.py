# fix broken behaviour - hardlinks are a FS attribute, not an OS attribute
# without doing this, the builds fail on encfs, AFS, NFS etc.
import os
if hasattr(os, 'link'):
  delattr(os, 'link')

if os.name == 'nt':
  # setuptools doesn't play nicely with py2exe
  from distutils.core import setup
else:
  # we need setuptools on *nix to create .debs with scripts
  from setuptools import setup

args = dict(
  name='spg',
  description='simple password generator',
  author='Devendra Gera',
  author_email='gera@theoldmonk.net',
  url='http://www.github.com/gera/spg',
  version='0.2',
  requires=['cjson', 'base64', 'tempfile', 'logging'],
  package_dir={'spg': '.'},
  packages=['spg'],
  )


if os.name == 'nt':
  import py2exe
  args["console"] = [{"script": "__init__.py", "dest_base": "spg"}]
  args["options"] = {"py2exe": {"bundle_files": 1,
                                "excludes": [
                                  "email", "ftplib", "doctest", "pyreadline",
                                  "difflib", "pickle", "calendar", "unittest",
                                  "subprocess", "multiprocessing", "threading",
                                  "bz2", "bdb", "Queue", "smtplib", "ssl",
                                  "_ssl", "xml", "xmllib", "xmlrpclib",
                                  "unicodedata", "commctrl", "decimal",
                                  "locale", "_socket", "random", "heapq",
                                ]}}
  args["zipfile"] = None
else:
  args['entry_points'] = {
    'console_scripts': [
      'spg = spg:main',
    ]
  }


setup(**args)

