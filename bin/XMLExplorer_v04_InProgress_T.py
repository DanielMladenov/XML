import xml.etree.ElementTree as ET
import numpy as np
import pandas as pd
import re




class xmlReader(object):
    """docstring for xmlReader"""
    def __init__(self, path):
        #super(xmlReader, self).__init__()
        parser = ET.XMLParser(encoding="iso-8859-5")
        self.path = path
        self.tree = ET.parse(path, parser=parser)
        self.root = self.tree.getroot() 
       


    def get_inner_object(self):
        return self.mlMode(self)


    class mlMode(object):
        """ML mode / getting export for learning"""
        def __init__(self, xmlReader):
            self.xmlReader = xmlReader
            self.root = self.xmlReader.root



        def mlCatLabels(self):
            ret = []
            for flatQues in self.root.iter('columns'): 
               #print(flatQues)
                for ques in flatQues.iter('variable'):
                    #print(self.xmlReader.getCatAtCurrentLevel(ques, "text", "en-US", 'title'))
                    TempIdent = self.xmlReader.getType(ques)
                    if TempIdent == '3':
                        for Ccat in ques.findall('categories'):    # old version was oQues.iter('categories')
                            TempCategories = self.xmlReader.getLabelatCurrentLevel(Ccat, "text", "en-US")
                            ret.append(TempCategories)
                        
            return ret


        def mlQuesLabel(self):
            ret = []
            for flatQues in self.root.iter('columns'):
                for ques in flatQues.iter('variable'):
                    ret.append(self.xmlReader.getLabelOfQuesCL(ques, "text", "en-US", "title"))

            return ret
                

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
                #print(self.getGridQuestion(ques, quesName, value, labelName, language, title, retDict))
                temp = {'Grid_' + str(innerCounter) : self.getGridQuestion(ques, quesName, value, labelName, language, title, retDict)}
                ret.update(temp)
        return ret


    def cleanHtml(self,row_string):
        if row_string:
            cleanr = re.compile('<.*?>')
            cleantext = re.sub(cleanr, '', row_string)
            return str(cleantext)
        else:
            return str('InproperLabel')

    def getGridQuestion(self, oQues, quesName, value, labelName, language, title, retDict):
        TempLevel = self.getLevel(oQues)
        #TempName = self.getNameCL(oQues, quesName)  This is used for debuging
        #print(TempLevel + " - " + TempName + " - " + str(oQues) + " - " + str(quesName)
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
            #print(self.getFlatQuestion(oQues, quesName, value, labelName, language, title))
            #print(str(oQues))
            for innerQues in oQues.findall('variable'):
                self.getGridQuestion(innerQues, quesName, value, labelName, language, title,retDict)

       
        return(retDict)


    
    def getFlatQuestion(self, oQues, quesName, value,labelName,language, title):
        #print(oQues)
        #for q in oQues:
            #print(oQues)
            TempIdent = self.getType(oQues)
            #print(TempIdent)
            TempLabel = self.getLabelOfQuesCL(oQues, labelName, language, title)
            TempLevel = self.getLevel(oQues)            
            TempName = self.getNameCL(oQues, quesName)
            #Geting Categories
            if TempIdent == '3':
                for Ccat in oQues.findall('categories'):    # old version was oQues.iter('categories')
                   TempCategories = self.getCatAtCurrentLevel(Ccat, labelName, language)
            else:
                TempCategories = {}    # No categories in the Text and Long questions

            #print(self.assembler(TempLevel, TempName, TempLabel, TempCategories))
            return self.assembler(TempLevel, TempName, TempLabel, TempCategories, TempIdent)

    def getLabelatCurrentLevel(self, oCat, labelName, language):
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
                        tempLabel = self.cleanHtml(combineLabel)
                        myLabel.append(tempLabel)
                        totalyNeedlessFlag = True

        return myLabel

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
                        tempLabel = self.cleanHtml(combineLabel)
                        myLabel.append(tempLabel)
                        totalyNeedlessFlag = True

        return dict(zip(myCat, myLabel))

    def getLevel(self, oQues):
        for key in oQues.attrib:
                if key == 'level':
                    return str(oQues.attrib[key])

    def getType(self, oQues):
        for ident in oQues.attrib:
            if ident == 'ident':
                return str(oQues.attrib[ident])
        


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
                        tempLabel = self.cleanHtml(combineLabel)
                        totalyNeedlessFlag = True

        return tempLabel


    def getNameCL(self, oQues, quesName):
        
        for name in oQues.findall(quesName):
            retName = name.text   

        
        return retName
        


    def assembler(self, quesLevel, quesName, quesLabel, quesCategories, ident):
        #print(quesName)
        if ident == '3':
            temp = {quesName : quesLabel}
            temp.update(quesCategories)

            ret = {quesLevel : temp}
        elif ident == '2':   # Text
            temp = {'Text' : {quesName : quesLabel}}
            ret = {quesLevel : temp}
        elif ident == '1':   # Long
            temp = {'Long' : {quesName : quesLabel}}
            ret = {quesLevel : temp}
        
        print(ret)
        return ret

   
#=========================================================================================================
#=========================================================================================================
#=========================================================================================================

xmlTest = xmlReader('../docs/XML_BNP.xml')
ml = xmlTest.get_inner_object()

testPD = pd.Series(ml.mlQuesLabel())
print(testPD)
testPD.to_csv(r'../docs/mlLab_BNP.csv')


#xmlTest.mlMode(xmlTest).mlLabels()

#tempDic = xmlTest.getLayout(quesName = 'name', value = "value", labelName = "text", language = "en-US")
#testPD = pd.DataFrame(tempDic)

#testPD.to_csv(r'../docs/TestCsv.csv')

