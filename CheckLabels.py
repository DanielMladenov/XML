import pandas as pd
import xml.etree.ElementTree as ET
import re

def cleanHtml(row_string):
    if row_string:
        cleanr = re.compile('<.*?>')
        cleantext = re.sub(cleanr, '', row_string)
        return str(cleantext)
    else:
        return str('InproperLabel')

def getLayoutForLabels(quesName, labelQuestion, language, xml):
    tree = ET.parse(xml)
    root = tree.getroot()

    myQues = []
    myLabel = []
    finalDict = {}
    tempDict = {}

    for MddTree in root.iter('variable'):
        myQues = ''
        myLabel = ''
        tempDict = {}

        for ques in MddTree.iter(quesName):
            myQues = ques.text
            totalyNeedlessFlag = False
            for qLabel in MddTree.iter(labelQuestion):
                if totalyNeedlessFlag:
                    break
                for text in qLabel.iter('text'):
                    myTempVal = text.attrib.values()
                    for key in myTempVal:
                        if key == str(language):
                            combine = ""
                            for t in text.itertext():
                                combine = combine + " " + t
                            myLabel = combine
                            totalyNeedlessFlag = True


        tempDict = {myQues : myLabel}
        finalDict.update(tempDict)

    return finalDict

labelFrame = getLayoutForLabels(quesName = "name", labelQuestion = 'label', language = 'en-US', xml = 'xml290120MDD.xml')
#print(labelFrame)
labelFrame = pd.DataFrame(labelFrame, index = [0])
labelFrame.to_csv(r'Labels.csv')
