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
        innerCounter = 1
        ret = {}
        for flatQues in self.root.iter('columns'): 
            for ques in flatQues.iter('variable'):                
                temp = {'Ques_'+ str(innerCounter) : self.getFlatQuestion(ques, quesName, value, labelName, language, title)}
                innerCounter = innerCounter + 1
                ret.update(temp)
                #print(temp)
                
        #dict(zip(myCat, myLabel))
        #update(self.getFlatQuestion(ques, quesName, value, labelName, language, title))

            
        #Based on the XML structure, the "Tables" cantain all of the Grid questions.
        for gridQues in self.root.iter('tables'):
            for ques in gridQues.findall('variable'):
                retDict = {} 
                print(self.getGridQuestion(ques, quesName, value, labelName, language, title, retDict))

        
        return ret


    def getGridQuestion(self, oQues, quesName, value, labelName, language, title, retDict):
        TempLevel = self.getLevel(oQues)
        TempName = self.getNameCL(oQues, quesName)
        #print(TempLevel + " - " + TempName)
        #print(type(TempLevel))
        

        #Write the constuction 


        # Check the level (loop or break)   / or numberOfIteration > 5
        if TempLevel.strip() == '0' :
            #print(retDict)
            retDict.update(self.getFlatQuestion(oQues, quesName, value, labelName, language, title))
            #print(retDict)
            #return(retDict)

        else:
            #numberOfIteration = numberOfIteration + 1
            retDict.update(self.getFlatQuestion(oQues, quesName, value, labelName, language, title))
            #print(retDict)
            for innerQues in oQues.findall('variable'):
                self.getGridQuestion(innerQues, quesName, value, labelName, language, title,retDict)

       
        return(retDict)


    
    def getFlatQuestion(self, oQues, quesName, value,labelName,language, title):
        #print(oQues)
        #for q in oQues:
            #print(oQues)
            TempLabel = self.getLabelOfQuesCL(oQues, labelName, language, title)
            TempLevel = self.getLevel(oQues)            
            TempName = self.getNameCL(oQues, quesName)
            #Geting Categories
            for Ccat in oQues.iter('categories'):
               TempCategories = self.getCatAtCurrentLevel(Ccat, labelName, language)

            #print(self.assembler(TempLevel, TempName, TempLabel, TempCategories))
            return self.assembler(TempLevel, TempName, TempLabel, TempCategories)

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
        
        for name in oQues.findall(quesName):
            retName = name.text   

        
        return retName
        


    def assembler(self, quesLevel, quesName, quesLabel, quesCategories):
        #print(quesName)
        temp = {quesName : quesLabel}
        temp.update(quesCategories)

        ret = {quesLevel : temp}


        return ret



#=========================================================================================================
#=========================================================================================================
#=========================================================================================================

xmlTest = xmlReader('../docs/XML_V2.xml')

#print(xmlTest.getLayout(quesName = 'name', value = "value", labelName = "text", language = "en-CA"))


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

