import xml.etree.ElementTree as ET
import re

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

    def checkQuestionName(self): #compare the current question name to the previous and next question in order to find out if it's part of a group.
        for i in range(1, self.listQuesLen):
            if i != self.listQuesLen - 1:
                print(self.listQues[i-1], self.listQues[i], self.listQues[i+1])
                #return [self.listQues[i-1], self.listQues[i], self.listQues[i+1]]
            else:
                print(self.listQues[i-1], self.listQues[i])
                #return [self.listQues[i-1], self.listQues[i]]

    def getNoFlatQuestionMatrix(self):
        for i in range(1, self.listQuesLen):
            if self.listQues[i].find(self.standardDelimiter) != -1:
                self.matrix.append([0,1,0])
            else:
                pass
                self.matrix.append([0,0,0])





    def printMyQues(self):
        print(self.matrix)



#==================================

#xmlTest = xmlImport('../docs/12375e01_liv.xml')
xmlTest = xmlImport(r'C:\Users\Danie\Documents\GitHub\XML\docs\147736_SurveyData.xml')
xmlTest.getLayout()
xmlTest.getNoFlatQuestionMatrix()
#xmlTest.printMyQues()


