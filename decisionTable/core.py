import re
from tabulate import tabulate

from decisionTable import exc
# Todo: String, regex, glob, evaluation expression
'''
Valid elements objects, string, regex, glob, templating with format, function, error
['in0', 'in1', 'out0']
['in1<self', 'in1<0', '3']
'''

# Initialize this fields in decisionTable.__init__.py
class ParentField(object):
	symbol = '.'
	def __str__(self):
		return self.symbol

class ErrorField(ParentField):
	symbol = 'ERROR'

class DecisionTable(object):

	fieldForm = re.compile(r'^[a-zA-Z_]+$')

	# Todo: Make csv parser!
	def __init__(self, table, **config):
		self.fields = table[0]
		self.records = table[1:]


		for i, field in enumerate(self.fields):
			if not isinstance(field, str):
				raise exc.FieldError('{}. field is not string.'.format(i+1, field))
			elif not self.fieldForm.match(field):
				raise exc.FieldError('{}. field "{}" is not in "{}" form.'.format(i+1, field, self.fieldForm.pattern))

		# Records length must be equal with fields length
		fieldsLen = len(self.fields)
		for i, record in enumerate(self.records):
			if len(record) != fieldsLen:
				raise exc.RecordError("{}. record length is not equal to fields length.".format(i+1))

	def test(self):
		pass
		# Todo: Test how many decision has more than one or none outputs.

	def decide(self,**config):
		outFieldsIndex = [self.fields.index(field) for field in config.get('outFields', self.fields) if field in self.fields]
		inFields = [{'index' : self.fields.index(field), 'value': config.get(field)} for field in self.fields if field in config]
		for record in self.records:
			for inField in inFields:
				if record[inField['index']] == inField['value']:
					return tuple(recEle for i, recEle in enumerate(record) if i in outFieldsIndex)



	def __str__(self):
		records = [[i+1] + list(record) for i, record in enumerate(self.records)]
		return tabulate(records, headers=['Index'] + list(self.fields), tablefmt='grid')

if __name__ == '__main__':
	parent = ParentField()
	error = ErrorField()

	table = DecisionTable([
		('packageState', 'configState', 'config', 'action', 'new_packageState', 'new_configState'),
		('None', 'None', 'False', 'install', 'install', 'install'),
		('ok', 'ok', 'False', 'purge', 'purge', 'purge'),
		(parent, parent, 'True', 'purge', 'ok', 'purge'),
		(parent, parent, 'True', 'update', 'ok', 'update'),
		('ok', 'error', 'False', 'purge', 'purge', 'purge'),
		(parent, parent, 'True', 'ok', 'ok', 'update'),
		(parent, parent, 'True', 'install', 'ok', 'install'),
		(parent, parent, 'True', 'purge', 'ok', 'purge'),
		('error', 'install', 'False', 'purge', 'purge', 'purge'),
		(parent, parent, 'False', 'install', 'install', 'install'),
		('None', 'error', 'True', 'purge', 'None', 'purge'),
		('error', 'purge', 'False', 'purge', 'purge', 'purge'),
		('ok', 'None', 'True', 'install', 'ok', 'install'),
		(parent, parent, 'False', 'purge', 'purge', 'None'),
		('*', '*', '*', '*', error, error)
	])
	table.test()
	ele = table.decide(packageState='*', outFields=['new_configState'])
	print(ele)
