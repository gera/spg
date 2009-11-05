#!/usr/bin/python

"""
This script takes a string (usually a URL) on the commandline and asks for a
passphrase, generating a password specific for the given string by combining
the two and returning a substring of the md5 of the result.

By default, the script does not print the generated password - only copies it
to the clipboard.

It records the the string in a ~/.spg file which can be used for
autocompletion.

The script takes the following options, given below in the short and long
formats:

	-p	--print		prints the password instead of copying
	-n	--no-record	does not record the string

Copyright (c) 2008, Devendra Gera
This program is free software and is released under the terms of the GPL
version 2.
"""

import os
import platform
import sys
import getopt
import getpass
import hashlib
from base64 import b64encode

def usage():
	print __doc__

def record_to_file(url, filename):
	"""
	records the url to the given filename, if it does not already exist
	in it.
	"""
	contents = []
	if os.path.exists(filename):
		contents = open(filename, "r").readlines()
	s = set(contents)
	s.add("%s\n" % url)
	open(filename, "w").writelines(s)


def copy_to_clipboard(string, win32=False):
	"""
	copies the string to the clipboard
	"""
	if win32:
		try:
			import win32clipboard as wcb
			wcb.OpenClipboard(0)
			wcb.EmptyClipboard()
			wcb.SetClipboardText(string)
			wcb.CloseClipboard()
		except:
			print >> sys.stderr, "Can't copy to win32 clipboard"
			sys.exit(2)
	else:
		try:
			import gtk
			cb = gtk.Clipboard()
			cb.set_text(string)
			cb.store()
		except:
			print >> sys.stderr, "Can't copy to gtk clipboard"
			sys.exit(2)


def main():
	argv = sys.argv[1:]
	no_copy = False
	record = True
	win32 = (platform.system().lower() == "windows")
	if win32:
		key = 'USERPROFILE'
	else:
		key = 'HOME'
	filename = os.path.join(os.environ[key], ".spg")

	try:
		opts, args = getopt.getopt(argv, "pn", ["print", "no-record"])
	except getopt.GetoptError:
		usage()
		sys.exit(2)

	for opt, arg in opts:
		if opt in ("-p", "--print"):
			no_copy = True
		elif opt in ("-n", "--no-record"):
			record = False
		else:
			usage()
			sys.exit(2)

	if args == []:
		# this is primarily for the Win32 'click-on.exe' use case.
		args.append(raw_input("Enter sitename: ").strip())
	url = args[0]
	passphrase = getpass.getpass("Passphrase: ")
	passwd = b64encode(hashlib.md5(passphrase + " " + url).digest())[:10]

	if record:
		record_to_file(url, filename)

	if no_copy:
		print passwd
		return

	copy_to_clipboard(passwd, win32)
	return

if __name__ == "__main__":
	main()

