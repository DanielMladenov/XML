from turtle import left
import xml.etree.ElementTree as ET
import re
import pandas as pd

class xmlImport(object):
    """docstring for xmlReader"""
    def __init__(self, path):
        #super(xmlReader, self).__init__()
        parser = ET.XMLParser(encoding="iso-8859-5")
        self.path = path
        self.tree = ET.parse(path, parser=parser)
        self.root = self.tree.getroot()
        self.listQues = []
        self.listQuesLen = 0
        self.standardDelimiter = "_"
        self.matrix = []

    def getLayout(self, quesName = "name", value = "value", labelName = "text", language="en-US", title = 'title'):
        for ques in self.root.iter('variable'):
             for name in ques.findall(quesName):
                #  print(name.text)
                self.listQues.append(name.text)
                
        self.listQuesLen = len(self.listQues)

    def quesNameArr(self, i): #compare the current question name to the previous and next question in order to find out if it's part of a group.
        if i != self.listQuesLen - 1:
           #print(self.listQues[i-1], self.listQues[i], self.listQues[i+1])
            return [self.listQues[i-1], self.listQues[i], self.listQues[i+1]]
        else:
            #print(self.listQues[i-1], self.listQues[i])
            return [self.listQues[i-1], self.listQues[i]]

    def getNoFlatQuestionMatrix(self):
        for i in range(0, self.listQuesLen):
            if self.listQues[i].find(self.standardDelimiter) != -1:
                firstPosition = self.getNoFlatQuestionFirstPosition( self.quesNameArr(i), self.listQues[i].find(self.standardDelimiter))
                midPosition = self.getNoFlatQuestionMidPosition()
                lastPosition = self.getFlatQuestionLastPosition( self.quesNameArr(i), self.listQues[i].find(self.standardDelimiter))
                self.matrix.append([firstPosition,midPosition,lastPosition])
            else:                
                self.matrix.append([0,0,0])

    def getNoFlatQuestionFirstPosition(self, arr,delimPosition):
        if len(arr) == 3:    
            if arr[1][:delimPosition+1] == arr[0][:delimPosition+1]:  #check if the current quesName (left from the delim) match with the previous question names
                return 1
            elif arr[1][:delimPosition+1] == arr[2][:delimPosition+1]:    #check if the current quesName (left from the delim) match with the next question name
                return 1
            else:
                return 0
        elif len(arr) == 2:
            if arr[1][:delimPosition+1] == arr[0][:delimPosition+1]:  #check if the current quesName (left from the delim) match with the previous question name
                return 1
            else:
                return 0
        else:
            print("Array of question names has unexpected len (number of elements). Number of elements should be 2 or 3")

    def getNoFlatQuestionMidPosition(self):
        return 1
    
    def getFlatQuestionLastPosition(self, arr,delimPosition):
        postFix = arr[1][delimPosition+1:]
        if re.search('^[0-9]', postFix):
            return 1
        else:
            return 0
            

    def printMyQues(self):
        print(self.matrix)

    def flatQuesToDF(self, type):
        if type.lower() == 'flat':            
            df = pd.DataFrame(zip(self.listQues, self.matrix), columns=['quesName', 'matrix'])
            return df

    def csvExport(self, df, name):
        df.to_csv('docs\\'+name+'.csv')



#==================================

#xmlTest = xmlImport('../docs/12375e01_liv.xml')
xmlTest = xmlImport(r'docs\147736_SurveyData.xml')
xmlTest.getLayout()
xmlTest.getNoFlatQuestionMatrix()

xmlTest.csvExport(xmlTest.flatQuesToDF('flat'), "test")


