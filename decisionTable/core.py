import re
from tabulate import tabulate

from decisionTable import exc
# Todo: String, regex, glob, evaluation expression
'''
Valid elements objects, string, regex, glob, templating with format, function, error
['in0', 'in1', 'out0']
['in1<self', 'in1<0', '3']
'''

class parent(object):
	def __str__(self):
		return '<parent>'

class DecisionTable(object):

	def __init__(self, fields, *records, **config):
		self.fields = fields
		self.records = records
		self.parentSym = config.get('parentSym', '.')

	def test(self):
		# All fields should be strings, containing safe characters
		fieldForm = re.compile(r'^[a-zA-Z_]+$')
		for i, field in enumerate(self.fields):
			if not isinstance(field, str):
				raise exc.TableError("{}. field is not string.".format(i+1))
			elif not fieldForm.match(field):
				raise exc.TableError("{}. field is not in {} form.".format(i+1, fieldForm.pattern))

		# Records length must be equal with fields length
		fieldsLen = len(self.fields)
		for i, record in enumerate(self.records):
			if len(record) != fieldsLen:
				raise exc.TableError("{}. record length is not equal to fields length.".format(i+1))

	def __str__(self):
		records = [[i+1] + list(record) for i, record in enumerate(self.records)]
		return tabulate(records, headers=['Index'] + list(self.fields), tablefmt='grid')

if __name__ == '__main__':
	table = DecisionTable(
		('packageState', 'configState', 'config', 'action', 'new_packageState', 'new_configState'),
		('None', 'None', 'False', 'install', 'install', 'install'),
		('ok', 'ok', 'False', 'purge', 'purge', 'purge'),
		(parent(), parent(), 'True', 'purge', 'ok', 'purge'),
		('.', '.', 'True', 'update', 'ok', 'update'),
		('ok', 'error', 'False', 'purge', 'purge', 'purge'),
		('.', '.', 'True', 'ok', 'ok', 'update'),
		('.', '.', 'True', 'install', 'ok', 'install'),
		('.', '.', 'True', 'purge', 'ok', 'purge'),
		('error', 'install', 'False', 'purge', 'purge', 'purge'),
		('.', '.', 'False', 'install', 'install', 'install'),
		('None', 'error', 'True', 'purge', 'None', 'purge'),
		('error', 'purge', 'False', 'purge', 'purge', 'purge'),
		('ok', 'None', 'True', 'install', 'ok', 'install'),
		('.', '.', 'False', 'purge', 'purge', 'None'),
		('*', '*', '*', '*', 'ERROR', 'ERROR')
	)
	table.test()
	print(table)
