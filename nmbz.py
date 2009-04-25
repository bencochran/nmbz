'''
NMBZ - Some handy little classes relating to numbers/math

Author: Ben Cochran
License: MIT License, see program file for details
More info: http://github.com/bcochran/nmbz
'''

# This software is made available under the terms of the MIT License.
# 
# Copyright (c) 2009 Ben Cochran
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy of
# this software and associated documentation files (the "Software"), to deal in
# the Software without restriction, including without limitation the rights to
# use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
# the Software, and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
# FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
# COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
# IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.


class matrix(object):
	'''
	Matrix class.
	
	'''
	def __init__(self, data, **optional_args):
		self.data = []
		
		# dtype stuff to come
		#self.dtype = int
		#if optional_args.has_key('dtype'):
		#	optional_args['dtype']
		#else:
		#	self.dtype = None
		#	dtypeAuto = True
		
		# size = (m,n) for an m x n matrix (m rows, n columns)
		self.mSize = (None, None)
		self.longestString = 0
		if isinstance(data, (list, tuple)):
			for row in data:
				if self.mSize[0] == None:
					self.mSize = (len(data),len(row))
				elif len(row) != self.mSize[1]:
					raise ValueError("inconsistent row size: %s" % data)
				if isinstance(row, (list, tuple)):
					for i in row:
						if not isinstance(i, (int, float, long, complex)):
							raise ValueError("invalid type: %s" % type(i))
						if len("%s" % i) > self.longestString:
							self.longestString = len("%s" % i)
					self.data.append(list(row))
				else:
					raise ValueError("invalid type: %s" % type(row))
		else:
			raise ValueError("invalid type: %s" % type(data))
	
	def __repr__(self):
		outStrings = []
		for row in self.data:
			outStrings.append("[%s]" % ", ".join([("%s" % i).rjust(self.longestString) for i in row]))
		
		return "matrix([%s])" % ",\n        ".join(outStrings)
	
	def __str__(self):
		outStrings = []
		for row in self.data:
			outStrings.append("[%s]" % " ".join([("%s" % i).rjust(self.longestString) for i in row]))
		
		return "[%s]" % "\n ".join(outStrings)

	def __len__(self):
		return len(self.data)

	def __getitem__(self, offset):
		if isinstance(offset, int):
			return matrix([self.data[offset]])			
		elif isinstance(offset, tuple):
			if len(offset) == 1:
				return self[offset[0]]
			elif len(offset) == 2:
				if isinstance(offset[0], int) and isinstance(offset[1], int):
					return self.data[offset[0]][offset[1]]
				elif isinstance(offset[0], int) and isinstance(offset[1], slice):
					return matrix([self.data[offset[0]][offset[1]]])
				elif isinstance(offset[0], slice) and isinstance(offset[1], int):
					return matrix([[item[offset[1]]] for item in self.data[offset[0]]])
				elif isinstance(offset[0], slice) and isinstance(offset[1], slice):
					return matrix([item[offset[1]] for item in self.data[offset[0]]])
				else:
					raise IndexError("invalid index: %s" % offset)
			else:
				raise IndexError("invalid index: %s" % offset)
		elif isinstance(offset, slice):
			indices = offset.indices(len(self))
			retList = []
			for i in range(indices[0],indices[1], indices[2]):
				retList.append(self.data[i])
			return matrix(retList)
		else:
			raise IndexError("invalid index: %s" % offset)				
			
	def __mul__(self, other):
		if isinstance(other, matrix):
			if self.mSize[1] != other.mSize[0]:
				raise ValueError("incomputable (%s x %s)*(%s x %s)" % (self.mSize[0], self.mSize[1], other.mSize[0], other.mSize[1]))
			else:
				outSize = (self.mSize[0], other.mSize[1])
				outData = [[0 for i in range(outSize[1])] for j in range(outSize[0])]
				for i in xrange(outSize[0]):
					row = self[i]
					for j in xrange(outSize[1]):
						col = other[:,j]
						itemSum = 0
						for n in xrange(len(col)):
							a = row[0,n]
							b = col[n,0]
							itemSum += a*b
						outData[i][j] = itemSum
				return matrix(outData)
		elif isinstance(other, (int, float, long, complex)):
			return matrix([[other * self[i,j] for j in range(self.mSize[1])] for i in range(self.mSize[0])])
		else:
			return NotImplemented
			
	def astype(self, dtype):
		'''
		Returns a copy of the matrix with values cast as the given dtype.
		'''
		return matrix([[dtype(self[i,j]) for j in range(self.mSize[1])] for i in range(self.mSize[0])])