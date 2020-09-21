import xml.etree.ElementTree as ET
import numpy as np
import pandas as pd
import re
import nested_dict as nd

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
            #for ques in flatQues.iter('variable'):
            tempFlat = self.getFlatQuestion(flatQues, quesName, value, labelName, language, title)


            
        #Grids
        for gridQues in self.root.iter('tables'):
            pass

        return tempFlat



    def getGridQuestion(self, oQues, quesName, value, labelName, language, title):
        pass


    def getFlatQuestion(self, oQues, quesName, value,labelName,language, title):
        #print(oQues)
        for q in oQues:
            #print(q.attrib)
            quesLabel = (self.getLabelOfQuesCL(q, labelName, language, title))
            quesLevel = self.getLevel(q)            
            quesName = self.getNameCL(q, quesName)
            #Geting Categories
            for Ccat in q.iter('categories'):
               quesCategories = self.getCatAtCurrentLevel(Ccat, labelName, language)


        return self.assembler(quesLevel, quesName, quesLabel, quesCategories)

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


    def getNameCL(self, oQues, quesName):
        for name in oQues.iter(quesName):
            tempName = name.text
        return tempName  


    def assembler(self, quesLevel, quesName, quesLabel, quesCategories):
        
        temp = {quesName : quesLabel}
        temp.update(quesCategories)

        ret = {quesLevel : temp}

        return ret



#=========================================================================================================
#=========================================================================================================
#=========================================================================================================

xmlTest = xmlReader('../docs/XML_V2.xml')

print(xmlTest.getLayout(quesName = 'name', value = "value", labelName = "text", language = "en-CA"))


#[[ 1 , 2],[2,6],[3,7]]
#{'_1' : {'1' : 'Gosho'}}
#{'LOOPVI' : {1 : { '_1' : 'Co-Op', '_2' : 'Costco'}, 0 : {'_4' : 'Very likely', '_3' : 'Somewhat likely'} }}  !!!
tempDic = xmlTest.getLayout(quesName = 'name', value = "value", labelName = "text", language = "en-CA")
testPD = pd.DataFrame(tempDic)

testPD.to_csv(r'../docs/TestCsv.csv')

#print(testPD)

#C:\\Users\\Daniel.Mladenov\\github\\JTI\\
#checkIfWork = getLayout(quesName = "name", value = "value", labelName = "text", xml = '../docs/XML.xml', language = "en-CA")
#checkIfWork = pd.DataFrame(checkIfWork)

#checkIfWork.to_csv(r'../docs/TestCsv.csv')

# The check for the dublicated labels of categories in the same question

