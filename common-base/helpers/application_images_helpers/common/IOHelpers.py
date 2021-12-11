from pathlib import Path
from termcolor import colored
import sys

class IOHelpers:
	'''
	Helper functionality related to I/O operations
	'''
	
	@staticmethod
	def log_stderr(message, color=None, attrs=[]):
		'''
		Prints a formatted log message to stderr
		'''
		print(colored('{}'.format(message), color=color, attrs=attrs), file=sys.stderr, flush=True)
	
	@staticmethod
	def read_file(filename):
		'''
		Reads the entire contents of the specified file
		'''
		return Path(filename).read_bytes().decode('utf-8')
	
	@staticmethod
	def write_file(filename, data):
		'''
		Writes the supplied data to the specified file
		'''
		Path(filename).write_bytes(data.encode('utf-8'))
