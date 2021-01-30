import numpy as np
import pandas as pd
import re
from XMLExplorer_v03 import xmlReader


#Reading the XML file
xmlTest = xmlReader('../docs/XML_FC.xml')
tempDic = xmlTest.getLayout(quesName = 'name', value = "value", labelName = "text", language = "en-US")
testPD = pd.DataFrame(tempDic)
#Write the CSV file
testPD.to_csv(r'..\docs\TestCsv.csv')

#===================================Seting new function==================================================


class arrayBuilderMDD(object):
	"""docstring for arrayBuilderMDD"""

	class categories:

		def __init__(self, innAr):
			self.innAr = innAr

		def count(self):
			for i in range(len(self.innAr)):
				if self.innAr[i].__class__.__name__ == 'dict' or self.innAr[i].__class__.__name__ == 'list' or self.innAr[i].__class__.__name__ == 'tuple':
					
					return len(self.innAr[i])-1


	def __init__(self, ar, possition):
		self.ar = ar
		self.possition = possition
		self.valid = self.checkValid()
		self.type = self.writeType()

	def __call__(self):
		pass

	def checkValid(self):
		if pd.isna(self.ar[1]) == True:
			ret = False
		else:
			ret = True

		return ret

	def print(self):
		print(self.ar)

	def writeLevel(self, ar):
		ret = 0
		#print(ar[0])
		if pd.isna(ar[1]) == False:
			ret = int(ar[0]) - 1
			if ret < 0:
				ret = 0

		return ret

	def writeType(self):
		if self.valid:
			temp = self.ar[1]
			for key in temp:
				#print(key)
				if key == 'Text':
					ret = 2
				elif key == 'Long':
					ret = 1
				else:
					ret = 3

			return int(ret)

	
	def writeCatNum(self):
		temp = self.testttt(self.ar)
		#print(temp)

	def getInnerDic(self, ar):	#This is not in use at the moment 
		try:
			for key, val in ar.items():
				for t in val.values():
					print(t)
			#for key in ar.vlues():
				#self.getInnerDic(key)
		except:
			return ar

	def testttt(self, ar):
			for i in range(len(ar)):
				if ar[i].__class__.__name__ == 'dict' or ar[i].__class__.__name__ == 'list' or ar[i].__class__.__name__ == 'tuple':
					print(ar[i])
					#self.testttt(ar[i])
					

				#else:
					#print(ar[i])
					#return ar[i]	


	def writeArr(self):			#This is mainFunction to Write the array
		ret = []
		if self.valid and self.type == 3:
			ar = self.ar

			ret.append(self.writeLevel(ar))
			ret.append(self.writeType())
			ret.append(self.categories(ar).count())
			#print(self.categories(ar).count())
			

			#print(ar)
			#print(ret)
			return ret
		

##========================= 	TESTING ========================================
for (columnName, columnData) in testPD.iteritems():
	#print(columnData)
	for cc in columnData.iteritems():
		#print(cc)
		tes = arrayBuilderMDD(cc, 1)
		#tes.print()
		#tes.writeLevel(cc)
		#tes.writeType()
		check = tes.writeArr()
		#print(check)
		



# [1, 1, 1, 1]