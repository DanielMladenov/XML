import xml.etree.ElementTree as ET
import numpy as np
import pandas as pd
import re


def cleanHtml(row_string):
    if row_string:
        cleanr = re.compile('<.*?>')
        cleantext = re.sub(cleanr, '', row_string)
        return str(cleantext)
    else:
        return str('InproperLabel')



class xmlReader(object):
    """docstring for xmlReader"""
    def __init__(self, path):
        #super(xmlReader, self).__init__()
        self.path = path
        self.tree = ET.parse(path)
        self.root = self.tree.getroot()


    def getLayout(self, quesName = "name", value = "value", labelName = "text", language="en-US", title = 'title'):
        #Based on the XML structure, the "Columns" cantain all of the flat questions.
        for flatQues in self.root.iter('columns'): 
            for ques in flatQues.iter(quesName):
               self.getFlatQuestion(flatQues, value, labelName, language, title)
            



    def getFlatQuestion(self, oQues, value,labelName,language, title):
        #print(oQues)
        for q in oQues:
            #print(q.attrib)
            print(self.getLabelOfQuesCL(q, labelName, language, title))
            self.getLevel(q)            
            #for cat in q:
                #print(cat.text)
            for Ccat in q.iter('categories'):
                print(self.getCatAtCurrentLevel(Ccat, labelName, language))

    def getCatAtCurrentLevel(self, oCat,labelName, language):
        #print(oCat)
        myCat = []
        myLabel = []
        for cat in oCat:
            #print(cat.text)
            totalyNeedlessFlag = False
            myCat.append(cat.text)
            for label in cat.iter(labelName):
                if totalyNeedlessFlag:
                    break             
                myTempVal = label.attrib.values()
                for key in myTempVal:
                    if key == language:
                        #print(label.text)
                        combineLabel = ""
                        for t in label.itertext():
                            combineLabel = combineLabel + " " + t
                        tempLabel = cleanHtml(combineLabel)
                        myLabel.append(tempLabel)
                        totalyNeedlessFlag = True

        return dict(zip(myCat, myLabel))

    def getLevel(self, oQues):
        for key in oQues.attrib:
                if key == 'level':
                    return str(oQues.attrib[key])


    def getLabelOfQuesCL(self, oQues, labelName, language,  title):
        print(oQues)
        for title in oQues.iter(title):
            totalyNeedlessFlag = False
            for label in title.iter(labelName):
                if totalyNeedlessFlag:
                    break
                myTempVal = label.attrib.values()
                for key in myTempVal:
                    if key == language:
                        combineLabel = ""
                        for t in label.itertext():
                            combineLabel = combineLabel + " " + t
                        tempLabel = cleanHtml(combineLabel)
                        totalyNeedlessFlag = True

        return tempLabel


        



xmlTest = xmlReader('../docs/XML.xml')

xmlTest.getLayout(quesName = 'name', value = "value", labelName = "text", language = "en-CA")


#[[ 1 , 2],[2,6],[3,7]]
#{'_1' : {'1' : 'Gosho'}}
#{'LOOPVI' : {1 : { '_1' : 'Co-Op', '_2' : 'Costco'}, 0 : {'_4' : 'Very likely', '_3' : 'Somewhat likely'} }}  !!!
tempDic = {'QPRMSHP' : { '_1' : 'primarily you alone', '_2' : 'You and someone else equally'}}
testPD = pd.DataFrame(tempDic)
 
testPD.to_csv(r'../docs/TestCsv.csv')

#print(testPD)

#C:\\Users\\Daniel.Mladenov\\github\\JTI\\
#checkIfWork = getLayout(quesName = "name", value = "value", labelName = "text", xml = '../docs/XML.xml', language = "en-CA")
#checkIfWork = pd.DataFrame(checkIfWork)

#checkIfWork.to_csv(r'../docs/TestCsv.csv')

# The check for the dublicated labels of categories in the same question

