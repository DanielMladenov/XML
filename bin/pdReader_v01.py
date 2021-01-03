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


for (columnName, columnData) in testPD.iteritems():
	print(columnData)