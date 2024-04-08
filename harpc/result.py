# result.py

class Result:
	def __init__(self, description, rows):
		self.descript   = description
		self.rows	   = rows

	def __repr__(self):
		return str(self.rows)

	def __getitem__(self, x):
		return self.rows[x]

	def __getslice__(self, x, y):
		return self.rows[x:y]

	def __len__(self):
		return len(self.rows)

	def data(self, count):
		try:
			x, y = count
		except:
			if not cmp(str(count).upper(), 'ALL'):
				x, y = 0, len(self.rows)
			else:
				x, y = 0, count

		return self.rows[x:y]

	def column(self):
		return self.descript

	def show(self):
		pass

class nResult(Result):
	def __init__(self, description, rows, sort = None):
		Result.__init__(self, description, rows)
		self.__sort__ = sort

	def sortopt(self, sort = None):
		if not sort:
			return self.__sort__
		elif sort.has_key('index') or sort.has_key('order'):
			self.__sort__.update(sort)

	def sort(self):
		sortidx = 0

		try:
			sortidx = self.descript.index(self.__sort__['index'])
		except:
			self.__sort__['index'] = self.descript[sortidx]

		if cmp(self.__sort__['order'], 'ASC'):
			self.rows.sort(lambda x, y, idx = sortidx: cmp(y[idx], x[idx]))
		else:
			self.rows.sort(lambda y, x, idx = sortidx: cmp(y[idx], x[idx]))

class DBResult(Result):
	def __init__(self, rowcount, description, rows):
		Result.__init__(self, description, rows)
		self.rowcount = rowcount

	def column(self):
		return map(lambda i, x = self.descript: x[i][0], range(len(self.descript)))

class FWResults(Result):
	pass

class FWResult:
	def __init__(self, idx, row):
		self.idx = idx
		self.row = row

	def __repr__(self):
		return str(self.row)

	def __getitem__(self, x):
		return self.row[x.upper()]

	def __setitem__(self, x, y):
		return self.row.update({x.upper():y})


import types
def PackList(l):
	import re, struct

	f = ''; d = ''
	p = re.compile('\[|\]')

	for v in l:
		if type(v) == types.StringType:
			f += '%ds' % len(v)
		elif type(v) == types.FloatType:
			f += 'f'
		elif type(v) == types.LongType:
			f += 'l'
		elif type(v) == types.IntType:
			f += 'i'

	return (f, eval('struct.pack(f, %s)' % p.sub('', repr(l))))

def UnpackList((f, d)):
	import struct

	return struct.unpack(f, d)

CONST = {
	# System Character
	'STX'		: '\x02',	# Start Text(Total Data)
	'USG'		: '\x03',	# Start Usage
	'SAH'		: '\x04',	# Start Application Header
	'STD'		: '\x05',	# Start Table Define
	'SFD'		: '\x06',	# Start Field Define
	'SRD'		: '\x07',	# Start Record Data
	'LF'		 : '\x0A',	# Line Feed
	'DLE'		: '\x10',	# Deliminator

	 # Field Attribute
	'NOA'		: '\x00',	# No Attribute
	'LNK'		: '\x30',	# Link
	'ALT'		: '\x31',	# Alert
	'DNY'		: '\x32',	# Deny
	'DMP'		: '\x33',	# Dump
	'MNT'		: '\x34',	# Monitor
	'LNKALT'	 : '\x35',	# Link & Alert
	'LNKDNY'	 : '\x36',	# Link & Deny
	'DMPMNT'	 : '\x37',	# Dump & Monitor
	'LNKALTDNY'  : '\x38'	 # Link & Alert & Deny
}

class ResultHandle(Result):

	def __init__(self, result):
		Result.__init__(self, result.descript, result.rows)
		self.rowcount = len(result.rows)
		self.result = ''

	def __getitem__(self, x):
		return self.rows[x]

	def __getslice__(self, x, y):
		return self.rows[x:y]

	def __Mangle__(self):
		result = '%c%07d%s' % (CONST['STX'], len(self.result)+8, self.result)
		self.result = ''

		return result

	def __MangleData__(self, data):
		if not type(data) in [types.ListType, types.TupleType]:
			raise TypeError, 'ResultHandle : must be list or tuple'

		return reduce(lambda x, y: str(x) + CONST['DLE'] + str(y), data) + CONST['DLE']

	def __AppzData__(self, data = ''):
		self.result += '%c%s' % (CONST['SAH'], data)
		return

		if not data:
			return

		self.result += self.__MangleData__(data)

	def __TableHeader__(self):
		self.result += '%c' % CONST['STD']

		info = []
		for elim in self.descript:
			if elim[1] == 4:
				info.append('ftInteger') # type
				info.append(elim[0])	 # name
				info.append(0)		   # scale
			else:
				info.append('ftString')  # type
				info.append(elim[0])	 # name
				info.append(elim[4])	 # scale

		self.result += self.__MangleData__(info)

	def __TableAttrib__(self, attrib):
		self.result += '%c%s' % (CONST['SFD'], attrib)

	def __TableData__(self, cnt='all'):
		self.result += '%c' % CONST['SRD']

		if cnt == 'all':
			stx, cnt = 0, self.rowcount
		elif type(cnt) == types.TupleType:
			stx, cnt = cnt
		else:
			stx, cnt = 0, cnt

		for elim in self.rows:
			if stx:
				stx -= 1;
				continue

			if cnt:
				cnt -= 1
			else:
				break

			self.result += self.__MangleData__(elim)

	def data(self, cnt='all', appz='', attr=''):
		self.__AppzData__(appz)
		self.__TableHeader__()
		self.__TableAttrib__(attr)
		self.__TableData__(cnt)

		return self.__Mangle__()

def test():
	procdescript = [('PID', 12, '', '', 20), \
		('NAME',        12, '', '', 40), \
		('TYPE',        12, '', '', 20), \
		('COMMENT',     12, '', '', 40)]

	d = ResultHandle()
	d.MakeAppzData()
	head = [{'type':'ftInteger', 'name':'Name', 'len':'0'}, \
			{'type':'ftString', 'name':'Test', 'len':'20'}]
	data = [['Minju', 'test1'], ['Miyoun', 'test2']]
	print d.MakeAppzData(head=head, body=data)

if __name__ == '__main__':
	test()
