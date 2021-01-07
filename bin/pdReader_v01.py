import numpy as np
import pandas as pd
import re
from XMLExplorer_v03 import xmlReader


#Reading the XML file
xmlTest = xmlReader('../docs/XML_FC.xml')
tempDic = xmlTest.getLayout(quesName = 'name', value = "value", labelName = "text", language = "en-US")
testPD = pd.DataFrame(tempDic)
#Write the CSV file
testPD.to_csv(r'../docs/TestCsv.csv')

#===================================Seting new function==================================================


class arrayBuilderMDD(object):
	"""docstring for arrayBuilderMDD"""
	def __init__(self, ar, possition):
		self.ar = ar
		self.possition = possition
		self.valid = self.checkValid()

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
		pass

	def writeArr(self):
		ret = []
		if self.valid:
			ar = self.ar

			ret.append(self.writeLevel(ar))
			ret.append(self.writeType())
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
		print(check)
		if pd.isna(cc[1]) == False:
			pass



# [1, 1, 1, 1]