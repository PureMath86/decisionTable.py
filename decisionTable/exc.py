class Error(Exception):
	"""Generic errors."""

	def __init__(self, msg):
		Exception.__init__(self)
		self.msg = msg

	def __str__(self):
		return self.msg


class TableError(Error):
	"""Table related errors."""
	pass

class FieldError(TableError):
	"""Field related errors."""
	pass

class RecordError(TableError):
	"""Record related errors."""
	pass
